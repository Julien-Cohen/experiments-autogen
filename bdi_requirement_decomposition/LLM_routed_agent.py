from abc import ABC

from autogen_core import RoutedAgent


class LLMRoutedAgent(RoutedAgent, ABC):
    llm_role = None
    llm_explicit_directive = None

    def __init__(self, description: str, role:str) -> None:
        super().__init__(description)
        self.llm_role = role