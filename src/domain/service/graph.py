from typing import Any, Type, cast

import msgspec
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from src.domain.entity.state import StateTypes


class GraphInput(msgspec.Struct):
    state: StateTypes
    config: RunnableConfig = {}


class GraphService:
    """
    LangGraph의 Graph에 State를 입력하고 그 결과를 반환합니다.
    """

    def __init__(
        self,
        graph: CompiledStateGraph,
    ) -> None:
        self.graph = graph

    def do(self, graph_input: GraphInput) -> StateTypes:
        return self._create_state(
            self.graph.invoke(
                input=graph_input.state,
                config=graph_input.config,
            )
        )

    def _create_state(self, graph_output: dict[str, Any] | Any) -> StateTypes:
        state_cls = cast(Type[StateTypes], self.graph.builder.schema)
        return state_cls.model_validate(
            obj=graph_output,
        )
