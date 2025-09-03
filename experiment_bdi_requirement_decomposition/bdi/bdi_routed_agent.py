from autogen_core import RoutedAgent, message_handler

from .bdi_component import *

from abc import abstractmethod


class BDIRoutedAgent(RoutedAgent, BDIComponent):

    def __init__(self, description):
        RoutedAgent.__init__(self, description)
        BDIComponent.__init__(self)

    def __str__(self):
        return (
            f"{'-' * 80}\n"
            + "I am: "
            + self._description
            + "\n"
            + str(self.beliefs)
            + "\n"
            + str(self.desires)
            + "\n"
            + str(self.intentions)
            + f"{'-' * 80}"
        )

    async def handle_message(self, message, ctx):
        await self.bdi_loop(message, ctx)
