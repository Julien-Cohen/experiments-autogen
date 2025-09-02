# Test BDI agents with a sequential workflow
# Adapted from https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/sequential-workflow.html

from autogen_core import (
    SingleThreadedAgentRuntime,
    TopicId,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient

from option_generator_agent import OptionGeneratorAgent
from option_selector_agent import OptionSelectorAgent
from user_agent import UserAgent
from option_validator_agent import *


async def main():

    # Workflow

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        # api_key="YOUR_API_KEY"
    )
    runtime = SingleThreadedAgentRuntime()

    await OptionGeneratorAgent.register(
        runtime, type=desire_topic_type, factory=lambda: OptionGeneratorAgent(model_client=model_client)
    )
    await OptionSelectorAgent.register(
        runtime, type=option_topic_type, factory=lambda: OptionSelectorAgent(model_client=model_client)
    )
    await OptionValidatorAgent.register(
        runtime, type=intention_topic_type, factory=lambda: OptionValidatorAgent(model_client=model_client)
    )

    await UserAgent.register(runtime, type=validated_topic_type, factory=lambda: UserAgent())

    # Run the workflow

    runtime.start()

    await runtime.publish_message(
        #Message(desire="I want to know the temperature in the capital of France"),
        #Message(desire="I want to become strong at playing volleyball"),
        Message(desire="I want to visit the moon."), # Sometimes invalidated
        # Message(desire="I want to visit another dimension."),
        topic_id=TopicId(desire_topic_type, source="default"),
    )

    await runtime.stop_when_idle()
    await model_client.close()

import asyncio
asyncio.run(main())

