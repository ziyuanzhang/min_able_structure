from llama_index.tools.metaphor import MetaphorToolSpec
from llama_index.core.tools.tool_spec.load_and_search import LoadAndSearchToolSpec
from llama_index.core.agent.workflow import FunctionAgent
import asyncio
import datetime
import config
from config import llm
from get_env import METAPHOR_API_KEY

metaphor_tool = MetaphorToolSpec(
    api_key=METAPHOR_API_KEY
)
metaphor_tool_list =  metaphor_tool.to_tool_list()
# for tool in metaphor_tool_list:
#     print(tool.metadata)
tool_ls = LoadAndSearchToolSpec.from_defaults(metaphor_tool_list[4]).to_tool_list()
print(tool_ls)

result = metaphor_tool.search("美国现任总统是谁？",num_results=3)
for ele in result:
    print(ele)

agent = FunctionAgent(
    tools=metaphor_tool_list,
    llm=llm,
    system_prompt="你是一个智能助手。对于任何涉及当前时间、新闻、政治人物或实时信息的问题，你必须使用搜索工具获取最新信息，不要依赖你内部的知识。"
)
async def main():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    prompt = f"当前日期是 {current_date}。请通过搜索引擎确认：美国现任总统是谁？"
    print(f"正在思考中... (Context: {current_date})")

    result = await agent.run(prompt)
    print("\n最终结果：")
    print(result)

if __name__ == "__main__":
     asyncio.run(main())
    # print("*"*40)
    # llm = Ollama(model="qwen3:4b",request_timeout=300.0,      # 等待最多 5 分钟
    # context_window=8192,        # 限制上下文为 8k（足够问答，避免 256k 拖慢）
    # temperature=0.1, verbose=True,)
    # resp = llm.complete("美国总统是谁？")
    # print(resp.text)

