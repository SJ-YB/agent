import click
import uvicorn

from src.api.web.app import create_web_app


@click.group()
def web() -> None: ...


@web.command()
def run() -> None:
    app = create_web_app()
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    server.run()
