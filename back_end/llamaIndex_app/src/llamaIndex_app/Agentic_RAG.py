# ======================
# 1. 环境设置与依赖
# ======================
import os
import getpass
from typing import Literal
from pydantic import BaseModel, Field

# 设置 OpenAI API Key
def _set_env(key: str):
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}:")
_set_env("OPENAI_API_KEY")

# 安装依赖（若未安装）
# !pip install -U --quiet langgraph "langchain[openai]" langchain-community langchain-text-splitters


# ======================
# 2. 文档加载与预处理
# ======================
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

print("Loading documents...")
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,  # 增大 chunk_size 提高语义完整性
    chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)
print(f"Split into {len(doc_splits)} chunks.")


# ======================
# 3. 向量存储与检索工具
# ======================
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng's blog posts on reward hacking, hallucination, or video diffusion models."
)


# ======================
# 4. 初始化 LLM
# ======================
from langchain.chat_models import init_chat_model

# 使用 gpt-4o-mini（性价比高）或 gpt-4o（更强）
response_model = init_chat_model("openai:gpt-4o-mini", temperature=0)
grader_model = init_chat_model("openai:gpt-4o-mini", temperature=0)


# ======================
# 5. 节点定义
# ======================
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, ToolMessage

# --- 节点 1: 决策是否检索 ---
def generate_query_or_respond(state: MessagesState):
    """LLM decides whether to call tool or answer directly."""
    response = response_model.bind_tools([retriever_tool]).invoke(state["messages"])
    return {"messages": [response]}


# --- 节点 2: 评分检索结果 ---
GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question.\n"
    "Retrieved document:\n\n{context}\n\n"
    "User question: {question}\n"
    "If the document contains keywords or semantic meaning related to the question, grade as relevant.\n"
    "Respond with 'yes' or 'no'."
)

class GradeDocuments(BaseModel):
    binary_score: str = Field(description="'yes' or 'no'")

def grade_documents(state: MessagesState) -> Literal["generate_answer", "rewrite_question"]:
    """Grade retrieved docs; route accordingly."""
    messages = state["messages"]
    question = messages[0].content
    # 最后一条应为 ToolMessage
    last_message = messages[-1]
    if isinstance(last_message, ToolMessage):
        context = last_message.content
    else:
        context = ""

    if not context.strip():
        return "rewrite_question"

    prompt = GRADE_PROMPT.format(question=question, context=context[:2000])  # 防止过长
    response = grader_model.with_structured_output(GradeDocuments).invoke(
        [{"role": "user", "content": prompt}]
    )
    return "generate_answer" if response.binary_score.lower() == "yes" else "rewrite_question"


# --- 节点 3: 重写问题 ---
REWRITE_PROMPT = (
    "Improve the user's question to better capture its semantic intent.\n"
    "Original question:\n-------\n{question}\n-------\n"
    "Rewritten question:"
)

def rewrite_question(state: MessagesState):
    """Rewrite the original question for better retrieval."""
    question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    # 替换用户消息为重写后的问题
    return {"messages": [{"role": "user", "content": response.content}]}


# --- 节点 4: 生成最终答案 ---
GENERATE_PROMPT = (
    "You are an assistant answering questions using ONLY the provided context.\n"
    "If the answer isn't in the context, say 'I don't know based on the provided documents.'\n"
    "Keep your answer concise (max 3 sentences).\n\n"
    "Question: {question}\nContext: {context}"
)

def generate_answer(state: MessagesState):
    """Generate final answer using retrieved context."""
    question = state["messages"][0].content
    context = state["messages"][-1].content if isinstance(state["messages"][-1], ToolMessage) else ""
    prompt = GENERATE_PROMPT.format(question=question, context=context[:2000])
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}


# ======================
# 6. 构建 Graph
# ======================
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

workflow = StateGraph(MessagesState)

# 添加节点
workflow.add_node("generate_query_or_respond", generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node("rewrite_question", rewrite_question)
workflow.add_node("generate_answer", generate_answer)

# 入口
workflow.add_edge(START, "generate_query_or_respond")

# 决策：是否调用工具？
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {"tools": "retrieve", END: END}
)

# 检索后：评分文档
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
    {"generate_answer": "generate_answer", "rewrite_question": "rewrite_question"}
)

# 重写后重新决策
workflow.add_edge("rewrite_question", "generate_query_or_respond")
workflow.add_edge("generate_answer", END)

# 编译图
graph = workflow.compile()


# ======================
# 7. 运行示例
# ======================
if __name__ == "__main__":
    question = "What does Lilian Weng say about types of reward hacking?"
    print(f"User: {question}\n{'='*50}\n")

    for chunk in graph.stream({"messages": [{"role": "user", "content": question}]}):
        for node, update in chunk.items():
            msg = update["messages"][-1]
            role = getattr(msg, "role", "tool")
            content = getattr(msg, "content", str(msg))
            tool_calls = getattr(msg, "tool_calls", [])
            print(f"[{node}]")
            if tool_calls:
                print(f"  → Tool call: {tool_calls[0]['name']}({tool_calls[0]['args']})")
            else:
                print(f"  → {content.strip()}")
            print()