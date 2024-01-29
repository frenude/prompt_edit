from typing import List

from openai import OpenAI, AzureOpenAI, Stream
from openai._types import NotGiven, NOT_GIVEN
from openai.pagination import SyncCursorPage
from openai.types.beta import assistant_create_params, Assistant
from openai.types.beta.threads import ThreadMessage

from openai.types.chat import ChatCompletionMessageParam, ChatCompletion, ChatCompletionChunk, ChatCompletionToolParam, \
    ChatCompletionToolChoiceOptionParam, completion_create_params

from src.conf import cfg

llm = {
    "openai": {"client": OpenAI(api_key=cfg.openai.api_key), "model": cfg.openai.model},
    "azure": {"client": AzureOpenAI(
        api_version=cfg.azure.api_version,
        azure_endpoint=cfg.azure.azure_endpoint,
        api_key=cfg.azure.api_key
    ), "model": cfg.azure.model},
    "moonshot": {"client": OpenAI(
        api_key=cfg.moonshot.api_key,
        base_url=cfg.moonshot.base_url,
    ), "model": cfg.moonshot.model}
}
client = llm[cfg.default.llm]["client"]


def completion(messages: List[ChatCompletionMessageParam], temperature: float,
               tools: List[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
               tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
               response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN) -> ChatCompletion | \
                                                                                                   Stream[
                                                                                                       ChatCompletionChunk]:
    """
    :param messages:
           messages = [
                        {
                            "role": "system",
                            "content": ""
                        },
                        {
                            "role": "user",
                            "content": ""
                        }
                    ]
    :param temperature:
    :param tools:
            tools = [
                        {
                            "type": "function",
                            "function": {
                                "name": "",
                                "description": "",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "____": {
                                            "type": "string",
                                            "enum": ["__","__"],
                                            "description": ""
                                        },

                                    },
                                    "required": ["____"],
                                }
                            }
                        }
                    ]
    :param tool_choice: default auto
    :return: chat.completions resp.choices[0].message.content
             function call resp.choices[0].message.tool_calls[0].function.arguments
    """
    return client.chat.completions.create(
        model=llm[cfg.default.llm]["model"],
        messages=messages,
        temperature=temperature,
        tools=tools,
        tool_choice=tool_choice,
        response_format=response_format
    )


def new_assistant(name: str, description: str, instructions: str,
                  tools: List[assistant_create_params.Tool] | NotGiven = NOT_GIVEN) -> Assistant:
    return client.beta.assistants.create(
        instructions=instructions,
        description=description,
        name=name,
        tools=tools if tools else [{"type": "code_interpreter"}, {"type": "retrieval"}],
        model=cfg.openai.model)


def add_and_run(content: str, assistant_id: str, instructions: str = "") -> SyncCursorPage[ThreadMessage]:
    """
    :param content:
    :param assistant_id:
    :param instructions:
    :return: thread_messages.data[0].content[0].text.value
    """
    run = client.beta.threads.create_and_run(
        assistant_id=assistant_id,
        instructions=instructions,
        thread={
            "messages": [
                {"role": "user", "content": content}
            ]
        }
    )
    while True:
        run = client.beta.threads.runs.retrieve(  # 通过thread.id和run.id来查看run的状态
            thread_id=run.thread_id,
            run_id=run.id
        )
        if run.status == "completed":
            break
    return client.beta.threads.messages.list(run.thread_id)