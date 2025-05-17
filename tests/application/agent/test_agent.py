from src.application.agent import AgentApplication
from src.domain.entity.state.messages import SingleMessageState
from src.domain.service.graph import GraphService


def test_agent_app_return_agent_message_when_given_user_message(
    fake_graph_service: GraphService,
) -> None:
    # Given
    app = AgentApplication(
        graph_service=fake_graph_service,
    )

    # When
    ## Fake graph service는 SinglneMessageState를 입력받습니다.
    state = SingleMessageState(
        id="test_state_id",
        message="",
    )
    result_state = app.process(state)

    # Then
    assert isinstance(result_state, SingleMessageState)
    assert result_state.message == "abc"
