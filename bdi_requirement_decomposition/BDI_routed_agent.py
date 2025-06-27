from autogen_core import RoutedAgent

from bdi_requirement_decomposition.BDI_data import BDIData


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
