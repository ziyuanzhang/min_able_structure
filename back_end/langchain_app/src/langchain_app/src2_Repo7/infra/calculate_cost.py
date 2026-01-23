from infra.db import conn
from types import SimpleNamespace
from datetime import datetime

# ==========================================
# 1. 定义定价策略配置 (Pricing)
# ==========================================
class PricingConfig:
    def __init__(self, tenant_id):
        # 在实际业务中，这里应该从数据库读取该租户的套餐配置
        # 这里为了演示，返回固定单价
        self.price_per_run = 0.01           # 每次运行 0.01 元
        self.price_per_1k_prompt = 0.002    # 输入每 1k token 0.002 元
        self.price_per_1k_completion = 0.005 # 输出每 1k token 0.005 元
        self.price_per_agent_minute = 0.10   # 机器耗时每分钟 0.10 元


# ==========================================
# 2. 核心：计算并更新金额 (Python 逻辑)
# ==========================================
def calculate_cost(tenant_id, month):
    """
    根据 usage_monthly 中的用量，结合定价策略算出 cost，并回写数据库
    """
    cursor = conn.cursor()

    # A. 获取刚刚聚合好的用量数据
    row = cursor.execute(
        "SELECT * FROM usage_monthly WHERE tenant_id=? AND month=?",
        (tenant_id, month)
    ).fetchone()

    if not row:
        print(f"No usage found for {tenant_id} in {month}")
        return

    # B. 将数据库行转换为对象，以支持 usage.field 这种点号写法
    # 这里使用 SimpleNamespace，它允许创建一个带有属性的简单对象
    usage = SimpleNamespace(**dict(row))

    # C. 获取该租户的定价配置
    pricing = PricingConfig(tenant_id)

    # D. 业务逻辑计算 (直接复用你提供的公式)
    cost = (
            usage.agent_runs * pricing.price_per_run +
            (usage.prompt_tokens / 1000.0) * pricing.price_per_1k_prompt +
            (usage.completion_tokens / 1000.0) * pricing.price_per_1k_completion +
            usage.agent_minutes * pricing.price_per_agent_minute
    )

    # 保留 4 位小数，防止精度问题
    cost = round(cost, 4)

    # E. 回写数据库
    cursor.execute(
        "UPDATE usage_monthly SET cost=? WHERE tenant_id=? AND month=?",
        (cost, tenant_id, month)
    )
    conn.commit()

    print(f"Update Success: Tenant [{tenant_id}] Month [{month}] Cost = {cost}")


# ==========================================
# 3. 触发器：先聚合数据，再计算金额
# ==========================================
def sync_usage_data():
    """
    这是定时任务的主入口
    """
    print("Step 1: Aggregating logs to monthly table...")

    # 执行你提供的 SQL (聚合 + Upsert)
    # 注意：这里使用 parameters=() 主要是为了安全，虽然这段 SQL 没有外部参数
    sql_aggregate = """
    INSERT INTO usage_monthly (
        tenant_id, month, agent_runs, prompt_tokens, 
        completion_tokens, agent_minutes, cost
    )
    SELECT
      tenant_id,
      strftime('%Y-%m', created_at) as month,
      COUNT(*) as agent_runs,
      SUM(prompt_tokens),
      SUM(completion_tokens),
      SUM(agent_duration_ms) / 60000.0 as agent_minutes,
      0 as cost
    FROM usage_event
    GROUP BY tenant_id, month
    ON CONFLICT (tenant_id, month) DO UPDATE SET
      agent_runs=excluded.agent_runs,
      prompt_tokens=excluded.prompt_tokens,
      completion_tokens=excluded.completion_tokens,
      agent_minutes=excluded.agent_minutes;
    """

    try:
        conn.execute(sql_aggregate)
        conn.commit()
    except Exception as e:
        print(f"Aggregation failed: {e}")
        return

    # Step 2: 找出所有受影响的 (tenant_id, month) 进行重算
    # 在真实高并发场景下，你应该在 Step 1 记录下变更了哪些 ID，
    # 这里为了简单，我们重新扫描 usage_monthly 中所有记录进行计算
    rows = conn.execute("SELECT tenant_id, month FROM usage_monthly").fetchall()

    print(f"Step 2: Recalculating costs for {len(rows)} records...")
    for r in rows:
        calculate_cost(r["tenant_id"], r["month"])
