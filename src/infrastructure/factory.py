from typing import Any

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langchain_core.language_models.fake_chat_models import FakeChatModel
from langchain_core.language_models.chat_models import BaseChatModel

from loguru import logger

from src.domain.entity.node.base import Node
from src.domain.entity.node.chat import ChatNode
from src.domain.entity.state import StateT, StateTypes
from src.domain.entity.state.base import State
from src.domain.vo.edge import Edge, NodeId


def create_nodes(
    node_configs: list[dict[str, Any]],
) -> dict[NodeId, Node[StateT]]:
    nodes: dict[NodeId, Node[StateT]] = {}

    def create_llm(config: dict[str, Any]) -> BaseChatModel:
        llm_type = config.get("type")
        if llm_type is None:
            raise KeyError
        
        match llm_type:
            case "fake":
                return FakeChatModel()
            case _:
                raise ValueError

    def create_chat_node(config: dict[str, Any]):
        node_id = config.get("id")
        if node_id is None:
            raise KeyError
        
        llm_config = config.get("llm")
        if llm_config is None:
            raise KeyError
        
        return ChatNode(
            id=node_id,
            llm=create_llm(llm_config)
        )

    for config in node_configs:
        node_type = config.get("type")
        if node_type is None:
            raise KeyError
        match config["type"]:
            case "chat":
                node = create_chat_node(config)
            case _:
                raise ValueError
            
        nodes[node.id] = node
            
    return nodes


def create_edges(
    edge_config: dict[str, Any],
) -> list[Edge]:
    logger.debug(edge_config)
    return []


def create_graph(
    state_schema_class: type[StateTypes],
    nodes: list[Node[State]],
    edges: list[Edge],
) -> CompiledStateGraph:
    graph_builder = StateGraph(
        state_schema=state_schema_class,
    )
    for node in nodes:
        graph_builder.add_node(node=node.id, action=node)

    for edge in edges:
        src_id = START if edge.src == "start" else edge.src
        dst_id = END if edge.dst == "end" else edge.dst
        graph_builder.add_edge(src_id, dst_id)

    return graph_builder.compile()
