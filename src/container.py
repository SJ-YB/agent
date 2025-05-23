from dependency_injector import containers, providers
from langgraph.checkpoint.memory import InMemorySaver

from src.application.agent import AgentApplication
from src.domain.factory import create_edges, create_graph, create_lms, create_nodes
from src.domain.service.graph import GraphService
from src.infrastructure.factory import (
    create_async_http_client,
    create_async_openai_client,
    create_sync_http_client,
    create_sync_openai_client,
)


class InfrastructureContainer(containers.DeclarativeContainer):
    env_config = providers.Configuration()

    sync_openai = providers.Resource(
        create_sync_openai_client,
        enabled=env_config.infrastructure.openai.enabled,
        api_key=env_config.infrastructure.openai.api_key,
        base_url=env_config.infrastructure.openai.base_url,
    )

    async_openai = providers.Resource(
        create_async_openai_client,
        enabled=env_config.infrastructure.openai.enabled,
        api_key=env_config.infrastructure.openai.api_key,
        base_url=env_config.infrastructure.openai.base_url,
    )

    http_async_openai = providers.Resource(
        create_async_http_client,
        enabled=env_config.infrastructure.openai.enabled,
        api_key=env_config.infrastructure.openai.api_key,
        base_url=env_config.infrastructure.openai.base_url,
    )
    http_sync_openai = providers.Resource(
        create_sync_http_client,
        enabled=env_config.infrastructure.openai.enabled,
        api_key=env_config.infrastructure.openai.api_key,
        base_url=env_config.infrastructure.openai.base_url,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    env_config = providers.Configuration()

    checkpoint_saver = providers.Selector(
        env_config.repository.checkpoint_saver,
        memory=providers.Singleton(
            InMemorySaver,
        ),
        null=providers.Object(),
    )


class GraphContainer(containers.DeclarativeContainer):
    graph_config = providers.Configuration()
    infrastructure_cont = providers.DependenciesContainer()
    repository_cont = providers.DependenciesContainer()

    lms = providers.Singleton(
        create_lms,
        lm_specs=graph_config.lms.provided,
        clients=providers.Dict(
            {
                "async_openai": infrastructure_cont.async_openai,
                "sync_openai": infrastructure_cont.sync_openai,
                "async_http_openai": infrastructure_cont.http_async_openai,
                "sync_http_openai": infrastructure_cont.http_sync_openai,
            }
        ),
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
        checkpoint_saver=repository_cont.checkpoint_saver,
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

    repository_cont = providers.Container(
        RepositoryContainer,
        env_config=env_config,
    )

    graph_cont = providers.Container(
        GraphContainer,
        graph_config=graph_config,
        infrastructure_cont=infrastructure_cont,
        repository_cont=repository_cont,
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
