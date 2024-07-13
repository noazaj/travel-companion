from openai import OpenAI
from promptType import PromptType

client = OpenAI(
    api_key="",
    organization=None,
    project=None,
    base_url=None,
    timeout=None,
    max_retries=None,
    default_headers=None,
    default_query=None,
    http_client=None,
)


def prompt(promptType, options):
    match(promptType):
        case PromptType.ChatCompletions:
            promptChatCompletions(options)
        case PromptType.Embeddings:
            promptEmbeddings(options)
        case PromptType.Images:
            promptImages(options)
        case _:
            raise TypeError("Invalid Prompt Type: {promptType}")


def promptChatCompletions(options):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant,\
             skilled in explaining complex programming concepts with\
             creative flair."},
            {"role": "user", "content": "Compose a poem that explains\
             the concept of recursion in programming."}
        ]
    )


def promptEmbeddings(options):
    return client.embeddings.create(
        model="text-embedding-ada-002",
        input="The food was delicious and the waiter..."
    )


def promptImages(options):
    return client.images.generate(
        prompt="A cute baby sea otter",
        n=2,
        size="1024x1024"
    )
