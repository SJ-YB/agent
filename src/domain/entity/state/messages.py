from operator import add
from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from src.domain.entity.state.base import State


class SingleMessageState(State):
    message: Annotated[str, add]


class MessageListState(State):
    messages: Annotated[list[BaseMessage], add_messages]
