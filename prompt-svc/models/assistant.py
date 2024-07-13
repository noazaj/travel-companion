# The code in this file is leveraged from the OpenAI documentation.
# The documentation used for this file can be found here:
# https://platform.openai.com/docs/assistants/overview?context=with-streaming

from typing_extensions import override
from openai import AssistantEventHandler
from .client import Client


class Assistant():

    def __init__(self) -> None:
        self.client = Client().getClient()

        self.assistant = self.client.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and \
                run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4o",
        )

        self.thread = self.client.beta.threads.create()

        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content="I need to solve the equation `3x + 11 = 14`. \
                Can you help me?"
        )
    
    def stream(self):
        # Then, we use the `stream` SDK helper
        # with the `EventHandler` class to create the Run
        # and stream the response.
        with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as Jane Doe. The user has a\
                premium account.",
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()


# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print("\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print("\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
