from operator import add
from typing import Annotated

from langchain_core.messages import BaseMessage

from src.domain.entity.state.base import State


class SingleMessageState(State, tag="single_message"):
    message: Annotated[str, add]


class MessageListState(State, tag="message_list"):
    messages: list[BaseMessage]
