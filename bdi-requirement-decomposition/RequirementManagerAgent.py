from autogen_core import type_subscription, RoutedAgent, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from Message import *
from LLMRoutedAgent import *

@type_subscription(topic_type=init_topic_type)
class RequirementManagerAgent(LLMRoutedAgent, BDIData):



    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A Requirement Manager agent (with LLM).", "You are a requirement manager.")
        self._system_message = SystemMessage(
            content=(
                self.llm_role +
                " Given a specification of a system, and a list of atomic requireents, tell if that list of atomic requirements covers well that specification."
                " Answer YES is the specification is well covered."
                " Answer NO otherwise."
            )
        )
        self._model_client = model_client

    @message_handler
    async def handle_user_desire(self, message: Message, ctx: MessageContext) -> None:
        bdi_observe_message(self, message)

        print(f"{'-' * 80}")
        print("I am: " + self._description)
        print("I received the initial specification and the list of atomic requirements")
        print("I pass them to the LLM to tell if the specification is well covered.")
        print(f"The current list of atomic requirements is:" + message.current_list)

        the_list = message.current_list if message.current_list != "" else "EMPTY"
        prompt = (f"This is the specification of the system: {message.initial_desription}"
                  f"This is the list of atomic requirements: {the_list}")
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)

        print("Here is its answer. (NO means not covered yet, YES means well covered)")

        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}")

        if response.startswith("YES"):
            print ("(End)")
        else:
            print ("(Continue)")
            print(f"{'-' * 80}\n")
            await self.publish_message(Message(initial_desription= self.get_belief_by_tag(spec_tag),
                                               current_list=self.get_belief_by_tag(req_list_tag)),
                                       topic_id=TopicId(cut_request_topic_type, source=self.id.key))
