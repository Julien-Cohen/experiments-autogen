from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId

from Message import *


@type_subscription(topic_type=validation_result_topic_type)
class LooperAgent(RoutedAgent):

    def __init__(self) -> None:
        super().__init__("A Looper agent (Algorithmic).")

    @message_handler
    async def handle_final_copy(self, message: Message, ctx: MessageContext) -> None:
        print(f"{'-' * 80}")
        print("I am: " + self._description +
              " My goal is to re-launch the process, with a convenient list of atomic requirements.")
        print("I received a message with the initial specification, a list of atomic requirement, a tentative requirement, and the result of the validation.")
        print(f"You described the following specification:\n {message.initial_desription}\n")
        print(f"We consider the following atomic requirement:\n {message.atomic_requirement_tentative}\n")
        print(f"Validation: {message.validation}")
        if bool(message.validation) :
            print(f"(validated)")
        else:
            print(f"(invalidated)")
        print(f"{'-' * 80}\n")

        new_list = message.current_list + " \n * " + message.atomic_requirement_tentative if bool(message.validation) else message.current_list

        if message.validation :
            await self.publish_message(Message(initial_desription=message.initial_desription, current_list=new_list ),
                                       topic_id=TopicId(init_topic_type, source=self.id.key))


