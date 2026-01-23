from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# llm = Ollama(
#     model= "qwen3:4b",
#     request_timeout=300.0,
#     context_window=8192,
#     temperature=0,
#     verbose=True
# )
# embed_model = OllamaEmbedding(
#     model_name="nomic-embed-text",
#     base_url="http://localhost:11434"
# )
llm = Ollama(
    model="qwen3-vl",
    request_timeout=300.0,
)
embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434"
)


Settings.llm = llm
Settings.embed_model = embed_model