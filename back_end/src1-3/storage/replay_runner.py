from storage.audit_reader import load_by_run_id

def replay(run_id:str):
    run = load_by_run_id(run_id)
    if not run:
        return RuntimeError("Run not found")

    print(f"Replay run_id={run_id}")
    print(f"Query: {run['query']}")
    print("-" * 40)

    for event in run["events"]:
        print(f"[{event['ts']}] NODE={event['node']}")
        print("INPUT:", event["input"])
        print("OUTPUT:", event["output"])
        print(f"Answer: {event['output']['answer'] if 'answer' in event['output'] else '[No answer]'}")
        print("-" * 40)


if __name__ == "__main__":
    replay("1e42a300-675c-43ef-b083-a0fb6463e83a")