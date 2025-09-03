from autogen_core import (
    type_subscription,
    MessageContext,
    TopicId,
    message_handler,
)
from autogen_core.models import UserMessage

from experiment_bdi_requirement_decomposition.example.message import *

from bdi_autogen.llm_bdi_routed_agent import *


@type_subscription(topic_type=cut_request_topic_type)
class RequirementDecomposerAgent(LLMBDIRoutedAgent):

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            model_client=model_client,
            description="Decomposer agent (with LLM).",
            llm_role="You are a decomposer.",
            llm_job_description=(
                "You receive a specification of a system, and a list of atomic requirements about that system."
                " You have to identify exactly one requirements that is related to the received specification and which is not in the list of atomic requirements."
            ),
        )

        self.llm_explicit_directive = (
            "Now please propose a new requirement (exactly one)."
        )
        self.add_desire(
            "Find requirements related to the specifications, that help to complete the list of atomic requirements."
        )

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        await super().handle_message(message, ctx)

    # override
    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)

    # override
    async def bdi_select_intention(self, ctx):
        prompt = (
            f"Initial specification:"
            + self.get_belief_by_tag(spec_tag)
            + " ;"
            + f" List of atomic requirements: "
            + self.get_belief_by_tag(req_list_tag)
            + self.llm_explicit_directive
        )
        llm_result = await self._model_client.create(
            messages=[
                self._system_message,
                UserMessage(content=prompt, source=self.id.key),
            ],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        log_answer(response)
        assert isinstance(response, str)
        self.add_intention("VALIDATION_REQUEST", response)

    # override
    async def bdi_act(self, ctx):
        assert self.has_intention("VALIDATION_REQUEST")
        action = "VALIDATION_REQUEST"
        data = self.get_intention_data("VALIDATION_REQUEST")
        self.remove_intention(action, data)
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=data,
            ),
            topic_id=TopicId(
                correctness_validation_request_topic_type, source=self.id.key
            ),
        )
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=data,
            ),
            topic_id=TopicId(
                non_redundancy_validation_request_topic_type, source=self.id.key
            ),
        )
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=data,
            ),
            topic_id=TopicId(
                satisfiability_validation_request_topic_type, source=self.id.key
            ),
        )
