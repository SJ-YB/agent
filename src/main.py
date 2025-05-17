import click

from src.api.web.commands import web as web_command
from src.container import Container
from src.settings import Settings

container = Container()
env_settings = Settings()
container.env_config.from_pydantic(env_settings)
container.graph_config.from_json(env_settings.graph_spec_path)
container.init_resources()


@click.group()
def cmd() -> None: ...


cmd.add_command(web_command)
if __name__ == "__main__":
    cmd()
