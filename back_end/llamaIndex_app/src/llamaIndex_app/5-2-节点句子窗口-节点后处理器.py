from llama_index.core.node_parser import SentenceSplitter,SentenceWindowNodeParser
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
# ===================================
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3, #前后各3句
    window_metadata_key="window", #把完整窗口存到 metadata["window"]
    original_text_metadata_key="original_text", #整个原始文档（可选）
)
text_splitter = SentenceSplitter() # 智能切分，优先保证句子完成性
# ==加载数据==================================
documents = SimpleDirectoryReader(input_files=["./data/llama.pdf"]).load_data()
# ==切分==================================
base_nodes = text_splitter.get_nodes_from_documents(documents)
nodes = node_parser.get_nodes_from_documents(documents)

# ==构建索引=============================
base_index = VectorStoreIndex(base_nodes)
sentence_index = VectorStoreIndex(nodes)
# ==查询================================
query_engine = sentence_index.as_query_engine(
    similarity_top_k=2,
    node_postprocessors=[MetadataReplacementPostProcessor(target_metadata_key="window")],
)
window_response = query_engine.query("Can you tell me about the key concepts for safety finetuning")
print(window_response)

base_query_engine = base_index.as_query_engine(similarity_top_k=2)
vector_response = base_query_engine.query("Can you tell me about the key concepts for safety finetuning")
print(vector_response)