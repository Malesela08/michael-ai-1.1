import json


class BlackBoxBus:
    def __init__(self):
        self._secure_channel = {}

    def transmit(self, sender, receiver, payload):
        # Data is encrypted conceptually by isolating it here
        self._secure_channel[receiver] = {"sender": sender, "data": payload}
        return f"Transmission complete: {sender} -> {receiver}"

    def receive(self, participant):
        return self._secure_channel.get(participant, "No secure packets.")
