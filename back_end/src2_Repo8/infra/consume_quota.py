from infra.db import conn

def consume_quota(tenant_id):
    conn.execute("UPDATE quota SET used_requests = used_requests + 1 WHERE tenant_id=?",(tenant_id,))
    conn.commit()