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
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        await super().handle_message(message, ctx)

    # override
    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)
        self.candidate = message.atomic_requirement_tentative
        self.validation = bool(message.validation)

    # override
    async def bdi_select_intention(self, ctx):

        print(f"We consider the following atomic requirement:\n {self.candidate}\n")
        print(f"Validation: {self.validation}")

        new_list = (
            self.get_belief_by_tag(req_list_tag) + " \n * " + self.candidate
            if self.validation
            else self.get_belief_by_tag(req_list_tag)
        )

        if self.validation:
            self.add_intention(
                "ADD",
                new_list,
            )
        else:
            self.add_intention(
                "PASS",
                new_list,
            )

    # override
    async def bdi_act(self, ctx):
        action = "ADD" if self.has_intention("ADD") else "PASS"
        data = self.get_intention_data(action)
        self.remove_intention(action, data)
        await self.publish_message(
            Message(
                initial_description=self.get_belief_by_tag(spec_tag),
                current_list=data,
            ),
            topic_id=TopicId(init_topic_type, source=self.id.key),
        )
