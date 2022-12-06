# pylint: disable=all

import urllib
import requests

def connect(self):
    resp = requests.post( f"https://{self.hostname}/v1/session/add", verify=False )

    if(resp.status_code == 404):
        return self._connect_linux_zvm()
    else:
        return self._connect_windows_zvm()
    
def _connect_windows_zvm(self):
    #
    # Open new API Session
    #
    resp = requests.post(
          url     = f"https://{self.hostname}/v1/session/add"
        , auth    = (self.username, self.password)
        , verify  = False
    )
    if resp.status_code != 200:
        raise Exception(f"Unable to create Zerto API Session - {resp.status_code}")

    self.sessionToken = resp.headers["x-zerto-session"]
    
    self.session = requests.Session()
    self.session.headers = { "x-zerto-session": resp.headers["x-zerto-session"]
                           , "Content-Type": "application/json" }
    self.session.verify = False

    return True

def _connect_linux_zvm(self):
    payload = {
        "grant_type": "password",
        "client_id":  "zerto-client",
        "username":   self.username,
        "password":   self.password
    }
    payload = urllib.parse.urlencode( payload )

    #
    # Open new API Session
    #
    resp = requests.post(
          url     = f"https://{self.hostname}/auth/realms/zerto/protocol/openid-connect/token"
        , headers = { "Content-Type": "application/x-www-form-urlencoded" }
        , data    = payload
        , verify  = False
    )

    if resp.status_code != 200:
        raise Exception(f"Unable to create Zerto API Session - {resp.status_code}")

    if not "access_token" in resp.json():
        raise Exception("Cannot find field access_toke in response")
    
    data = resp.json()
    self.sessionToken = data["access_token"]
    
    self.session = requests.Session()
    self.session.headers = { "Authorization": f"Bearer {data['access_token']}"
                           , "Content-Type": "application/json" }
    self.session.verify = False

    return True

