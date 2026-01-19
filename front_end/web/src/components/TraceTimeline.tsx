import { Timeline, Card } from "antd";

export function TraceTimeline({ events }) {
  return (
    <Timeline>
      {events.map((e, i) => (
        <Timeline.Item key={i}>
          <Card title={`${e.node} - id:${e.id}`}>
            <pre>{JSON.stringify(e.output_data, null, 2)}</pre>
          </Card>
        </Timeline.Item>
      ))}
    </Timeline>
  );
}
