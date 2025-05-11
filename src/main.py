import click

from src.api.web.commands import web as web_command


@click.group()
def cmd() -> None: ...


cmd.add_command(web_command)
if __name__ == "__main__":
    cmd()
