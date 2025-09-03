from autogen_core.models import SystemMessage, ChatCompletionClient

from experiment_bdi_requirement_decomposition.bdi_autogen.bdi_routed_agent import *


def log_answer(answer):
    log("[LLM ANSWER]")
    log(f"{'=' * 80}")
    log(answer)
    log(f"{'=' * 80}\n")


class LLMBDIRoutedAgent(BDIRoutedAgent):

    def __init__(
        self,
        model_client: ChatCompletionClient,
        description: str,
        llm_role: str,
        llm_job_description,
    ):
        BDIRoutedAgent.__init__(self, description)
        self.llm_role = llm_role
        self.llm_explicit_directive = None
        self.llm_job_description = llm_job_description
        self._system_message = SystemMessage(
            content=(self.llm_role + " " + self.llm_job_description)
        )
        self._model_client = model_client
