import json

import typer

from rich.panel import Panel
from typing_extensions import Annotated

from ..bot import CoverageBot
from ..console import console
from ..models import CovReport, DiffCovReport


bot_typer = typer.Typer(help="Bot actions. Use `--help` for more options.")


@bot_typer.command(help="Post a comment. Use `--help` for more options")
def post(
    bitbucket: Annotated[
        bool,
        typer.Option(help="Post comment to bitbucket PR."),
    ] = False,
    dry: Annotated[
        bool,
        typer.Option(help="Only prepare comment without actually posting."),
    ] = False,
):
    with console.status("Parsing Reports"):
        with open("diff-coverage.json", encoding="utf-8") as f:
            diff_cov = DiffCovReport(**json.load(f))

        with open("coverage.json", encoding="utf-8") as f:
            cov = CovReport(**json.load(f))

    with console.status("Preparing Comment"):
        bot = CoverageBot(cov=cov, diff_cov=diff_cov)
        bot_comment = bot.get_comment()
        console.rule("Comment")
        console.log(Panel(bot_comment))

    if dry:
        return

    with console.status("Posting Comment", spinner="aesthetic"):
        bot.post_comment(comment=bot_comment)


@bot_typer.command(help="[WIP] Run bot as an application.")
def serve():
    raise NotImplementedError
