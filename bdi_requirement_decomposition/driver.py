# Test BDI agents with a sequential workflow
# Adapted from https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/sequential-workflow.html

from autogen_core import (
    SingleThreadedAgentRuntime,
    TopicId,
)
from autogen_core.models import ModelInfo
from autogen_ext.cache_store.diskcache import DiskCacheStore
from autogen_ext.models.cache import ChatCompletionCache, CHAT_CACHE_VALUE_TYPE
from autogen_ext.models.openai import OpenAIChatCompletionClient

from requirement_manager_agent import RequirementManagerAgent
from requirement_decomposer_agent import RequirementDecomposerAgent
from looper_agent import LooperAgent
from requirement_validator_agent import *

from dotenv import load_dotenv

load_dotenv()


async def main():

    # Workflow

    model_client_1 = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        # api_key="YOUR_API_KEY"
    )
    # https://platform.openai.com/settings/organization/limits

    model_client_2 = OpenAIChatCompletionClient(
        model="gemini-2.0-flash-lite",
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="unknown",
            structured_output=True,
        ),
        # api_key="GEMINI_API_KEY",
    )
    # https://ai.google.dev/gemini-api/docs/rate-limits?hl=fr

    from diskcache import Cache

    cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache("/tmp"))
    cache_client = ChatCompletionCache(model_client_1, cache_store)

    # update model_client below to change the LLM model
    model_client = cache_client

    runtime = SingleThreadedAgentRuntime()

    await RequirementManagerAgent.register(
        runtime,
        type=init_topic_type,
        factory=lambda: RequirementManagerAgent(model_client=model_client),
    )
    await RequirementDecomposerAgent.register(
        runtime,
        type=cut_request_topic_type,
        factory=lambda: RequirementDecomposerAgent(model_client=model_client),
    )
    await RequirementValidatorAgent.register(
        runtime,
        type=validation_request_topic_type,
        factory=lambda: RequirementValidatorAgent(model_client=model_client),
    )

    await LooperAgent.register(
        runtime, type=validation_result_topic_type, factory=lambda: LooperAgent()
    )

    # Run the workflow

    runtime.start()

    await runtime.publish_message(
        Message(
            initial_desription="A system to manage a space mission.", current_list=""
        ),
        topic_id=TopicId(init_topic_type, source="default"),
    )

    await runtime.stop_when_idle()
    await model_client.close()


import asyncio

asyncio.run(main())
