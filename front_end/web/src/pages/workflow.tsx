import { ReactFlow } from "@xyflow/react";

import "@xyflow/react/dist/style.css";
import { useEffect, useState, useMemo } from "react";
import { get } from "../api/client";
import { useParams } from "react-router-dom";

const initialNodes = [
  { id: "1", position: { x: 0, y: 0 }, data: { label: "1" } },
  { id: "2", position: { x: 0, y: 100 }, data: { label: "2" } }
];
const initialEdges = [{ id: "e1-2", source: "1", target: "2" }];

export default function App() {
  const { requestId } = useParams();
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);
  const getList = () => {
    get(`/graph/run/${requestId}`).then((res) => {
      const nodeList = [];
      const edgeList = [];
      const Arr = res.data; // 确保这是数组！
      res.data.forEach((item, index) => {
        nodeList.push({
          id: String(item.id),
          // 简单的自动布局逻辑 (实际项目中可能需要 dagre 或 elkjs 算法)
          position: { x: 100, y: index * 100 },
          data: {
            label: item.node
          },
          type: "default", // 或自定义节点类型
          style: {
            border: "1px solid #777",
            padding: 10,
            background: item.node === "router_node" ? "#00ff00" : "#ffffff"
          }
        });
        if (index < res.data.length - 1) {
          edgeList.push({
            id: `e-${index}`,
            source: String(item.id),
            target: String(Arr[index + 1].id),
            // label: schemaEdge.node,
            animated: true // 举例：加个动画
          });
        }
      });
      console.log("nodeList:", nodeList);
      console.log("edgeList:", edgeList);
      setNodes(nodeList);
      setEdges(edgeList);
    });
  };

  useEffect(() => {
    getList();
  }, []);

  return (
    <div style={{ height: "1000px" }}>
      <ReactFlow nodes={nodes} edges={edges} fitView />
    </div>
  );
}
