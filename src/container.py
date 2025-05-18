from dependency_injector import containers, providers

from src.application.agent import AgentApplication
from src.domain.factory import create_edges, create_graph, create_lms, create_nodes
from src.domain.service.graph import GraphService
from src.infrastructure.factory import create_http_client


class InfrastructureContainer(containers.DeclarativeContainer):
    env_config = providers.Configuration()

    openai = providers.Resource(
        create_http_client,
        enabled=env_config.infrastructure.openai.enalbed,
        api_key=env_config.infrastructure.openai.api_key,
        base_url=env_config.infrastructure.openai.base_url,
    )


class GraphContainer(containers.DeclarativeContainer):
    graph_config = providers.Configuration()

    lms = providers.Singleton(
        create_lms,
        lm_specs=graph_config.lms.provided,
    )
    nodes = providers.Singleton(
        create_nodes,
        node_specs=graph_config.nodes.provided,
        language_models=lms,
    )
    edges = providers.Singleton(
        create_edges,
        edge_specs=graph_config.edges.provided,
    )
    compiled_graph = providers.Singleton(
        create_graph,
        state_schema_class=graph_config.state_schema,
        nodes=nodes,
        edges=edges,
    )


class ServiceContainer(containers.DeclarativeContainer):
    graph_cont = providers.DependenciesContainer()

    graph = providers.Singleton(
        GraphService,
        graph=graph_cont.compiled_graph,
    )


class Container(containers.DeclarativeContainer):
    env_config = providers.Configuration()
    graph_config = providers.Configuration()

    infrastructure_cont = providers.Container(
        InfrastructureContainer,
        env_config=env_config,
    )

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
