from typing import Self, cast

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from src.application.agent import AgentApplication
from src.container import Container
from src.domain.entity.state.messages import MessageListState
from src.domain.service.graph import GraphInput

router: APIRouter = APIRouter()


class ChatRequestView(BaseModel):
    id: str
    thread_id: str
    message: str

    def to_graph_input(self) -> GraphInput:
        return GraphInput(
            state=self._to_state(),
            config=self._to_config(),
        )

    def _to_state(self) -> MessageListState:
        return MessageListState(
            id=self.id,
            messages=[
                HumanMessage(content=self.message),
            ],
        )

    def _to_config(self) -> RunnableConfig:
        return {
            "configurable": {
                "thread_id": self.thread_id,
            },
        }


class ChatResponseView(BaseModel):
    id: str
    message: str

    @classmethod
    def from_state(cls, state: MessageListState) -> Self:
        message = state.messages[-1]
        if not isinstance(message, AIMessage):
            raise RuntimeError("Chat Model didn't answer yet.")
        return cls(id=state.id, message=message.text())


@router.post("/v1/chat")
@inject
async def chat(
    req: ChatRequestView,
    app: AgentApplication = Depends(Provide[Container.agent_app]),
) -> ChatResponseView:
    return ChatResponseView.from_state(
        cast(MessageListState, app.process(req.to_graph_input()))
    )
