from dependency_injector import containers, providers

from src.application.agent import AgentApplication
from src.domain.entity.state.messages import MessageListState, SingleMessageState
from src.domain.factory import create_edges, create_graph, create_nodes
from src.domain.service.graph import GraphService


class Infrastructure(containers.DeclarativeContainer): ...


class GraphContainer(containers.DeclarativeContainer):
    graph_config = providers.Configuration()

    state_schema_class = providers.Selector(
        graph_config.state_schema,
        single_message=providers.Callable(SingleMessageState),
        message_list=providers.Callable(MessageListState),
    )

    nodes = providers.Singleton(
        create_nodes,
        node_=providers.ProvidedInstance(
            provides=graph_config.nodes,
        ),
    )
    edges = providers.Singleton(
        create_edges,
        edge_specs=providers.ProvidedInstance(
            provides=graph_config.edges,
        ),
    )
    compiled_graph = providers.Resource(
        create_graph,
        state_schema_class=state_schema_class,
        nodes=nodes,
        edges=edges,
    )


class ServiceContainer(containers.DeclarativeContainer):
    graph_cont = providers.DependenciesContainer()

    graph = providers.Singleton(
        GraphService,
        graph=graph_cont.compiled_graph,
        state_schema_class=graph_cont.state_schema_class,
    )


class Container(containers.DeclarativeContainer):
    env_config = providers.Configuration()
    graph_config = providers.Configuration()

    graph_cont = providers.Container(
        GraphContainer,
        graph_config=graph_config,
    )

    service = providers.Container(
        ServiceContainer,
        graph_cont=graph_cont,
    )

    agent_app = providers.Singleton(
        AgentApplication,
        graph_service=service.graph,
    )

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.api",
        ],
    )
