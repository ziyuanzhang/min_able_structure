def allow_rag(state) -> bool:

    # 最简单的策略：每次最多 1 次
    return  state['rag_calls']<1