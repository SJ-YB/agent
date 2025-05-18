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
from src.domain.entity.state.messages import MessageListState, SingleMessageState
from src.domain.factory import create_edges, create_graph, create_lms, create_nodes
from src.domain.service.graph import GraphService
from src.settings import Settings


@pytest.fixture
def fake_chat_graph_spec_dict() -> dict[str, Any]:
    with open(Path("./tests/specs/fake_chat.json"), "r", encoding="utf-8") as io:
        return json.load(io)


@pytest.fixture
def fake_llm() -> FakeChatModel:
    return FakeChatModel()


@pytest.fixture
def fake_dummy_chat_graph(
    fake_chat_graph_spec_dict: dict[str, Any],
    fake_llm: FakeChatModel,
) -> CompiledStateGraph:
    lms = create_lms(
        lm_specs=fake_chat_graph_spec_dict["lms"],
    )
    nodes = create_nodes(
        node_specs=fake_chat_graph_spec_dict["nodes"],
        language_models=lms,
    )
    edges = create_edges(
        edge_specs=fake_chat_graph_spec_dict["edges"],
    )
    return create_graph(
        state_schema_class=fake_chat_graph_spec_dict["state_schema"],
        nodes=nodes,
        edges=edges,
    )


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
def fake_graph_service(
    fake_dummy_chat_graph: CompiledStateGraph,
) -> GraphService:
    return GraphService(
        fake_dummy_chat_graph,
    )
