from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from message import desire_topic_type, Message, option_topic_type


@type_subscription(topic_type=desire_topic_type)
class OptionGeneratorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("An option generator agent.")
        self._system_message = SystemMessage(
            content=(
                "You are an option generator. Given a desire, identify a set of options to achieve that desire."
            )
        )
        self._model_client = model_client

    @message_handler
    async def handle_user_desire(self, message: Message, ctx: MessageContext) -> None:
        desire = message.desire
        prompt = f"This is my desire: {desire}"
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-'*80}")
        print("I am the Option Generator agent.")
        print("I received the desire and passed it to the LLM.")
        print("Here is its answer.")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}\n")

        await self.publish_message(Message(desire = desire, options=response), topic_id=TopicId(option_topic_type, source=self.id.key))
