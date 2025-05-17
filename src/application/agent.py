from src.domain.entity.state import StateTypes
from src.domain.service.graph import GraphService


class AgentApplication:
    def __init__(
        self,
        graph_service: GraphService,
    ) -> None:
        self.graph_service = graph_service

    def process(
        self,
        state: StateTypes,
    ) -> StateTypes:
        return self.graph_service.do(state)
