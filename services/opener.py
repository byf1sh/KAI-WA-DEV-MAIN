import json
from datetime import datetime, timedelta

def get_time():
    now = datetime.now()
    time_minus = now - timedelta(minutes=10)
    time_now = now.strftime("%Y-%m-%d %H:%M")
    time_minus_10_minutes = time_minus.strftime("%Y-%m-%d %H:%M")
    return time_now, time_minus_10_minutes

def openJSON(file):
    with open(file,"r") as f:
        data = json.load(f)
    return data

def bodyModified(file, status, start_time, end_time):
    with open(file,"r") as f:
        data = json.load(f)
    JQL = f"project = SOC\nAND organizations = \"PT Kereta Api Indonesia (Persero)\"\nAND \"Request Type\" = \"MSE - Event Detection (2) (SOC)\"\nAND created >= {start_time}\nAND created <= {end_time}\nAND status = \"{status}\"\nORDER BY created DESC, status ASC, key DESC"
    data["variables"]["issueSearchInput"]["jql"] = JQL
    return data

# A = bodyModified("body.json")
# print(json.dumps(A,indent=2))