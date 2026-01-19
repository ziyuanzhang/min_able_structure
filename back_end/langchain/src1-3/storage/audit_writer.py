import json
import uuid
from datetime import datetime,UTC
from storage.models import AgentRun
from get_env import AUDIT_FILE



def new_run(query:str,role:str)->AgentRun:
    return {
        "run_id":str(uuid.uuid4()),
        "query":query,
        "role":role,
        "events":[]
    }

def record_event(run:AgentRun, node:str, input_data, output_data):
    run["events"].append({
        "ts":datetime.now(UTC).isoformat(),
        "node":node,
        "input":input_data,
        "output":output_data
    })


# ---  新增：万能序列化函数 ---
def safe_serialize(obj):
    """
    当 json.dumps 遇到无法识别的对象时，会调用此函数。
    优先尝试转为字典，实在不行转为字符串。
    """
    # 如果是日期对象，转 ISO 格式
    if isinstance(obj, (datetime, float, int, bool, str)) or obj is None:
        return obj

    # 如果对象有 .model_dump() 方法 (如 Pydantic V2)
    if hasattr(obj, "model_dump") and callable(obj.model_dump):
        return obj.model_dump()

    # 如果对象有 .dict() 方法 (如 Pydantic V1)
    if hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()

    # 如果对象有 .to_dict() 方法 (常见自定义类)
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return obj.to_dict()

    # 如果是普通对象，尝试获取其属性字典
    if hasattr(obj, "__dict__"):
        return obj.__dict__

    # 实在没办法，直接强转字符串，保证不报错
    return str(obj)

def persist(run:AgentRun):
    with open(AUDIT_FILE,"a") as f:
        f.write(json.dumps(run,ensure_ascii=False,default=safe_serialize) + "\n")