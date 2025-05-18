from typing import Any

import msgspec
from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import FakeChatModel
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.domain.entity.node import NodeTypes
from src.domain.entity.node.base import Node
from src.domain.entity.node.chat import ChatNode
from src.domain.entity.state.base import State
from src.domain.vo.edge import Edge, NodeId


def create_lms(
    lm_specs: list[dict[str, str]],
) -> dict[str, BaseChatModel]:
    lms: dict[str, BaseChatModel] = {}

    for lm_spec in lm_specs:
        match (lm_spec["provider"], lm_spec["model"]):
            case ("langchain", "fake"):
                lm = FakeChatModel()
            case _:
                raise ValueError

        lms[lm_spec["id"]] = lm
    return lms


def create_nodes(
    node_specs: list[dict[str, Any]],
    language_models: dict[str, BaseChatModel],
) -> dict[NodeId, NodeTypes]:
    nodes: dict[NodeId, NodeTypes] = {}

    def create_chat_node(config: dict[str, Any]) -> ChatNode:
        node_id = config.get("id")
        if node_id is None:
            raise KeyError

        reasoning_model_id = config.get("reasoning_model")
        if reasoning_model_id is None:
            raise KeyError

        return ChatNode(id=node_id, llm=language_models[reasoning_model_id])

    for node_spec in node_specs:
        node_type = node_spec.get("type")
        if node_type is None:
            raise KeyError

        match node_spec["type"]:
            case "chat":
                node = create_chat_node(node_spec)
            case _:
                raise ValueError

        nodes[node.id] = node

    return nodes


def create_edges(
    edge_specs: list[dict[str, Any]],
) -> list[Edge]:
    edges = [
        msgspec.convert(
            edge_spec,
            type=Edge,
        )
        for edge_spec in edge_specs
    ]
    return edges


def create_graph(
    state_schema_class: str,
    nodes: dict[NodeId, Node[State]],
    edges: list[Edge],
) -> CompiledStateGraph:
    match state_schema_class:
        case "message_list":
            from src.domain.entity.state.messages import (
                MessageListState as state_schema,
            )
        case _:
            raise ValueError

    graph_builder = StateGraph(
        state_schema=state_schema,
        input=state_schema,
        output=state_schema,
    )
    for node_id, node in nodes.items():
        graph_builder.add_node(
            node=node_id,
            action=node,
        )

    for edge in edges:
        src_id = START if edge.src == "start" else edge.src
        dst_id = END if edge.dst == "end" else edge.dst
        graph_builder.add_edge(src_id, dst_id)

    return graph_builder.compile()
