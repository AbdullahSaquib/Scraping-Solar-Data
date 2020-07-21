import requests
import json


class MyHttp:
    def __init__(self, url, login_id, password):
        self.BASE_URL = url
        self.token = None
        self.login_id = login_id
        self.password = password
    
    def get_token(self, login_id, password):
        print("Getting token")
        login_url = self.BASE_URL + "/admin/Admin/login"
        payload = {"login_id":login_id,"password":password}
        payload = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", login_url, headers=headers, data=payload)
        if response.status_code == 200:
            self.token = response.json()['resultObject']['token']

    def send_request(self, endpoint, payload):
        if not self.token:
            self.get_token(self.login_id, self.password)
        if not self.token:
            print("Could not be authenticated !")
            return None
        payload = json.dumps(payload)
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", self.BASE_URL + endpoint, headers=headers, data = payload)
        if response.status_code == 200:
            return response.json()
        return None
