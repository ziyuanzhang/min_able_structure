from langgraph.graph import  StateGraph,END
from agent.router.intent import route_intent
from agent.graphs.search_agent import build_search_graph
from agent.graphs.qa_agent import build_qa_graph
from agent.nodes.judge import judge
from agent.nodes.observe import observe
from agent.nodes.retry import retry_policy
from agent.runtime.tracer import trace_node
from agent.nodes.wait import wait
from agent.nodes.human_resume import human_resume

search_agent = build_search_graph()
qa_agent = build_qa_graph()

def build_supervisor():
    @trace_node("router_node")
    def router_node(state):
        state["route"] = route_intent(state["input"])
        return state

    @trace_node("call_agent")
    async def call_agent(state):

        if state["route"] == "search":
            result =  await search_agent.ainvoke(state)
        else:
            result = await qa_agent.ainvoke(state)

        state["result"] = result.get("result")
        return state

    @trace_node("can_retry")
    def can_retry(state):
        return (
                not state["success"]
                and state["retry_count"] < state["max_retry"]
        )

    g = StateGraph(dict)
    g.add_node("router",router_node)
    g.add_node("call_agent",call_agent)
    g.add_node("observe",observe)
    g.add_node("judge",judge)
    g.add_node("retry",retry_policy)
    g.add_node("wait",wait)
    g.add_node("human_resume",human_resume)

    g.set_entry_point("router")
    g.add_edge("router","call_agent")
    g.add_edge("call_agent","observe")
    g.add_edge("observe","judge")
    g.add_conditional_edges("judge", lambda s: (
        "wait" if s.get("need_human")
        else "retry" if not s["success"] and s["retry_count"]<s["max_retry"]
        else "final"
    ), {
        "wait":"wait",
        "retry": "retry",
        "final": END
    })
    g.add_edge("retry","call_agent")
    g.add_edge("human_resume","call_agent")

    return g.compile()