from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import Checkpoint
from src.domain.entity.state.messages import MessageListState
from src.domain.service.graph import GraphInput, GraphService
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
        messages=[HumanMessage(content="test_message_input")],
    )
    fake_config: RunnableConfig = {"configurable": {"thread_id": "test_thread"}}
    fake_input = GraphInput(
        state=fake_state,
        config=fake_config,
    )
    # When
    result_state = fake_graph_service.do(
        graph_input=fake_input,
    )

    # Then
    assert isinstance(result_state, MessageListState)


def test_graph_save_memory(
    fake_graph_service: GraphService,
) -> None:
    # Given
    fake_state = MessageListState(
        id="test_state_id",
        messages=[HumanMessage(content="test_message_input")],
    )
    fake_config: RunnableConfig = {"configurable": {"thread_id": "test_thread"}}

    fake_input = GraphInput(
        state=fake_state,
        config=fake_config,
    )
    # When
    result_state = fake_graph_service.do(
        graph_input=fake_input,
    )

    # Then
    checkpoint = fake_graph_service.graph.checkpointer.get(fake_config)

    assert checkpoint is not None
    for k in Checkpoint.__annotations__.keys():
        assert k in checkpoint
    assert checkpoint["channel_values"]["id"] == fake_state.id
    assert checkpoint["channel_values"]["messages"][0] == fake_state.messages[0]
    assert checkpoint["channel_values"]["messages"][1] == result_state.messages[-1]
