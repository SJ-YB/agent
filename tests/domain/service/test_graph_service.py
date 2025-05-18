from typing import Any
from src.domain.entity.state.messages import MessageListState, SingleMessageState
from src.domain.factory import create_edges, create_graph, create_lms, create_nodes
from src.domain.service.graph import GraphService
from langgraph.graph.state import CompiledStateGraph


def test_create_graph_service_instance(
    fake_dummy_chat_graph: CompiledStateGraph,
) -> None:
    # When
    service = GraphService(
        graph=fake_dummy_chat_graph,
    )

    # Then
    assert isinstance(service, GraphService)
    assert service.graph == fake_dummy_chat_graph


def test_graph_service_return_state_object(
    fake_graph_service: GraphService,
) -> None:
    # Given
    fake_state = MessageListState(
        id="test_state_id",
        messages=["test_message_input"],
    )
    result_state = fake_graph_service.do(fake_state)

    assert isinstance(result_state, MessageListState)
