from autogen_core import (
    type_subscription,
    RoutedAgent,
    message_handler,
    MessageContext,
    TopicId,
)

from message import *
from bdi_routed_agent import *


@type_subscription(topic_type=validation_result_topic_type)
class LooperAgent(BDIRoutedAgent):

    def __init__(self) -> None:
        super().__init__("A Looper agent (Algorithmic).")

        self.desire.append("Pass to the manager a list of requirement complete.")
        self.desire.append("Pass to the manager a list of requirement correct.")
        self.desire.append(
            "Pass to the manager a list of requirements without redundancy."
        )

    @message_handler
    async def handle_final_copy(self, message: Message, ctx: MessageContext) -> None:
        bdi_observe_message(self, message)
        candidate = message.atomic_requirement_tentative
        self.set_intention(
            "Consider the result of the analysis I receive, build a new list accordingly, and transmit it to the manager.",
            message.validation,
        )

        print(f"{'-' * 80}")

        print(str(self))

        print(
            "My goal is to re-launch the process, with a convenient list of atomic requirements."
        )
        print(
            "I received a message with the initial specification, a list of atomic requirement, a tentative requirement, and the result of the validation."
        )
        print(
            f"You described the following specification:\n"
            + self.get_belief_by_tag(spec_tag)
            + "\n"
        )
        print(f"We consider the following atomic requirement:\n {candidate}\n")
        print(f"Validation: {message.validation}")
        if bool(message.validation):
            self.set_intention(
                "Add this requirement to the list of considered requirements and notify the manager.",
                candidate,
            )
        else:
            self.set_intention(
                "Do not add this requirement to the list of considered requirements and notify the manager.",
                candidate,
            )

        print(f"{'-' * 80}\n")

        new_list = (
            self.get_belief_by_tag(req_list_tag) + " \n * " + candidate
            if bool(message.validation)
            else self.get_belief_by_tag(req_list_tag)
        )

        await self.publish_message(
            Message(
                initial_desription=self.get_belief_by_tag(spec_tag),
                current_list=new_list,
            ),
            topic_id=TopicId(init_topic_type, source=self.id.key),
        )
        # self.clear_intention()

    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)

    def bdi_select_intention(self, message):
        pass  # fixme

    def bdi_act(self, message):
        pass  # fixme
