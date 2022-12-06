
def peer_sites(self):
    resp = self.session.get( f"https://{self.hostname}/v1/peersites" )
    data = resp.json()
    return data

def local_site(self):
    resp = self.session.get( f"https://{self.hostname}/v1/localsite" )
    data = resp.json()
    return data
