# pylint: disable=all

import json

def create_backup(self, vpg_names):
    
    resp = self.session.post(
      url  = f"https://{self.hostname}/v1/vpgSettings/exportSettings"
    , data = json.dumps( { 'vpgNames': vpg_names }  )
    )

    if resp.status_code != 200:
        raise Exception("Unable to create Zerto API Session")
    data = resp.json()

    if not "TimeStamp" in data:
        raise Exception("Cannot find field 'TimeStamp' in response")

    return data

def fetch_backup(self, timestamp):
    resp = self.session.post( f"https://{self.hostname}/v1/vpgSettings/exportedSettings/{timestamp}" )
    if resp.status_code != 200:
        raise Exception("Unable to create Zerto API Session")
    data = resp.json()
    return data
