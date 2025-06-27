from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from message import option_topic_type, Message, intention_topic_type


@type_subscription(topic_type=option_topic_type)
class OptionSelectorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("An option selector agent.")
        self._system_message = SystemMessage(
            content=(
                "You are an option selector. You receive a set of options that could satisfy a given desire. Identify the easiest to achieve."
            )
        )
        self._model_client = model_client

    @message_handler
    async def handle_options(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"Desire: {message.desire} ; Options: {message.options}"
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}")
        print("I am the Option Selector agent.")
        print("I received the desire and the set of options and I passed them to the LLM.")
        print("Criteria specified : easiest.")
        print("Here is its answer.")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}\n")

        await self.publish_message(Message(desire=message.desire, options=message.options, intention=response), topic_id=TopicId(intention_topic_type, source=self.id.key))
