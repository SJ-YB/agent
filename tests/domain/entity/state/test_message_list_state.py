from src.domain.entity.state.messages import MessageListState


def test_create_message_list_state_instance() -> None:
    # Given
    test_state_id = "test_state_id"
    test_message = "initial message for test"

    # When
    msgs_state = MessageListState(
        id=test_state_id,
        messages=[test_message],
    )

    # Then
    assert isinstance(msgs_state, MessageListState)
