# Simple in-memory conversation memory for the hackathon agent

class MemoryStore:
    def __init__(self):
        self.history = []

    def add(self, user, message):
        self.history.append((user, message))

    def get_history(self, user=None):
        if user:
            return [f"{u}: {msg}" for u, msg in self.history if u == user]
        return [f"{u}: {msg}" for u, msg in self.history]
