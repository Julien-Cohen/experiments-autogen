from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from Message import *


@type_subscription(topic_type=intention_topic_type)
class OptionValidatorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("An option validator agent.")
        self._system_message = SystemMessage(
            content=(
                "You are an action validator. "
                " Given an a desire, a list of options to satisfy that desire, an a chosen action to satisfy that desire,"
                " validate that this action is possible and that it enables the satisfaction of that desire."
                " Start your answer with CORRECT if you validate, and give a brief description of the action."
                " Start your answer with INCORRECT otherwise, and explain why it is not validated."
            )
        )
        self._model_client = model_client

    @message_handler
    async def handle_options(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"Desire: {message.desire} ; Options: {message.options} ; Action to validate: {message.intention}"
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}")
        print("I am the Option Validator Agent.")
        print("I received the desire, the set of options, the selected option, and I passed them to the LLM.")
        print("Criteria specified : possible.")
        print("Here is its answer.")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}\n")


        await self.publish_message(Message(desire = message.desire, intention=message.intention, validation=response), topic_id=TopicId(validated_topic_type, source=self.id.key))
