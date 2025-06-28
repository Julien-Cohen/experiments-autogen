from autogen_core import (
    type_subscription,
    MessageContext,
    TopicId,
)
from autogen_core.models import UserMessage

from message import *
from llm_bdi_routed_agent import *


@type_subscription(topic_type=init_topic_type)
class RequirementManagerAgent(LLMBDIRoutedAgent):

    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            model_client=model_client,
            description="Requirement Manager agent (with LLM).",
            llm_role="You are a requirement manager.",
            llm_job_description=(
                "Given a specification of a system, and a list of atomic requirements, tell if that list of atomic requirements covers well that specification."
                + " Answer COMPLETE is the specification is well covered."
                + " Answer PARTIAL otherwise."
            ),
        )

        self.llm_explicit_directive = "Do you think the specification if well covered ?"

        self.add_desire(
            "Build a list of atomic requirements that cover the given specification."
        )

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        self.bdi_observe_message(message)
        log(str(self))
        await self.bdi_select_intention(ctx)
        await self.bdi_act(ctx)

    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)

    async def bdi_select_intention(self, ctx):
        print(
            "I received the initial specification and the list of atomic requirements"
        )
        print("I pass them to the LLM to tell if the specification is well covered.")
        print(
            f"The current list of atomic requirements is:"
            + self.get_belief_by_tag(req_list_tag)
        )

        l = self.get_belief_by_tag(req_list_tag)
        the_list = l if l != "" else "EMPTY"

        prompt = (
            f"This is the specification of the system: {self.get_belief_by_tag(spec_tag)}"
            f"This is the list of atomic requirements: {the_list}"
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

        print(f"{'-' * 80}")

        if response.startswith("COMPLETE"):
            self.set_intention("STOP", l)
            print("(End)")
        else:
            self.set_intention("PASS", l)
            print("(Continue)")
            print(f"{'-' * 80}\n")

    async def bdi_act(self, ctx):
        if self.get_intention_action() == "PASS":
            await self.publish_message(
                Message(
                    initial_description=self.get_belief_by_tag(spec_tag),
                    current_list=self.get_belief_by_tag(req_list_tag),
                ),
                topic_id=TopicId(cut_request_topic_type, source=self.id.key),
            )
        else:
            print(self.get_intention_data())
