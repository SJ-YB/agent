from typing import Any

import msgspec
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from loguru import logger

from src.domain.entity.node.base import Node, NodeSpec
from src.domain.entity.state import StateSchema, StateT, StateTypes
from src.domain.entity.state.base import State
from src.domain.vo.edge import Edge, NodeId


def create_nodes(
    node_specs: NodeSpec,
) -> dict[NodeId, Node[State]]:
    logger.debug(node_specs)
    return {}


def create_edges(
    edge_specs: list[dict[str, Any]],
) -> list[Edge]:
    logger.debug(edge_specs)
    return []


class GraphSpec(msgspec.Struct):
    state_schema: StateSchema
    node_specs: list[NodeSpec]
    edges: list[Edge]


def create_graph(
    state_schema_class: type[StateTypes],
    nodes: list[Node[StateT]],
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
