import json
from get_env import AUDIT_FILE

def load_all():
    with open(AUDIT_FILE) as f:
        for line in f:
            yield json.loads(line)


def load_by_run_id(run_id:str):
    for run in load_all():
        if run["run_id"] == run_id:
            return run
    return None