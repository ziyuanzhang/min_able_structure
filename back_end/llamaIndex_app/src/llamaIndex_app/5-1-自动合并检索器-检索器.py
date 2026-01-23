from llama_index.core import Document,VectorStoreIndex,StorageContext
from llama_index.core.node_parser import HierarchicalNodeParser,get_leaf_nodes, get_root_nodes
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.storage.docstore import SimpleDocumentStore
import config
from llama_index.core.retrievers import AutoMergingRetriever

# =========加载====================
loader = PyMuPDFReader()
docs0 =loader.load_data("./data/llama.pdf")
# for i,doc in enumerate(docs):
#     print(i,"="*40)
#     print(doc.text)
doc_txt = "\n\n".join([d.get_content() for d in docs0])
docs = [Document(text=doc_txt)]
# =========切分=========================
node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=[1204,512,128])
nodes = node_parser.get_nodes_from_documents(docs)
# for i,node in enumerate(nodes):
#     print(i,"="*40)
#     print(node)
leaf_nodes = get_leaf_nodes(nodes)
# print(len(leaf_nodes))
# root_nodes = get_root_nodes(nodes)
# print(len(root_nodes))

# 0-77: 78
# 78-270
# 270-1046: 777
# ==创建文档存储（保存所有层级的节点：root/mid/leaf）===========================
doc_store = SimpleDocumentStore()
doc_store.add_documents(nodes)
# ==构建存储上下文================
storage_context = StorageContext.from_defaults(docstore=doc_store)
# ==仅用 leaf_nodes 构建向量索引（因为只有 leaf 有 embedding）==========================
base_index = VectorStoreIndex(leaf_nodes,storage_context=storage_context)
# ==创建基础检索器（只查 leaf 节点）=============================
base_retriever = base_index.as_retriever(similarity_top_k=6)
retriever = AutoMergingRetriever( # 【关键】包装成自动合并检索器
    base_retriever, # 底层检索器
    storage_context, # 用来查找父节点（必须包含所有层级 nodes！）
    verbose=True,  # 打印合并过程日志
    # 可选参数：
    # max_rank_per_leaf = 10,  # 每个 leaf 最多追溯多少父节点
    # min_rank_per_parent = 2,  # 至少有几个子 leaf 匹配，才合并父节点
    # include_all_metadata = False  # 是否保留父节点 metadata
)
# =========查询==========================
query_str = (
    "What could be the potential outcomes of adjusting the amount of safety"
    " data used in the RLHF stage?"
)

base_nodes = base_retriever.retrieve(query_str)
nodes = retriever.retrieve(query_str)

print("nodes length:",len(nodes))
for i,node in enumerate(nodes):
    print("node",i,"="*40)
    print(node)

print("base_nodes length:",len(base_nodes))
for i,node in enumerate(base_nodes):
    print("base_nodes",i,"="*40)
    print(node)