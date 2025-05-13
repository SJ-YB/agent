import msgspec

from src.domain import Node, CharacterAppendingNode


def test_create_node():
    sample_node_spec = {"id": "node_1", "attr": "test"}
    node = msgspec.convert(sample_node_spec, type=Node)

    assert isinstance(node, Node)
    assert node.id == sample_node_spec["id"]
    assert node.attr == sample_node_spec["attr"]


def test_create_a_char_appending_node():
    sample_node_spec = {"id": "node_1", "attr": "test", "char": "A"}
    node = msgspec.convert(sample_node_spec, type=CharacterAppendingNode)
    state = {"test": ""}

    new_state = node(state)

    assert isinstance(node, CharacterAppendingNode)
    assert new_state.get("test") == state["test"] + sample_node_spec["char"]


def test_create_char_append_nodes():
    sample_node_specs = [
        {"id": "node_1", "attr": "test", "char": "A"},
        {"id": "node_2", "attr": "test", "char": "B"},
        {"id": "node_3", "attr": "test", "char": "C"},
    ]

    nodes = [
        msgspec.convert(spec, type=CharacterAppendingNode) for spec in sample_node_specs
    ]
    state = {"test": ""}

    for node in nodes:
        state = node(state)

    assert len(nodes) == len(sample_node_specs)
    assert all(isinstance(node, CharacterAppendingNode) for node in nodes)
    assert state.get("test") == "ABC"
