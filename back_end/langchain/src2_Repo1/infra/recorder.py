# 事件记录器
import json
from infra.db import conn


def custom_serializer(obj):
    """
    自定义 JSON 序列化器
    用于处理 CallToolResult 等无法直接序列化的对象
    """
    # 1. 尝试 Pydantic v2 (model_dump)
    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    # 2. 尝试 Pydantic v1 (dict)
    if hasattr(obj, "dict"):
        return obj.dict()

    # 3. 尝试普通对象的属性字典 (__dict__)
    if hasattr(obj, "__dict__"):
        return obj.__dict__

    # 4. 最后的兜底：直接转为字符串 (避免报错)
    return str(obj)

def record_event(request_id: str, node_name: str, input_data, output_data):
    """记录事件"""
    conn.execute(
        " INSERT INTO agent_event (request_id, node, input_data, output_data) VALUES (?, ?, ?, ?)",
        (
            request_id,
            node_name,
            json.dumps(input_data,ensure_ascii=False,default=custom_serializer),
            json.dumps(output_data,ensure_ascii=False,default=custom_serializer)
        )
    )
    conn.commit()