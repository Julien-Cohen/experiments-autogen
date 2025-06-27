from autogen_core import RoutedAgent, message_handler

from bdi_requirement_decomposition.bdi_data import *

from abc import abstractmethod


def log(m: str):
    print("[LOG] " + m)


class BDIRoutedAgent(RoutedAgent):

    def __init__(self, description):
        RoutedAgent.__init__(self, description)
        self.beliefs = Beliefs()
        self.desires = Desires()
        self.intention = Intention()

    def __str__(self):
        return (
            "I am: "
            + self._description
            + "\n"
            + str(self.beliefs)
            + "\n"
            + str(self.desires)
            + "\n"
            + str(self.intention)
        )

    def set_intention(self, action: str, data: str):
        self.intention.set(action, data)
        log("Intention updated (" + self._description + ")")
        log(str(self.intention))

    def get_intention_action(self):
        return self.intention.get_action()

    def get_intention_data(self):
        return self.intention.get_data()

    def add_belief(self, data, tag):
        self.beliefs.add_belief(data, tag)

    def update_belief(self, data, tag):
        self.beliefs.update_belief(data, tag)

    def get_belief_by_tag(self, tag):
        return self.beliefs.get_belief_by_tag(tag)

    def add_desire(self, d):
        self.desires.add(d)

    # @message_handler
    async def handle_message(self, message, ctx):
        self.bdi_observe_message(message)
        self.bdi_select_intention(ctx)
        self.bdi_act(ctx)

    @abstractmethod
    def bdi_observe_message(self, message): ...

    @abstractmethod
    def bdi_select_intention(self, ctx): ...

    @abstractmethod
    def bdi_act(self, ctx): ...
