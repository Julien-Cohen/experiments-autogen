from autogen_core import (
    type_subscription,
    MessageContext,
    TopicId,
)

from message import *
from bdi_routed_agent import *


@type_subscription(topic_type=validation_result_topic_type)
class LooperAgent(BDIRoutedAgent):

    def __init__(self) -> None:
        super().__init__("A Looper agent (Algorithmic).")

        self.add_desire("Pass to the manager a list of requirement complete.")
        self.add_desire("Pass to the manager a list of requirement correct.")
        self.add_desire(
            "Pass to the manager a list of requirements without redundancy."
        )
        self.candidate = None
        self.validation = None

    @message_handler
    async def handle_final_copy(self, message: Message, ctx: MessageContext) -> None:
        self.bdi_observe_message(message)

        print(f"{'-' * 80}")
        print(str(self))

        print(
            f"You described the following specification:\n"
            + self.get_belief_by_tag(spec_tag)
            + "\n"
        )

        print(f"We consider the following atomic requirement:\n {self.candidate}\n")
        print(f"Validation: {self.validation}")

        self.bdi_select_intention(ctx)

        print(f"{'-' * 80}\n")

        await self.bdi_act(ctx)

    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)
        self.candidate = message.atomic_requirement_tentative
        self.validation = bool(message.validation)

    def bdi_select_intention(self, ctx):

        new_list = (
            self.get_belief_by_tag(req_list_tag) + " \n * " + self.candidate
            if self.validation
            else self.get_belief_by_tag(req_list_tag)
        )

        if self.validation:
            self.set_intention(
                "Pass the list with the new requirement.",
                new_list,
            )
        else:
            self.set_intention(
                "Pass the list without the new requirement.",
                new_list,
            )

    async def bdi_act(self, ctx):
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=self.get_intention_data(),
            ),
            topic_id=TopicId(init_topic_type, source=self.id.key),
        )
