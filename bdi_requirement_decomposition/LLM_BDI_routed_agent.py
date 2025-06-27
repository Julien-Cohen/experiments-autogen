from abc import ABC

from IPython.core.hooks import deprecated
from autogen_core import RoutedAgent

from bdi_requirement_decomposition.BDI_routed_agent import BDIRoutedAgent


class LLMBDIRoutedAgent(BDIRoutedAgent):
    llm_role = None
    llm_explicit_directive = None

    def __init__(self, description: str, role: str) -> None:
        BDIRoutedAgent.__init__(self, description)
        self.llm_role = role