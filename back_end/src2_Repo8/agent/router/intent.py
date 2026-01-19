def route_intent(text:str) ->str:
    if "搜索" in text or "查" in text:
        return "search"
    return "qa"