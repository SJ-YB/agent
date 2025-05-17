from langchain_core.language_models.chat_models import BaseChatModel

from src.domain.entity.node.base import Node, NodeSpec, StateDiff
from src.domain.entity.state.messages import MessageListState


class ChatNode(Node[MessageListState], tag="chat"):
    llm: BaseChatModel

    def _process(self, state: MessageListState) -> StateDiff:
        result = self.llm.invoke(state.messages)
        return {"messages": result}
