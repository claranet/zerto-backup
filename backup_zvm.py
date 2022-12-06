#! env python3

# ZVM Config Dumper
#
# Create a new Dump and download it
# By Default, the Settings dump is saved as <hostname>_<timestamp>.json in local directory

# Author: Martin Weber <martin.weber@de.clara.net>
# Version: 0.1.0

import argparse
import json
from datetime import datetime

from zerto import Zerto

parser = argparse.ArgumentParser(description="Create ZVM Configuratio Dump and download it")
parser.add_argument("--host", default="127.0.0.1", help="Zerto ZVM Hostname", action="store")
parser.add_argument("--username", default="admin", help="ZVM Login Username", action="store")
parser.add_argument("--password", required=True, help="ZVM Login Password", action="store")
parser.add_argument("--output", default=False, help="Define file for output, use '-' for stdout, default file <host>_<timestamp>.json", action="store")
args = parser.parse_args()

zerto = Zerto(args.host, args.username, args.password)
zerto.connect()

#
# Create Export of Sessings
#
vpgs = zerto.list_vpgs()
backup = zerto.create_backup( [x["VpgName"] for x in vpgs] )
#
# Fetch created Settings
#
data = zerto.fetch_backup(backup["TimeStamp"])
ZVM_SETTINGS=data["ExportedVpgSettingsApi"]

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

