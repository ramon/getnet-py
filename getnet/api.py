class API:
    client_id: str = None
    client_secret: str = None

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
