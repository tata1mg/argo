import sys

import typer

from typing_extensions import Annotated

from .bot import CoverageBot
from .console import console
from .diff import generate_report


core_typer = typer.Typer(
    help="A code quality & coverage analytics toolkit.\n\n",
    no_args_is_help=True,
    epilog="Built with 🤍 @ Tata 1mg (https://www.1mg.com/jobs)"
)



@core_typer.command(help="Generate diff coverage report and post a comment to the Bitbucket PR.")
def report(
    compare_branch: Annotated[
        str,
        typer.Option(help="Branch to compare."),
    ] = "origin/master",
    fail_under: Annotated[
        int,
        typer.Option(help="Diff Coverage percent below which error code is returned.", show_default=False),
    ] = None,
    dry: Annotated[
        bool,
        typer.Option(help="Only prepare comment without actually posting."),
    ] = False,
):
    returncode, stdout, stderr = generate_report(compare_branch=compare_branch, fail_under=fail_under)

    if stdout:
        console.rule("Report")
        console.print(stdout.decode())

    if stderr:
        console.rule("Err")
        console.print(stderr.decode())

    bot = CoverageBot(returncode=returncode)
    bot.post(dry=dry)

    if int(returncode)!=0:
        console.rule("Failed")
        print(stderr.decode())
        sys.exit(int(returncode))

@core_typer.command(help="[WIP] Serve hector as a web application.")
def serve():
    ...

if __name__ == "__main__":
    core_typer()
