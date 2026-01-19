import { Button } from "antd";
import { useEffect, useState } from "react";
import { get, post } from "../../api/client";
import { TraceTimeline } from "../../components/TraceTimeline";
import { useParams } from "react-router-dom";

export default function RunDetail() {
  const { requestId } = useParams();

  const [events, setEvents] = useState([]);

  useEffect(() => {
    get(`/agent/run/${requestId}`).then((r) => setEvents(r.data));
  }, []);

  return (
    <>
      <Button onClick={() => post(`/agent/replay/${requestId}`)}>Replay</Button>
      <p style={{ marginBottom: "20px" }}></p>
      <TraceTimeline events={events} />
    </>
  );
}
