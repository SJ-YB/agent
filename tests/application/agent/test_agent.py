from langchain_core.runnables import RunnableConfig
from src.application.agent import AgentApplication
from src.domain.entity.state.messages import MessageListState
from src.domain.service.graph import GraphInput, GraphService
from langchain_core.messages import HumanMessage


def test_agent_app_return_ai_message_when_given_user_message(
    fake_graph_service: GraphService,
) -> None:
    # Given
    app = AgentApplication(
        graph_service=fake_graph_service,
    )
    state = MessageListState(
        id="test_state_id",
        messages=[HumanMessage("hello")],
    )
    config: RunnableConfig = {
        "configurable": {
            "thread_id": "test_thread",
        }
    }
    graph_input = GraphInput(
        state=state,
        config=config,
    )
    # When
    result_state = app.process(graph_input)

    # Then
    assert isinstance(result_state, MessageListState)
    assert result_state.messages[-1].text() == "fake response"
