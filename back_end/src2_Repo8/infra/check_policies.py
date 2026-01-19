from infra.db import conn

def check_policies(context):
    policies = conn.fetch_all("""
      SELECT * FROM policy
      WHERE tenant_id=? AND enabled=1
    """, (context["tenant_id"],))

    for p in policies:
        if p["type"] == "input":
            if context["prompt_tokens"] > p["rule"]["max_tokens"]:
                return policy_action(p)

    return "ok"

def policy_action(policy):
    if policy["action"] == "block":
        raise Exception("PolicyBlocked")

    if policy["action"] == "retry":
        return {"retry": True}

    # if policy["action"] == "warn":
    #     log_warning(policy)
    #
    # if policy["action"] == "escalate":
    #     create_human_task(policy)