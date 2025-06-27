from autogen_core import RoutedAgent, message_handler

from bdi_requirement_decomposition.bdi_data import BDIData
from bdi_requirement_decomposition.message import bdi_observe_message

from abc import ABC, abstractmethod


def log(m: str):
    print("[LOG] " + m)


class BDIRoutedAgent(RoutedAgent, BDIData):

    def __init__(self, description):
        RoutedAgent.__init__(self, description)
        BDIData.__init__(self)

    def __str__(self):
        return "I am: " + self._description + "\n" + BDIData.__str__(self)

    def set_intention(self, action: str, data: str):
        BDIData.set_intention(self, action, data)
        log("Intention updated (" + self._description + ")")
        log(self.format_intention())

    # @message_handler
    async def handle_message(self, message, ctx):
        self.bdi_observe_message(message)
        self.bdi_select_intention(message)
        self.bdi_act(message)

    @abstractmethod
    def bdi_observe_message(self, message): ...

    @abstractmethod
    def bdi_select_intention(self, message): ...

    @abstractmethod
    def bdi_act(self, message): ...
