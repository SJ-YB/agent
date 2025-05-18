from abc import abstractmethod
from typing import Any, Generic, TypeAlias

import msgspec

from src.domain.entity.state import StateT

StateDiff: TypeAlias = dict[str, Any]


class Node(msgspec.Struct, Generic[StateT]):
    """
    Node class for LangGraph's Graph.
    ref: https://langchain-ai.github.io/langgraph/concepts/low_level/#nodes
    """

    id: str

    def __call__(self, state: StateT) -> StateDiff:
        """
        State를 반환하지 않고, 증분(StateDiff)만 반환합니다.
        증분을 State에 반영하는 방식은 State 속성의 reducer로 관리합니다.
        """
        return self._process(state)

    @abstractmethod
    def _process(self, state: StateT) -> StateDiff:
        raise NotImplementedError
