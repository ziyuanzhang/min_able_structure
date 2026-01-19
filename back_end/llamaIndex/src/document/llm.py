from llama_index.llms.ollama import Ollama
llm = Ollama(
    model="qwen3:8b",
    request_timeout=300.0,
    context_window=8192,
    temperature=0,
    verbose=True
)