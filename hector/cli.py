import typer

from typing_extensions import Annotated

from .typers import bot_typer, diff_typer, report_typer
from .typers.bot import post


core_typer = typer.Typer(
    help="A code quality & coverage analytics toolkit.\n\nBuilt with 🤍 @ Tata 1mg."
)
core_typer.add_typer(diff_typer, name="diff")
core_typer.add_typer(bot_typer, name="bot")
core_typer.add_typer(report_typer, name="report")


@core_typer.command(help="Post a comment. Alias for `bot post`")
def comment(
    bitbucket: Annotated[
        bool,
        typer.Option(help="Post comment to bitbucket PR."),
    ] = False,
    dry: Annotated[
        bool,
        typer.Option(help="Only prepare comment without actually posting."),
    ] = False,
):
    post(bitbucket=bitbucket, dry=dry)


if __name__ == "__main__":
    core_typer()
