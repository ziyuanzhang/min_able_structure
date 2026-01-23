import functools
import inspect
import uuid
from infra.recorder import record_event

def trace_node(node_name):
    """
    记录节点调用
    """
    def decorator(fn):
        if inspect.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def wrapper(state):
                request_id = state.get("request_id")
                if not request_id:
                    request_id = str(uuid.uuid4())
                    state["request_id"] = request_id
                record_event(request_id,node_name,"start",state,None)
                new_state = await fn(state)
                record_event(request_id,node_name,"success",None,new_state)
                return new_state
            return wrapper
        else:
            @functools.wraps(fn)
            def wrapper(state):
                request_id = state.get("request_id")
                if not request_id:
                    request_id = str(uuid.uuid4())
                    state["request_id"] = request_id
                record_event(request_id,node_name,"start",state,None)
                new_state = fn(state)
                record_event(request_id,node_name,"success",None,new_state)
                return new_state
            return wrapper
    return decorator