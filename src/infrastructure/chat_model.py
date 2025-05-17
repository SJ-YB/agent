from typing import TypeAlias

import msgspec


class HuggingFaceChatModelSpec(msgspec.Struct):
    model_id: str


class OpenAIChatModelSpec(msgspec.Struct):
    model_id: str


ChatModelSpecTypes: TypeAlias = HuggingFaceChatModelSpec | OpenAIChatModelSpec
