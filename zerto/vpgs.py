# pylint: disable=all

def list_vpgs(self):
    resp = self.session.get( f"https://{self.hostname}/v1/vpgs" )
    if resp.status_code != 200:
        raise Exception("Unable to create Zerto API Session")
    data = resp.json()
    return data
