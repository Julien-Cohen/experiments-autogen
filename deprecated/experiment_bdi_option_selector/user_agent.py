from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext

from message import *


@type_subscription(topic_type=validated_topic_type)
class UserAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("A user agent that outputs the intention to the user.")

    @message_handler
    async def handle_final_copy(self, message: Message, ctx: MessageContext) -> None:
        print(f"{'-' * 80}")
        print("I am the User agent, my goal is to present the result to you (the user).")
        print("I received a message with the desire, the selected option, and the validation.")
        print("Here they are.")
        print(f"{'-' * 80}")
        print(f"You expressed that desire:\n {message.desire}\n")
        print(f"We selected the following action:\n {message.intention}\n")
        if message.validation.startswith("CORRECT") :
            print(f"Additionally, this action has been validated ({message.validation})")
        elif message.validation.startswith("INCORRECT") :
            print(f"But, this action has been invalidated ({message.validation})")
        else:
            print(f"Additionally, this action received the following validation:\n {message.validation}\n")

        print(f"{'-' * 80}\n")
