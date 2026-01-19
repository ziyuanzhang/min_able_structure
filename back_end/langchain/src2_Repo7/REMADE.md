curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"input":"LangGraph 是什么"}'


curl -X POST http://localhost:8000/agent/replay/<request_id>

curl -X POST http://localhost:8000/agent/human/<request_id>
curl -X POST http://localhost:8000/agent/human/125cca1d-7ea3-4c37-a5d1-6778ca89a242