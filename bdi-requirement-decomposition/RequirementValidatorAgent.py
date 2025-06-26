from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from Message import *


@type_subscription(topic_type=validation_request_topic_type)
class RequirementValidatorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("An option validator agent.")
        self._system_message = SystemMessage(
            content=(
                "You are a requirement validator. "
                " Given an initial specification of a system, a list of atomic requirements for that system, and a new atomic requirement,"
                " validate that this new requirement is correct with respect to the initial specification, is not redundant with the atomic requirements already listed, and is not contradictory with the atomic requirements already listed."
                " Start your answer with CORRECT if you validate."
                " Start your answer with INCORRECT otherwise, and explain in your answer why it is not valid."
            )
        )
        self._model_client = model_client

    @message_handler
    async def handle_options(self, message: Message, ctx: MessageContext) -> None:
        the_list = message.current_list if message.current_list != "" else "EMPTY"
        prompt = f"Initial specification: {message.initial_desription} ;"\
                 f" Current atomic requirements: {the_list} ;"\
                 f" New atomic requirement to validate: {message.atomic_requirement_tentative}"
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}")
        print("I am the Validator Agent (LLM).")
        print("I received the initial specification, the list of atomic requirements, the proposed addition, and I passed them to the LLM.")
        print("Here is its answer.")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}\n")

        answer_bool = response.startswith("CORRECT")
        

        await self.publish_message(Message(initial_desription=message.initial_desription,
                                           current_list=message.current_list,
                                           atomic_requirement_tentative=message.atomic_requirement_tentative,
                                           validation=str(answer_bool)),
                                   topic_id=TopicId(validation_result_topic_type, source=self.id.key))
