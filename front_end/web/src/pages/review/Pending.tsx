// src/pages/Pending.tsx
import { Button, Card } from "antd";
import { useEffect, useState } from "react";
import { get, post } from "../../api/client";

export default function Pending() {
  const [tasks, setTasks] = useState([]);

  const getList = () => {
    get("/agent/pending").then((r) => setTasks(r.data));
  };
  const handleBtn = (request_id: string, action: string) => {
    post(`/agent/human/${request_id}`, { action: action }).then((res) => {
      if (res.code == "200") getList();
    });
  };
  useEffect(() => {
    getList();
  }, []);

  return (
    <>
      {tasks.map((t) => (
        <Card key={t.request_id} title={t.request_id}>
          <Button onClick={() => handleBtn(t.request_id, "approve")}>
            Approve
          </Button>

          <Button danger onClick={() => handleBtn(t.request_id, "reject")}>
            Reject
          </Button>
        </Card>
      ))}
    </>
  );
}
