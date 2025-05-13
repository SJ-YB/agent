from typing import TypedDict

import msgspec


class State(TypedDict): ...


class Node(msgspec.Struct):
    id: str
    attr: str

    def __call__(self, state: State) -> State: ...  # type: ignore


class CharacterAppendingNode(Node):
    char: str

    def __call__(self, state: State) -> State:
        val = state.get(self.attr)
        if val is None:
            raise KeyError

        return {self.attr: val + self.char}  # type: ignore
