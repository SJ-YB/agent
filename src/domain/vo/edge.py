from typing import TypeAlias

import msgspec

NodeId: TypeAlias = str


class Edge(msgspec.Struct):
    src: NodeId
    dst: NodeId
