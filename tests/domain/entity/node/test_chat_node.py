import msgspec
import pytest

from src.domain.entity.node import NodeTypes
from src.domain.entity.node.chat import ChatNode

from langchain_core.language_models.fake_chat_models import FakeChatModel
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage

from src.domain.entity.state.messages import MessageListState


def test_create_chat_node_instance(
    fake_llm: FakeChatModel,
) -> None:
    node_spec = {
        "type": "chat",
        "id": "test_chat_node",
        "llm": fake_llm,
    }
    node = msgspec.convert(node_spec, type=NodeTypes)

    assert isinstance(node, ChatNode)
    assert node.id == node_spec["id"]
    assert isinstance(node.llm, BaseChatModel)


def test_create_chat_node_instance(
    fake_llm: FakeChatModel,
) -> None:
    # Given
    node_spec = {
        "type": "chat",
        "id": "dummy_chat_node",
        "llm": fake_llm,
    }

    # When
    chat_node = msgspec.convert(
        node_spec,
        type=NodeTypes,
    )

    # Then
    assert isinstance(chat_node, ChatNode)
    assert isinstance(chat_node.llm, BaseChatModel)


def test_chat_node_returns_message(fake_llm: FakeChatModel) -> None:
    # Given
    node_spec = {
        "type": "chat",
        "id": "dummy_chat_node",
        "llm": fake_llm,
    }
    chat_node = msgspec.convert(
        node_spec,
        type=NodeTypes,
    )
    input_state = MessageListState(
        id="test_state", messages=[HumanMessage("hello world")]
    )
    expected_chat_node_response_message = "fake response"

    # When
    result_state = chat_node(input_state)

    # Then
    assert "messages" in result_state
    for key in result_state:
        assert key in MessageListState.__annotations__.keys()
    assert isinstance(result_state["messages"], AIMessage)
    assert result_state["messages"].content == expected_chat_node_response_message
