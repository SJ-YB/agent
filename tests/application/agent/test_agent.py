from src.application.agent import AgentApplication
from src.domain.entity.state.messages import MessageListState
from src.domain.service.graph import GraphService
from langchain_core.messages import HumanMessage


def test_agent_app_return_ai_message_when_given_user_message(
    fake_graph_service: GraphService,
) -> None:
    # Given
    app = AgentApplication(
        graph_service=fake_graph_service,
    )

    # When
    ## Fake graph service는 SinglneMessageState를 입력받습니다.
    state = MessageListState(
        id="test_state_id",
        messages=[HumanMessage("hello")],
    )
    result_state = app.process(state)

    # Then
    assert isinstance(result_state, MessageListState)
    assert result_state.messages[-1].text() == "fake response"
