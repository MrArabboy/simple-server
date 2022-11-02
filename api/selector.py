import json

from api.client import alarm_server_client as client


def get_all_incoming_alarms():
    alarms = client.alarms(offset=0, limit=100)
    total_alarms = alarms["total"]
    alarms["itemSize"] = total_alarms
    required_num_of_request = total_alarms // 100

    for page_num in range(1, required_num_of_request + 1):
        alarms_in_next_page = client.alarms(offset=page_num * 100, limit=100)
        alarms["items"].extend(alarms_in_next_page["items"])

    return json.dumps(alarms)
