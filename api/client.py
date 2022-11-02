import json
import requests
from urllib3.exceptions import InsecureRequestWarning

import env
from api.exceptions import NotAuthorizedError
from api.decorator import auth_required

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class Client(SingletonClass):
    AUTH_URL = f"{env.BASE_URL}/service/session"
    ALARM_URL = f"{env.BASE_URL}/service/sites/4375077F/alarms/activeAlarms"
    AUTH_TOKEN = None

    def __init__(self):
        self.auth()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    @auth_required
    def send_command(self, url, payload={}, header={}):
        response = requests.post(url=url, headers=header, data=payload, verify=False)
        if url == self.AUTH_URL:
            self.AUTH_TOKEN = response.headers.get("X-Auth-Token")
        elif response.status_code == 401:
            raise NotAuthorizedError()
        return response.json()

    def auth(self):
        return self.send_command(
            url=self.AUTH_URL, header=self.header(url=self.AUTH_URL)
        )

    def alarms(self, offset=0, limit=100):
        payload = {
            "offset": offset,
            "limit": limit,
            "viewId": 4,
            "order": ["occurtime ASC"],
            "alarmLevel": ["1", "2"],
            "clearStopTime": "0",
        }
        return self.send_command(
            url=self.ALARM_URL, payload=json.dumps(payload), header=self.header()
        )

    def header(self, url=""):  # sourcery skip: dict-assign-update-to-union
        header = {
            "Accept": "application/json;version=v6.1",
            "Content-Type": "application/json",
            "Accept-Language": "en_US",
        }
        if url == self.AUTH_URL:
            header.update(
                {
                    "X-Auth-User": env.USERNAME,
                    "X-Auth-Key": env.PASSWORD,
                    "X-Auth-UserType": "0",
                    "X-Auth-AuthType": "0",
                    "X-ENCRIPT-ALGORITHM": "1",
                }
            )
        else:
            header["X-Auth-Token"] = self.AUTH_TOKEN
        return header


alarm_server_client = Client()
