# CS467 Online Capstone: GPT API Challenge
# Kongkom Hiranpradit, Connor Flattum, Nathan Swaim, Noah Zajicek

from .promptType import PromptType
from .client import Client

PROMPT_ITINERARY = "You are a professional vacation planner helping users \
                    plan trips abroad. You will recommend hotels, \
                    attractions, restaurants, shopping area, natural sites \
                    or any other places that the user requests. You will \
                    plan according to the budget and vacation length given \
                    by the user. You will present the result in a format of \
                    detailed itinerary of each day, begin from day 1 to the \
                    last day."


# Prompt class used to make chat GPT prompts
class Prompt():

    def __init__(self) -> None:
        self.client = Client().getClient()

    ###########################################################
    #
    #  Prompts the ChatGPT client based on the prompt type.
    #
    #  Receives:
    #   - promptType:  a PromptType enumeration of the prompt
    #                  type
    #   - options:     options used for the prompt
    #
    #  Returns:
    #   - a response from the ChatGPT client
    #
    #  Throws:
    #   - TypeError:    throws TypeError if prompt type is
    #                    invalid
    #
    ###########################################################
    def prompt(self, promptType, options):
        match(promptType):
            case PromptType.ChatCompletions:
                return self.promptChatCompletions(options)
            case PromptType.Embeddings:
                return self.promptEmbeddings(options)
            case PromptType.Images:
                return self.promptImages(options)
            case _:
                raise TypeError("Invalid Prompt Type: {promptType}")

    # Helper method for Chat GPT chat completion prompts
    def promptChatCompletions(self, messages):

        try:
            # Make call to chat GPT API
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(completion)
            return completion
        except Exception as e:
            print(e)
            return {
                "error": f"Error proocessing request: {e}"
            }

    # Helper method for Chat GPT embedded prompts
    def promptEmbeddings(self, options):
        print(options)
        completion = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=options.get('text')
        )

        return completion.to_json()

    # Helper method for Chat GPT image prompts
    def promptImages(self, options):
        completion = self.client.images.generate(
            prompt=options.get('text'),
            n=2,
            size=options.get('size')
        )

        return completion.to_json()
