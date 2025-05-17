from enum import StrEnum, auto
from typing import TypeAlias, TypeVar

from src.domain.entity.state.base import State
from src.domain.entity.state.messages import MessageListState, SingleMessageState

StateT = TypeVar("StateT", bound=State)
StateTypes: TypeAlias = MessageListState | SingleMessageState


class StateSchema(StrEnum):
    SINGLE_MESSAGE = auto()
    MESSAGE_LIST = auto()
