import json
from pathlib import Path
from typing import Any, TypeAlias, cast
import msgspec
import pytest
from fastapi.testclient import TestClient
from langgraph.graph.state import CompiledStateGraph, StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain_core.messages import AIMessage
from langchain_core.language_models.fake_chat_models import FakeChatModel


from src.api.web.app import create_web_app
from src.container import Container
from src.domain.entity.node import NodeTypes
from src.domain.entity.node.base import StateDiff, Node
from src.domain.entity.state.messages import SingleMessageState
from src.domain.factory import GraphSpec, create_graph
from src.domain.service.graph import GraphService
from src.settings import ServiceName, Settings


@pytest.fixture
def fake_abc_graph_app_config_dict() -> dict[str, Any]:
    with open(Path("./tests/specs/abc.json"), "r", encoding="utf-8") as io:
        return json.load(io)


@pytest.fixture(scope="session")
def client() -> TestClient:
    app = create_web_app()
    return TestClient(app)


@pytest.fixture
def fake_agent() -> CompiledStateGraph:
    def dummy_agent_node(state: MessagesState) -> dict[str, str]:
        return {"messages": AIMessage("Hello from fake agent.")}

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(node="agent", action=dummy_agent_node)
    graph_builder.add_edge(start_key=START, end_key="agent")
    graph_builder.add_edge(start_key="agent", end_key=END)
    agent = graph_builder.compile(
        debug=True,
    )
    return agent


@pytest.fixture
def fake_chat_client() -> TestClient:
    container = Container()
    settings = Settings(_env_file=Path(".env.test"))
    container.env_config.from_pydantic(settings)
    container.graph_config.from_json(settings.graph_spec_path)
    container.init_resources()
    app = create_web_app()
    return TestClient(app)


@pytest.fixture
def fake_graph(fake_abc_graph_app_config_dict: dict[str, Any]) -> CompiledStateGraph:
    class StaticValueNode(Node[SingleMessageState], tag="static_value"):
        """
        Unit test 용 임시 Node.
        {"message": `value`} StateDiff를 반환합니다.
        """

        value: str

        def _process(self, state: SingleMessageState) -> StateDiff:
            return cast(StateDiff, {"message": self.value})

    FakeNodeTypes: TypeAlias = NodeTypes | StaticValueNode

    class FakeGraphSpec(GraphSpec):
        nodes: list[FakeNodeTypes]

    spec = msgspec.convert(
        fake_abc_graph_app_config_dict,
        type=FakeGraphSpec,
    )

    graph_builder = StateGraph(state_schema=SingleMessageState)

    for node in spec.nodes:
        graph_builder.add_node(node=node.id, action=node)

    for edge in spec.edges:
        src_id = START if edge.src == "start" else edge.src
        dst_id = END if edge.dst == "end" else edge.dst
        graph_builder.add_edge(src_id, dst_id)

    return graph_builder.compile()


@pytest.fixture
def fake_graph_service(
    fake_graph: CompiledStateGraph,
) -> GraphService:
    return GraphService(
        fake_graph,
        state_schema_class=SingleMessageState,
    )


@pytest.fixture
def fake_llm() -> FakeChatModel:
    return FakeChatModel()
