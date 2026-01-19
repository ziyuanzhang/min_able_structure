from llama_index.core import Document,VectorStoreIndex,StorageContext
from llama_index.core.node_parser import SentenceSplitter,HierarchicalNodeParser,get_leaf_nodes, get_root_nodes
from llama_index.readers.file import PDFReader,PyMuPDFReader
from llama_index.core.storage.docstore import SimpleDocumentStore
# =============================
loader = PyMuPDFReader()
docs0 =loader.load_data("./data/llama.pdf")
# for i,doc in enumerate(docs):
#     print(i,"="*40)
#     print(doc.text)
doc_txt = "\n\n".join([d.get_content() for d in docs0])
docs = [Document(text=doc_txt)]
# ==================================
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
# ===================================
doc_store = SimpleDocumentStore()
doc_store.add_documents(nodes)
storage_context = StorageContext.from_defaults(docstore=doc_store)
base_index = VectorStoreIndex(leaf_nodes,storage_context=storage_context)