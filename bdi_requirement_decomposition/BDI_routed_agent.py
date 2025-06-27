from autogen_core import RoutedAgent

from bdi_requirement_decomposition.BDI_data import BDIData


class BDIRoutedAgent(RoutedAgent, BDIData):

    def __init__(self, description):
        RoutedAgent.__init__(self, description)
        BDIData.__init__(self)

    def __str__(self):
        return "I am: " + self._description + "\n" + BDIData.__str__(self)