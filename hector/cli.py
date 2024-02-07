import typer

from .typers import bot_typer, diff_typer, report_typer


core_typer = typer.Typer(
    help="A code quality & coverage analytics toolkit.\n\nBuilt with 🤍 @ Tata 1mg."
)
core_typer.add_typer(diff_typer, name="diff")
core_typer.add_typer(bot_typer, name="bot")
core_typer.add_typer(report_typer, name="report")


if __name__ == "__main__":
    core_typer()
