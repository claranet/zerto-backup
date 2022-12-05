#! env python3

# ZVM Config Dumper
#
# Create a new Dump and download it
# By Default, the Settings dump is saved as <hostname>_<timestamp>.json in local directory

# Author: Martin Weber <martin.weber@de.clara.net>
# Version: 0.1.0

import argparse
import json
import requests
import urllib3
import urllib
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="Create ZVM Configuratio Dump and download it")
parser.add_argument("--host", default="127.0.0.1", help="Zerto ZVM Hostname", action="store")
parser.add_argument("--username", default="admin", help="ZVM Login Username", action="store")
parser.add_argument("--password", required=True, help="ZVM Login Password", action="store")
parser.add_argument("--output", default=False, help="Define file for output, use '-' for stdout, default file <host>_<timestamp>.json", action="store")
args = parser.parse_args()

ZVM_HOST=args.host

payload = {
    "grant_type": "password",
    "client_id": "zerto-client",
    "username": args.username,
    "password": args.password
}
payload = urllib.parse.urlencode( payload )

#
# Open new API Session
#
resp = requests.post(
      url     = f"https://{ZVM_HOST}/auth/realms/zerto/protocol/openid-connect/token"
    , headers = { "Content-Type": "application/x-www-form-urlencoded" }
    , data    = payload
    , verify  = False
)
if resp.status_code != 200:
    raise Exception(f"Unable to create Zerto API Session - {resp.status_code}")

if not "access_token" in resp.json():
    raise Exception("Cannot find field access_toke in response")

ZVM_TOKEN=resp.json()["access_token"]

# Create Session
zvm_session = requests.Session()
zvm_session.headers = {"Authorization": f"Bearer {ZVM_TOKEN}", "Content-Type": "application/json"}
zvm_session.verify = False

#
# Fetch List of VPGs
#
resp = zvm_session.get( f"https://{ZVM_HOST}/v1/vpgs" )
if resp.status_code != 200:
    raise Exception("Unable to create Zerto API Session")

vpgNames = [x["VpgName"] for x in resp.json()]

#
# Create Export of Sessings
#
payload = json.dumps( { 'vpgNames': vpgNames }  )
resp = zvm_session.post(
      url  = f"https://{ZVM_HOST}/v1/vpgSettings/exportSettings"
    , data = payload
)
if resp.status_code != 200:
    raise Exception("Unable to create Zerto API Session")
if not "TimeStamp" in resp.json():
    raise Exception("Cannot find field 'TimeStamp' in response")

#
# Fetch created Settings
#
resp = zvm_session.post( f"https://{ZVM_HOST}/v1/vpgSettings/exportedSettings/{resp.json()['TimeStamp']}" )
if resp.status_code != 200:
    raise Exception("Unable to create Zerto API Session")

ZVM_SETTINGS=resp.json()["ExportedVpgSettingsApi"]

timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
filename = f"./{args.host}_{timestamp}.json"
if  args.output:
    filename = args.output

if filename == "-":
    print( json.dumps( ZVM_SETTINGS ) )
else:
    with open(filename, "w") as f:
        f.write(json.dumps( ZVM_SETTINGS ))
        f.close()

