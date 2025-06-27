from autogen_core import (
    type_subscription,
    message_handler,
    MessageContext,
    TopicId,
)
from autogen_core.models import UserMessage

from message import *

from LLM_BDI_routed_agent import *


@type_subscription(topic_type=validation_request_topic_type)
class RequirementValidatorAgent(LLMBDIRoutedAgent):

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            model_client=model_client,
            description="Requirement Validator agent (with LLM).",
            llm_role="You are a requirement validator.",
            llm_job_description=(
                "Given an initial specification of a system, a list of atomic requirements for that system, and a new atomic requirement,"
                " validate that this new requirement is correct with respect to the initial specification, is not redundant with the atomic requirements already listed, and is not contradictory with the atomic requirements already listed."
                " Start your answer with CORRECT if you validate."
                " Start your answer with INCORRECT otherwise, and explain in your answer why it is not valid."
            ),
        )

        self.llm_explicit_directive = "Do you validate this?"

        self.desire.append("Ensure that the new requirement is correct.")
        self.desire.append(
            "Ensure that the new requirement is not already taken into account."
        )

    @message_handler
    async def handle_options(self, message: Message, ctx: MessageContext) -> None:
        bdi_observe_message(self, message)
        candidate = message.atomic_requirement_tentative
        self.set_intention(
            "Consult an LLM to analyse the tentative requirement.", candidate
        )

        the_list = (
            self.get_belief_by_tag(req_list_tag)
            if self.get_belief_by_tag(req_list_tag) != ""
            else "EMPTY"
        )  # fixme: avoid duplicate call

        print(f"{'-' * 80}")
        print(str(self))
        print(
            "I received the initial specification, the list of atomic requirements, the proposed addition, and I passed them to the LLM."
        )

        prompt = (
            f"Initial specification:" + self.get_belief_by_tag(spec_tag) + " ;"
            f" Current atomic requirements: {the_list} ;"
            f" New atomic requirement to validate: {candidate} "
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
        assert isinstance(response, str)

        log_answer(response)

        print(f"{'-' * 80}\n")

        answer_bool = response.startswith("CORRECT")

        self.set_intention(
            "Communicate my analysis to the looper agent.", str(answer_bool)
        )

        await self.publish_message(
            Message(
                initial_desription=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=candidate,
                validation=str(answer_bool),
            ),
            topic_id=TopicId(validation_result_topic_type, source=self.id.key),
        )
