from enum import Enum


class PromptType(Enum):
    ChatCompletions = "chat"
    Embeddings = "embedded"
    Images = "image"
