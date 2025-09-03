from autogen_core import RoutedAgent, message_handler

from .bdi_data import *

from abc import abstractmethod


def log(m: str):
    print("[LOG] " + m)


class BDIComponent:
    def __init__(self):
        self.beliefs = Beliefs()
        self.desires = Desires()
        self.intentions = Intentions()

    def add_intention(self, action: str, data: str):
        self.intentions.add(action, data)
        log("Intention updated (" + self._description + ")")
        log(str(self.intentions) + "\n")

    def remove_intention(self, action, data):
        self.intentions.remove_intention(action, data)

    def remove_first_intention(self, action):
        self.intentions.remove_first_intention(action)

    def has_intention(self, tag):
        return self.intentions.has_intention(tag)

    def get_intention_data(self, tag):
        return self.intentions.get_intention_data(tag)

    def add_belief(self, data, tag):
        self.beliefs.add_belief(data, tag)

    def update_belief(self, data, tag):
        self.beliefs.update_belief(data, tag)

    def get_belief_by_tag(self, tag):
        return self.beliefs.get_belief_by_tag(tag)

    def add_desire(self, d):
        self.desires.add(d)

    @abstractmethod
    def bdi_observe_message(self, message): ...

    @abstractmethod
    async def bdi_select_intention(self, ctx): ...

    @abstractmethod
    async def bdi_act(self, ctx): ...

    async def bdi_loop(self, message, ctx):
        """Main BDI agent loop"""
        self.bdi_observe_message(message)
        log(str(self))
        await self.bdi_select_intention(ctx)
        await self.bdi_act(ctx)
