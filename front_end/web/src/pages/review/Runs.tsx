import { get } from "../../api/client.ts";
import { Button, Table } from "antd";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router";

export default function Runs() {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    get("/agent/runs").then((r) => setData(r.data));
  }, []);
  return (
    <Table
      rowKey="request_id"
      columns={[
        { title: "Request ID", dataIndex: "request_id" },
        { title: "Time", dataIndex: "ts" },
        {
          title: "操作",
          dataIndex: "active",
          render: (_, r) => (
            <div>
              <Button onClick={() => navigate(`/runDetail/${r.request_id}`)}>
                详情
              </Button>
              <Button onClick={() => navigate(`/workflow/${r.request_id}`)}>
                流程
              </Button>
            </div>
          )
        }
      ]}
      dataSource={data}
    />
  );
}
