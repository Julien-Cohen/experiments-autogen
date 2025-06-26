from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from Message import *

from LLMRoutedAgent import *

@type_subscription(topic_type=cut_request_topic_type)
class DecomposerAgent(LLMRoutedAgent):


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

    @message_handler
    async def handle_options(self, message: Message, ctx: MessageContext) -> None:
        prompt = (  f"Initial specification: {message.initial_desription} ;"
                    f" List of atomic requirements: {message.current_list}"
                    "Now please propose a new requirement (exactly one).")
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}")
        print("I am: " + self._description)
        print("I received the initial specification and the list of atomic requirements and I passed them to the LLM.")
        print("Here is its answer.")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}\n")

        await self.publish_message(Message(initial_desription=message.initial_desription,
                                           current_list=message.current_list,
                                           atomic_requirement_tentative=response),
                                   topic_id=TopicId(validation_request_topic_type, source=self.id.key))
