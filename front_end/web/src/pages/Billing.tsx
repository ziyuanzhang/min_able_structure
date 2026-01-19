// src/pages/Billing.tsx
import { Card, Statistic, Row, Col } from "antd";
import { useEffect, useState } from "react";
import { get } from "../api/client";
import { Table } from "antd";

export default function Billing() {
  const [data, setData] = useState([]);

  const [events, setEvents] = useState([]);

  useEffect(() => {
    get("/billing/summary").then((r) => setData(r.data));
    get("/billing/events").then((r) => setEvents(r.data));
  }, []);

  if (!data) return null;

  return (
    <div>
      {data.map((user) => (
        <Row gutter={16} key={user.tenant_id}>
          <Col span={6}>
            <Card>
              <Statistic title="Agent Runs" value={user.agent_runs} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="Prompt Tokens" value={user.prompt_tokens} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Agent Minutes"
                value={user.agent_minutes.toFixed(2)}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic title="Cost ($)" value={user.cost.toFixed(2)} />
            </Card>
          </Col>
        </Row>
      ))}

      <Table
        columns={[
          { title: "Request", dataIndex: "request_id" },
          { title: "Prompt Tokens", dataIndex: "prompt_tokens" },
          { title: "Completion Tokens", dataIndex: "completion_tokens" },
          { title: "Duration(ms)", dataIndex: "agent_duration_ms" },
          { title: "Time", dataIndex: "created_at" }
        ]}
        dataSource={events}
      />
    </div>
  );
}
