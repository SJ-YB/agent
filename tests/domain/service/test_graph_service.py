from src.domain.entity.state.messages import SingleMessageState
from src.domain.service.graph import GraphService
from langgraph.graph.state import CompiledStateGraph


def test_create_graph_service_instance(
    fake_graph: CompiledStateGraph,
) -> None:
    # Given
    fake_abc_graph = fake_graph
    state_schema_class = SingleMessageState

    # When
    service = GraphService(
        graph=fake_abc_graph,
        state_schema_class=state_schema_class,
    )

    # Then
    assert isinstance(service, GraphService)
    assert service.graph == fake_abc_graph
    assert service.state_schema_class == state_schema_class


def test_graph_service_return_state_object(
    fake_graph_service: GraphService,
) -> None:
    # Given
    fake_state = SingleMessageState(
        id="test_state_id",
        message="test_message_input",
    )
    result_state = fake_graph_service.do(fake_state)

    assert isinstance(result_state, SingleMessageState)
