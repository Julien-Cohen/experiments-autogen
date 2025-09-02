from autogen_core import (
    type_subscription,
    MessageContext,
    TopicId,
)

from experiment_bdi_requirement_decomposition.example.message import *
from bdi_routed_agent import *


@type_subscription(topic_type=validation_result_topic_type)
class MultiplexerAgent(BDIRoutedAgent):

    validation_correctness = "CORRECTNESS"
    validation_non_redundancy = "NON-REDUNDANCY"
    validation_satisfiability = "SATISFIABILITY"

    def __init__(self) -> None:
        super().__init__("A Multiplexer Agent (Algorithmic).")

        self.add_desire("Pass to the manager a list of requirement complete.")
        self.add_desire("Pass to the manager a list of requirement correct.")
        self.add_desire(
            "Pass to the manager a list of requirements without redundancy."
        )
        self.candidate = None

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        await super().handle_message(message, ctx)

    # override
    def bdi_observe_message(self, message):
        message__bdi_observe_message(self, message)
        self.candidate = message.atomic_requirement_tentative
        if message.validation is correctness_validated:
            self.update_belief(tag=self.validation_correctness, data=True)
        elif message.validation is correctness_invalidated:
            self.update_belief(tag=self.validation_correctness, data=False)
        elif message.validation is non_redundancy_validated:
            self.update_belief(tag=self.validation_non_redundancy, data=True)
        elif message.validation is non_redundancy_invalidated:
            self.update_belief(tag=self.validation_non_redundancy, data=False)
        elif message.validation is satisfiability_validated:
            self.update_belief(tag=self.validation_satisfiability, data=True)
        elif message.validation is satisfiability_validated:
            self.update_belief(tag=self.validation_satisfiability, data=False)

    # override
    async def bdi_select_intention(self, ctx):

        print(f"We consider the following atomic requirement:\n {self.candidate}\n")
        print(
            f"* Correctness Validation: {str(self.get_belief_by_tag(self.validation_correctness))}"
        )
        print(
            f"* Non Redundancy Validation: {str(self.get_belief_by_tag(self.validation_non_redundancy))}"
        )
        print(
            f"* Satisfiability Validation: {str(self.get_belief_by_tag(self.validation_satisfiability))}"
        )

        old_list = self.get_belief_by_tag(req_list_tag)

        if (
            (self.get_belief_by_tag(self.validation_correctness) is False)
            or (self.get_belief_by_tag(self.validation_non_redundancy) is False)
            or (self.get_belief_by_tag(self.validation_satisfiability) is False)
        ):
            self.add_intention("PASS", old_list)

        elif (
            (self.get_belief_by_tag(self.validation_correctness) is None)
            or (self.get_belief_by_tag(self.validation_non_redundancy) is None)
            or (self.get_belief_by_tag(self.validation_satisfiability) is None)
        ):
            self.add_intention("WAIT", "-")

        else:
            assert (
                (self.get_belief_by_tag(self.validation_correctness) is True)
                and (self.get_belief_by_tag(self.validation_non_redundancy) is True)
                and (self.get_belief_by_tag(self.validation_satisfiability) is True)
            )

            new_list = old_list + " \n * " + self.candidate

            self.add_intention("ADD", new_list)

    def reset(self):
        self.update_belief(tag=self.validation_correctness, data=None)
        self.update_belief(tag=self.validation_non_redundancy, data=None)
        self.update_belief(tag=self.validation_satisfiability, data=None)

    # override
    async def bdi_act(self, ctx):
        if self.has_intention("ADD"):
            self.reset()
            data = self.get_intention_data("ADD")
            self.remove_intention("ADD", data)
            await self.publish_message(
                Message(
                    initial_description=self.get_belief_by_tag(spec_tag),
                    current_list=data,
                ),
                topic_id=TopicId(init_topic_type, source=self.id.key),
            )

        elif self.has_intention("PASS"):
            self.reset()
            data = self.get_intention_data("PASS")
            self.remove_intention("PASS", data)
            await self.publish_message(
                Message(
                    initial_description=self.get_belief_by_tag(spec_tag),
                    current_list=data,
                ),
                topic_id=TopicId(init_topic_type, source=self.id.key),
            )

        else:
            assert self.has_intention("WAIT")
            self.remove_first_intention("WAIT")
            return
