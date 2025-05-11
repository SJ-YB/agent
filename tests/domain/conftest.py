from pytest import fixture


@fixture
def sample_node_spec() -> dict[str, str]:
    return {"id": "node_1", "attr": "test"}


@fixture
def abc_node_spec() -> dict[str, str]:
    return {"id": "node_1", "attr": "test", "char": "A"}


@fixture
def abc_node_specs() -> list[dict[str, str]]:
    return [
        {"id": "node_1", "attr": "test", "char": "A"},
        {"id": "node_2", "attr": "test", "char": "B"},
        {"id": "node_3", "attr": "test", "char": "C"},
    ]
