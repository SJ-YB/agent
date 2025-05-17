from src.domain.entity.state.messages import SingleMessageState


def test_create_single_messages_state_instance() -> None:
    # Given
    test_state_id = "test_state_id"
    test_message = "initial message for test"

    # When
    msgs_state = SingleMessageState(
        id=test_state_id,
        message=test_message,
    )

    # Then
    assert isinstance(msgs_state, SingleMessageState)
