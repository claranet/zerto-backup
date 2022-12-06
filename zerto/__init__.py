# pylint: disable=all

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Zerto(object):
    hostname = ""
    username = ""
    password = ""
    sessionToken = None
    session = None

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    from .session import connect

    from .settings import create_backup, fetch_backup

    from .vpgs import list_vpgs
    
    from .sites import local_site, peer_sites
