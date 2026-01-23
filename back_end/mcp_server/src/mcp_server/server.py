from fastmcp import FastMCP
from ragflow_sdk import RAGFlow

from mcp_server.get_env import get_env
import requests

mcp = FastMCP("rag-tools")

# 延迟初始化 RAGFlow
_rag_object = None


def get_rag():
    global _rag_object
    if _rag_object is None:
        if not get_env.RAGFLOW_API_KEY:
            raise ValueError("RAGFLOW_API_KEY is missing")
        if not get_env.RAGFLOW_URL:
            raise ValueError("RAGFLOW_URL is missing")
        # 确保去除 URL 尾部的斜杠
        base_url = get_env.RAGFLOW_URL.rstrip('/')
        _rag_object = RAGFlow(api_key=get_env.RAGFLOW_API_KEY, base_url=base_url)
    return _rag_object


@mcp.tool(name="ragflow.search")
def ragflow_search(query: str, top_k: int = 5) -> str:
    """
    在 RagFlow 的所有知识库中检索相关内容。
    """
    try:
        rag = get_rag()
        # -------------------------------------------------------------
        # 1. 获取所有知识库列表 (SDK 方式)
        # -------------------------------------------------------------
        try:
            datasets = rag.list_datasets(id=RAGFLOW_KNOWLEDGE_BASE_ID,page=1, page_size=100)
        except Exception as e:
            return f"Error listing datasets: {str(e)}"

        if not datasets:
            return "No knowledge bases available."
        # -------------------------------------------------------------
        # 2. 提取所有知识库 ID
        # -------------------------------------------------------------
        all_dataset_ids = []

        # 兼容处理：datasets 可能是字典(旧版)或列表(新版)
        ds_list = []
        if isinstance(datasets, list):
            ds_list = datasets
        elif isinstance(datasets, dict) and 'data' in datasets:
            ds_list = datasets['data']

        for ds in ds_list:
            # 兼容对象属性 (.id) 和 字典键 (['id'])
            ds_id = None
            if isinstance(ds, dict):
                ds_id = ds.get('id')
            else:
                ds_id = getattr(ds, 'id', None)

            if ds_id:
                all_dataset_ids.append(ds_id)

        if not all_dataset_ids:
            return "No valid dataset IDs found."

        print(f"======Searching query '{query}' across {len(all_dataset_ids)} datasets...")
        print(f"======Target IDs: {all_dataset_ids}")
        # -------------------------------------------------------------
        # 3. 执行聚合检索 (Requests 方式 - 稳定方案)
        # -------------------------------------------------------------
        # 构造 URL
        base_url = RAGFLOW_URL.rstrip('/')
        if '/api/v1' not in base_url:
            base_url += '/api/v1'
        retrieval_url = f"{base_url}/retrieval"

        headers = {
            "Authorization": f"Bearer {RAGFLOW_API_KEY}",
            "Content-Type": "application/json"
        }

        # 构造符合 API 文档的 Payload
        payload = {
            "question": query,
            "dataset_ids": all_dataset_ids,
            "page": 1,
            "page_size": top_k,  # 这里将 top_k 映射为 page_size
            "similarity_threshold": 0.2,
            "rerank_id": ""  # 可选，如果有重排模型ID可填入
        }

        try:
            resp = requests.post(retrieval_url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            res_json = resp.json()
            print("=======RAG Flow:", res_json)
        except Exception as http_e:
            return f"HTTP Retrieval failed: {http_e}"

        # -------------------------------------------------------------
        # 4. 解析结果
        # -------------------------------------------------------------
        if res_json.get('code') != 0:
            return f"Server Error: {res_json.get('message')}"

        retrieved_chunks = res_json.get('data', [])
        unique_contents = []
        seen = set()

        for chunk in retrieved_chunks["chunks"]:
            # 获取内容，API 返回的字段通常是 content_with_weight
            # print("chunk:",type(chunk),chunk)
            content = chunk.get('content_with_weight') or chunk.get('content') or ""

            # 清理空白符
            content = content.strip()

            if content and content not in seen:
                seen.add(content)
                unique_contents.append(content)

        if not unique_contents:
            return "No relevant content found."

        print(f"=====Found {len(unique_contents)} unique results.")
        # 返回结果
        return "\n---\n".join(unique_contents[:top_k])

    except Exception as e:
        print(f"=======ragflow_search exception: {e}")
        import traceback
        traceback.print_exc()
        return f"======RAG search error: {type(e).__name__}: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000)