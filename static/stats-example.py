# Example script to get the number of users created today.
import requests
from requests.auth import HTTPBasicAuth
JFA_GO_HOST="http://localhost:8056"
JFA_GO_USERNAME="stats"
JFA_GO_PASSWORD="aSecureStatsAccountPassword"
JFA_GO_TOKEN = ""
JFA_GO_REFRESH_TOKEN = ""

# Logs in with username and password, and sets JFA_GO_TOKEN, which lasts 20 minutes and JFA_GO_REFRESH_TOKEN, which lasts 1 day.
def firstLogin():
    global JFA_GO_TOKEN, JFA_GO_REFRESH_TOKEN
    basic = HTTPBasicAuth(JFA_GO_USERNAME, JFA_GO_PASSWORD)
    resp = requests.get(JFA_GO_HOST+"/token/login", auth=basic)
    JFA_GO_TOKEN = resp.json()["token"]
    JFA_GO_REFRESH_TOKEN = resp.cookies.get("refresh")
    # print(f"Logged in with user/pass, got token {JFA_GO_TOKEN}, refresh {JFA_GO_REFRESH_TOKEN}")

# Logs in with JFA_GO_REFRESH_TOKEN, and sets a new JFA_GO_TOKEN and JFA_GO_REFRESH_TOKEN.
def loginWithRefresh():
    global JFA_GO_TOKEN, JFA_GO_REFRESH_TOKEN
    resp = requests.get(JFA_GO_HOST+"/token/refresh", cookies={"refresh": JFA_GO_REFRESH_TOKEN})
    JFA_GO_TOKEN = resp.json()["token"]
    JFA_GO_REFRESH_TOKEN = resp.cookies.get("refresh")
    # print(f"Logged in with refresh cookie, got token {JFA_GO_TOKEN}, refresh {JFA_GO_REFRESH_TOKEN}")

def countAccountsMadeToday():
    data = {
      "searchTerms": [],
      "queries": [
        {
          "field": "time",
          "operator": "<",
          "class": "date",
          "value": {
            "year": 2025,
            "month": 10,
            "day": 23,
            "hour": 23,
            "minute": 59,
            "offsetMinutesFromUTC": 0
          }
        },
        {
          "field": "time",
          "operator": ">",
          "class": "date",
          "value": {
            "year": 2025,
            "month": 10,
            "day": 22,
            "hour": 23,
            "minute": 59,
            "offsetMinutesFromUTC": 0
          }
        },
        {
          "field": "accountCreation",
          "operator": "=",
          "class": "bool",
          "value": True
        }
      ],
      "limit": 20,
      "page": 0,
      "sortByField": "time",
      "ascending": False
    }

    resp = requests.post(JFA_GO_HOST+"/activity/count", json=data, headers={"Authorization": "Bearer "+JFA_GO_TOKEN})
    if resp.status_code != 200:
        # Re-log (maybe our token has expired?)
        loginWithRefresh()
        resp = requests.post(JFA_GO_HOST+"/activity/count", json=data, headers={"Authorization": "Bearer "+JFA_GO_TOKEN})
    if resp.status_code == 200:
        print("Got count matching:", resp.json()["count"])
    else:
        print("Failed:", resp)

if __name__ == "__main__":
    firstLogin()
    countAccountsMadeToday()
