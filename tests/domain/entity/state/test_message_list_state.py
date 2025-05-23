from langchain_core.messages import HumanMessage
from langgraph.cache.base import JsonPlusSerializer
from src.domain.entity.state.messages import MessageListState


def test_create_message_list_state_instance() -> None:
    # Given
    test_state_id = "test_state_id"
    test_message = HumanMessage(content="initial message for test")

    # When
    msgs_state = MessageListState(
        id=test_state_id,
        messages=[test_message],
    )

    # Then
    assert isinstance(msgs_state, MessageListState)


def test_message_list_state_is_serializable_with_default_serde() -> None:
    # Given
    test_state_id = "test_state_id"
    test_message = "initial message for test"
    langchain_default_serde = JsonPlusSerializer()

    msgs_state = MessageListState(
        id=test_state_id,
        messages=[HumanMessage(content=test_message)],
    )

    # When
    serialized = langchain_default_serde.dumps(msgs_state)

    # Then
    assert isinstance(serialized, bytes)
