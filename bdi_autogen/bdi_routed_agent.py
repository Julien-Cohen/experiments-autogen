from autogen_core import RoutedAgent

from bdi.bdi_component import *


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
            + BDIComponent.__str__(self)
            + "\n"
            + f"{'-' * 80}"
        )

    async def handle_message(self, message, ctx):
        await self.bdi_loop(message, ctx)
