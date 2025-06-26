from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from Message import *

from LLMRoutedAgent import *
from BDIData import *

@type_subscription(topic_type=cut_request_topic_type)
class DecomposerAgent(LLMRoutedAgent, BDIData):


    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A decomposer agent (with LLM).", "You are a decomposer.")
        self._system_message = SystemMessage(
            content=(
                self.llm_role +
                " You receive a specification of a system, and a list of atomic requirements about that system."
                " You have to identify exactly one requirements that is related to the received specification and which is not in the list of atomic requirements."
            )
        )
        self._model_client = model_client

        self.llm_explicit_directive = "Now please propose a new requirement (exactly one)."
        self.desire.append("Find requirements related to the specifications, that help to complete the list of atomic requirements.")


    @message_handler
    async def handle_options(self, message: Message, ctx: MessageContext) -> None:
        bdi_observe_message(self, message)


        print(f"{'-' * 80}")
        print("I am: " + self._description)
        print("I received the initial specification and the list of atomic requirements and I passed them to the LLM.")



        prompt = (  f"Initial specification:" + self.get_belief_by_tag(spec_tag) +" ;" +
                    f" List of atomic requirements: " + self.get_belief_by_tag(req_list_tag) +
                    self.llm_explicit_directive)
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        self.intention = response

        print("Here is its answer.")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}\n")

        await self.publish_message(Message(initial_desription=self.get_belief_by_tag(spec_tag),
                                           current_list=self.get_belief_by_tag(req_list_tag),
                                           atomic_requirement_tentative=self.intention),
                                   topic_id=TopicId(validation_request_topic_type, source=self.id.key))
