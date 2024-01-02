class Event():
    sender: str
    target: str
    move: str

    def __init__(self, sender: str, target: str, move: str):
        self.sender = sender
        self.target = target
        self.move = move
