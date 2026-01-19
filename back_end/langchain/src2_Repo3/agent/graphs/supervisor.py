from langgraph.graph import  StateGraph,END
from agent.router.intent import route_intent
from agent.graphs.search_agent import build_search_graph
from agent.graphs.qa_agent import build_qa_graph

search_agent = build_search_graph()
qa_agent = build_qa_graph()

def build_supervisor():
    def router_node(state):
        state["route"] = route_intent(state["input"])
        return state

    async def call_agent(state):

        if state["route"] == "search":
            result =  await search_agent.ainvoke(state)
        else:
            result = await qa_agent.ainvoke(state)

        state["result"] = result["result"]
        return state

    g = StateGraph(dict)
    g.add_node("router",router_node)
    g.add_node("call_agent",call_agent)

    g.set_entry_point("router")
    g.add_edge("router","call_agent")
    g.add_edge("call_agent",END)
    return g.compile()