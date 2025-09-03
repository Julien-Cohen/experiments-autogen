from autogen_core import (
    type_subscription,
    MessageContext,
    TopicId,
    message_handler,
)
from autogen_core.models import UserMessage

from experiment_bdi_requirement_decomposition.example.message import *

from bdi.llm_bdi_routed_agent import *


@type_subscription(topic_type=correctness_validation_request_topic_type)
class RequirementValidatorAgentC(LLMBDIRoutedAgent):
    """Check Correctness"""

    correct_tag = "CORRECT"
    incorrect_tag = "INCORRECT"

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            model_client=model_client,
            description="Requirement Correctness Validator agent (with LLM).",
            llm_role="You are a requirement validator.",
            llm_job_description=(
                "Given an initial specification of a system, a list of atomic requirements for that system, and a new atomic requirement,"
                " validate that this new requirement is correct with respect to the initial specification."
                " Start your answer with " + self.correct_tag + " if you validate."
                " Start your answer with "
                + self.incorrect_tag
                + " otherwise, and explain in your answer why it is not valid."
            ),
        )

        self.llm_explicit_directive = "Do you validate this?"

        self.add_desire("Ensure that the new requirement is correct.")

        self.candidate = None

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        await super().handle_message(message, ctx)

    # override
    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)
        self.candidate = message.atomic_requirement_tentative

    # override
    async def bdi_select_intention(self, ctx):
        l = self.get_belief_by_tag(req_list_tag)
        the_list = l if l != "" else "EMPTY"

        print(
            "I received the initial specification, the list of atomic requirements, the proposed addition, and I passed them to the LLM."
        )

        prompt = (
            f"Initial specification:" + self.get_belief_by_tag(spec_tag) + " ;"
            f" Current atomic requirements: {the_list} ;"
            f" New atomic requirement to validate: {self.candidate} "
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

        answer_bool = response.startswith(self.correct_tag)

        self.add_intention(
            "PUBLISH", correctness_validated if answer_bool else correctness_invalidated
        )

    # override
    async def bdi_act(self, ctx):
        assert self.has_intention("PUBLISH")
        action = "PUBLISH"
        data = self.get_intention_data(action)
        self.remove_intention(action, data)
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=self.candidate,
                validation=data,
            ),
            topic_id=TopicId(validation_result_topic_type, source=self.id.key),
        )


@type_subscription(topic_type=non_redundancy_validation_request_topic_type)
class RequirementValidatorAgentNR(LLMBDIRoutedAgent):
    """Check Not Redundant"""

    redundant_tag = "REDUNDANT"
    non_redundant_tag = "NONREDUNDANT"

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            model_client=model_client,
            description="Requirement Non-Redundancy Validator agent (with LLM).",
            llm_role="You are a requirement validator.",
            llm_job_description=(
                "Given an initial specification of a system,"
                " a list of atomic requirements for that system, and a new atomic requirement,"
                " validate that this new requirement is not redundant with the atomic requirements already listed,"
                " Start your answer with "
                + self.non_redundant_tag
                + " if you validate."
                " Start your answer with "
                + self.redundant_tag
                + " otherwise, and explain in your answer why it is not valid."
            ),
        )

        self.llm_explicit_directive = "Do you validate this?"

        self.add_desire("Ensure that the new requirement is not redundant.")
        self.candidate = None

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        await super().handle_message(message, ctx)

    # override
    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)
        self.candidate = message.atomic_requirement_tentative

    # override
    async def bdi_select_intention(self, ctx):
        l = self.get_belief_by_tag(req_list_tag)
        the_list = l if l != "" else "EMPTY"

        print(
            "I received the initial specification, the list of atomic requirements, the proposed addition, and I passed them to the LLM."
        )

        prompt = (
            f"Initial specification:" + self.get_belief_by_tag(spec_tag) + " ;"
            f" Current atomic requirements: {the_list} ;"
            f" New atomic requirement to validate: {self.candidate} "
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

        answer_bool = response.startswith(self.non_redundant_tag)

        self.add_intention(
            "PUBLISH",
            non_redundancy_validated if answer_bool else non_redundancy_invalidated,
        )

    # override
    async def bdi_act(self, ctx):
        assert self.has_intention("PUBLISH")
        action = "PUBLISH"
        data = self.get_intention_data(action)
        self.remove_intention(action, data)
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=self.candidate,
                validation=data,
            ),
            topic_id=TopicId(validation_result_topic_type, source=self.id.key),
        )


@type_subscription(topic_type=satisfiability_validation_request_topic_type)
class RequirementValidatorAgentS(LLMBDIRoutedAgent):
    """Check Satisfiability"""

    satisfiable_tag = "SATISFIABLE"
    not_satisfiable_tag = "NOT_SATISFIABLE"

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            model_client=model_client,
            description="Requirement Satisfiability Validator agent (with LLM).",
            llm_role="You are a requirement validator.",
            llm_job_description=(
                "Given an initial specification of a system, a list of atomic requirements for that system, and a new atomic requirement,"
                " validate that this new requirement is not contradictory with the atomic requirements already listed."
                " Start your answer with " + self.satisfiable_tag + " if you validate."
                " Start your answer with "
                + self.not_satisfiable_tag
                + " otherwise, and explain in your answer why it is not valid."
            ),
        )

        self.llm_explicit_directive = "Do you validate this?"

        self.add_desire(
            "Ensure that the new requirement is not contradictory with the other requirements."
        )
        self.candidate = None

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        await super().handle_message(message, ctx)

    # override
    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)
        self.candidate = message.atomic_requirement_tentative

    # override
    async def bdi_select_intention(self, ctx):
        l = self.get_belief_by_tag(req_list_tag)
        the_list = l if l != "" else "EMPTY"

        print(
            "I received the initial specification, the list of atomic requirements, the proposed addition, and I passed them to the LLM."
        )

        prompt = (
            f"Initial specification:" + self.get_belief_by_tag(spec_tag) + " ;"
            f" Current atomic requirements: {the_list} ;"
            f" New atomic requirement to validate: {self.candidate} "
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

        answer_bool = response.startswith(self.satisfiable_tag)

        self.add_intention(
            "PUBLISH",
            satisfiability_validated if answer_bool else satisfiability_invalidated,
        )

    # override
    async def bdi_act(self, ctx):
        assert self.has_intention("PUBLISH")
        action = "PUBLISH"
        data = self.get_intention_data(action)
        self.remove_intention(action, data)
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_belief_by_tag(req_list_tag),
                atomic_requirement_tentative=self.candidate,
                validation=data,
            ),
            topic_id=TopicId(validation_result_topic_type, source=self.id.key),
        )
