import msgspec

from src.domain import Node, CharacterAppendingNode


def test_create_node():
    sample_node_spec = {"id": "node_1", "attr": "test"}
    node = msgspec.convert(sample_node_spec, type=Node)

    assert isinstance(node, Node)
    assert node.id == "node_1"
    assert node.attr == "test"


def test_create_a_char_appending_node():
    sample_node_spec = {"id": "node_1", "attr": "test", "char": "A"}
    node = msgspec.convert(sample_node_spec, type=CharacterAppendingNode)
    state = {"test": ""}

    new_state = node(state)

    assert isinstance(node, CharacterAppendingNode)
    assert new_state.get("test") == "A"


def test_cteate_char_append_nodes_from_spec():
    sample_node_specs = [
        {"id": "node_1", "attr": "test", "char": "A"},
        {"id": "node_2", "attr": "test", "char": "B"},
        {"id": "node_3", "attr": "test", "char": "C"},
    ]

    nodes = []
    for spec in sample_node_specs:
        nodes.append(msgspec.convert(spec, type=CharacterAppendingNode))
    state = {"test": ""}

    new_state = nodes[0](state)
    new_state = nodes[1](new_state)
    new_state = nodes[2](new_state)

    assert len(nodes) == 3
    assert new_state.get("test") == "ABC"
