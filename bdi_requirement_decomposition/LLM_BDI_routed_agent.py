from autogen_core.models import SystemMessage, ChatCompletionClient

from bdi_requirement_decomposition.BDI_routed_agent import BDIRoutedAgent


class LLMBDIRoutedAgent(BDIRoutedAgent):

    def __init__(
        self,
        model_client: ChatCompletionClient,
        description: str,
        role: str,
        job_desciption,
    ):
        BDIRoutedAgent.__init__(self, description)
        self.llm_role = role
        self.llm_explicit_directive = None
        self.job_description = job_desciption
        self._system_message = SystemMessage(
            content=(self.llm_role + " " + self.job_description)
        )
        self._model_client = model_client
