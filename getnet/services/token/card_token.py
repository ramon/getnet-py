class CardToken:
    number_token: str

    def __init__(self, number_token: str):
        self.number_token = number_token

    def __str__(self):
        return self.number_token

    def __eq__(self, other):
        return self.number_token == other.number_token
