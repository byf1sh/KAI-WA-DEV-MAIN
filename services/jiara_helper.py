import requests
import json
from services.opener import openJSON, bodyModified
# from opener import openJSON, bodyModified
from datetime import datetime, timedelta

def get_case_id():
    list_case_id = []
    status = "Recommendation Provided"
    start_time = "startOfDay()" # 2025-05-07 21:45"
    end_time = "endOfDay()" # 2025-05-07 21:45"

    url = "https://soc-agit.atlassian.net/gateway/api/graphql/slow/pq/7f1bc9e7fd0554b827eb92d8de38dc93835b843a1ba4a5c7a18ce65d2b06991b?operation=IssueNavigatorIssueSearchRefetchQuery"
    cookies = openJSON("utils/cookies.json")
    headers = openJSON("utils/headers.json")
    body = bodyModified("utils/body.json",status, start_time, end_time)

    res = requests.post(url, cookies=cookies, headers=headers, json=body)
    jsons = json.dumps(res.json(), indent=4)
    # print(res.status_code)
    data = res.json()
    count = 0
    slice_data = data["data"]["jira"]["jiraIssueSearchView"]["issues"]["edges"]
    for sum in slice_data:
        count += 1
        case_id = {"case_id":sum["fieldSets"]["edges"][0]["node"]["fields"]["edges"][0]["node"]["text"]}
        list_case_id.append(case_id)
        # print(f"{count}. {sum["node"]["summary"]} : {sum["fieldSets"]["edges"][0]["node"]["fields"]["edges"][0]["node"]["text"]}")
    return list_case_id

# a = get_case_id()
# print(a)