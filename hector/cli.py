import typer

from rich.console import Console

from .typers import bot_typer, diff_typer, report_typer


console = Console()


typer_app = typer.Typer()
typer_app.add_typer(diff_typer, name="diff")
typer_app.add_typer(bot_typer, name="bot")
typer_app.add_typer(report_typer, name="report")


if __name__ == "__main__":
    typer_app()
