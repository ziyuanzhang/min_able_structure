from langchain_ollama import ChatOllama

model = ChatOllama(
    model="qwen3:4b",
    base_url="http://localhost:11434",
    validate_model_on_init=True,
    temperature=0.8,
)
def generate(prompt:str) -> str:
    print("generate:",prompt)
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt}
    ]
    res = model.invoke(messages)
    print("llm:",res)
    return res.content