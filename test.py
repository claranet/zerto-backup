

# # MenuItem is the base class for all items, it doesn't do anything when selected
# menu_item = MenuItem("Menu Item")

# # A FunctionItem runs a Python function when selected
# function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# # A CommandItem runs a console command
# command_item = CommandItem("Run a console command",  "touch hello.txt")

# # A SelectionMenu constructs a menu from a list of strings
# selection_menu = SelectionMenu(["item1", "item2", "item3"])

# # A SubmenuItem lets you add a menu (the selection_menu above, for example)
# # as a submenu of another menu
# submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# # Once we're done creating them, we just add the items to the menu
# menu.append_item(menu_item)
# menu.append_item(function_item)
# menu.append_item(command_item)
# menu.append_item(submenu_item)

# # Finally, we call show to show the menu and allow the user to interact
# menu.show()

from zerto import Zerto
import argparse
import json
from consolemenu import *
from consolemenu.items import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="Create ZVM Configuratio Dump and download it")
parser.add_argument("--host", default="127.0.0.1", help="Zerto ZVM Hostname", action="store")
parser.add_argument("--username", default="admin", help="ZVM Login Username", action="store")
parser.add_argument("--password", help="ZVM Login Password", action="store")
parser.add_argument("--file", required=True, action="store")
args = parser.parse_args()

def get_file_identifier(file):
    sites = []
    with open(file) as f:
        data = json.loads( f.read() )

        for _vpg in data:
            if not [x for x in sites if x["id"] == _vpg["Basic"]["ProtectedSiteIdentifier"] ]:
                sites.append({
                    "name": _vpg["SourceSiteName"],
                    "id":   _vpg["Basic"]["ProtectedSiteIdentifier"]
                })
            if not [x for x in sites if x["id"] == _vpg["Basic"]["RecoverySiteIdentifier"] ]:
                sites.append({
                    "name": _vpg["TargetSiteName"],
                    "id":   _vpg["Basic"]["RecoverySiteIdentifier"] 
                })

        f.close()

    return sites

def get_remote_identifier(host, username, password):
    zerto = Zerto(host, username, password)
    zerto.connect()

    sites = []
    sites.append({
        "name": zerto.local_site()["SiteName"],
        "id":   zerto.local_site()["SiteIdentifier"]
    })
    for _site in zerto.peer_sites():
        sites.append({
            "name": _site["PeerSiteName"],
            "id":   _site["SiteIdentifier"]
        })
    return sites

    # print(z.peer_sites())


current_sites = get_remote_identifier(args.host, args.username, args.password)
old_sites = get_file_identifier(args.file)

# print(json.dumps(sites))
def test(name, id):
    print(name, id)

submenus = []
for x in current_sites:
    item = FunctionItem(f"{x['name']} ({x['id']})", test, kwargs=x)
    item = SubmenuItem()


menu = ConsoleMenu("Change Zerto Site Identifier", "Select ID to Change")
for x in old_sites:
    menu.append_item( item )

menu.show()
