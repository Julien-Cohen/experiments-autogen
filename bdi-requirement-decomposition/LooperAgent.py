from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId

from Message import *
from BDIData import *


@type_subscription(topic_type=validation_result_topic_type)
class LooperAgent(RoutedAgent, BDIData):

    def __init__(self) -> None:
        RoutedAgent.__init__(self, "A Looper agent (Algorithmic).")
        BDIData.__init__(self)

        self.desire.append("Pass to the manager a list of requirement complete.")
        self.desire.append("Pass to the manager a list of requirement correct.")
        self.desire.append("Pass to the manager a list of requirements without redundancy.")

    @message_handler
    async def handle_final_copy(self, message: Message, ctx: MessageContext) -> None:
        bdi_observe_message(self, message)

        print(f"{'-' * 80}")
        print("I am: " + self._description)

        print(str(self))

        print("My goal is to re-launch the process, with a convenient list of atomic requirements.")
        print("I received a message with the initial specification, a list of atomic requirement, a tentative requirement, and the result of the validation.")
        print(f"You described the following specification:\n" + self.get_belief_by_tag(spec_tag) +"\n")
        print(f"We consider the following atomic requirement:\n {message.atomic_requirement_tentative}\n")
        print(f"Validation: {message.validation}")
        if bool(message.validation) :
            print(f"(validated)")
        else:
            print(f"(invalidated)")
        print(f"{'-' * 80}\n")

        new_list = self.get_belief_by_tag(req_list_tag) + " \n * " + message.atomic_requirement_tentative if bool(message.validation) else self.get_belief_by_tag(req_list_tag)

        if message.validation :
            await self.publish_message(Message(initial_desription=self.get_belief_by_tag(spec_tag),
                                               current_list=new_list ),
                                       topic_id=TopicId(init_topic_type, source=self.id.key))


    def __str__(self) :
        return BDIData.__str__(self)