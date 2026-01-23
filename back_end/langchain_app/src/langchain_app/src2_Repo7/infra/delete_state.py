from infra.db import conn


def delete_state_by_id(request_id):
    try:
        cursor = conn.execute(
            "DELETE FROM agent_state WHERE request_id = ?",
            (request_id,)
        )
        conn.commit()  # 别忘了 commit

        return cursor.rowcount > 0  # 返回 True 表示删除成功，False 表示没这条数据

    except Exception as e:
        print(f"Delete Error: {e}")
        return False