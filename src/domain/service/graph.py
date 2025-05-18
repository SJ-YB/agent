from typing import Any, Type, cast

import msgspec
from langgraph.graph.state import CompiledStateGraph

from src.domain.entity.state import StateTypes


class GraphService:
    """
    LangGraph의 Graph에 State를 입력하고 그 결과를 반환합니다.
    """

    def __init__(
        self,
        graph: CompiledStateGraph,
    ) -> None:
        self.graph = graph

    def do(self, state: StateTypes) -> StateTypes:
        return self._create_state(self.graph.invoke(state))

    def _create_state(self, graph_output: dict[str, Any] | Any) -> StateTypes:
        return msgspec.convert(
            graph_output,
            type=cast(Type[StateTypes], self.graph.builder.schema),
        )
