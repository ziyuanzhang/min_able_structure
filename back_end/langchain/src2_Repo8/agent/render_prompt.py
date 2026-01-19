from infra.db import conn

def render_prompt(prompt_name: str, variables: dict, tenant_id: str):
    prompt = conn.fetch_one("""
      SELECT content FROM prompt_template
      WHERE tenant_id=? AND name=? AND status='active'
      ORDER BY version DESC
      LIMIT 1
    """, (tenant_id, prompt_name))

    if not prompt:
        raise ValueError(f"Prompt template '{prompt_name}' not found for tenant '{tenant_id}'")

    try:
        return prompt["content"].format(**variables)
    except KeyError as e:
        missing_key = e.args[0]
        raise ValueError(f"Missing variable in prompt template: '{missing_key}'")