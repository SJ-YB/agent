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
        state_schema_class: type[StateTypes],
    ) -> None:
        self.graph = graph
        self.state_schema_class = state_schema_class

    def do(self, state: StateTypes) -> StateTypes:
        result_state = self.graph.invoke(state)
        return msgspec.convert(
            result_state,
            type=self.state_schema_class,
        )
