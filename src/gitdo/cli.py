"""CLI interface for GitDo."""

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .storage import Storage

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """GitDo - Simple CLI tool to plan your work."""
    pass


@cli.command()
def init():
    """Initialize a new GitDo project."""
    storage = Storage()
    if storage.is_initialized():
        console.print("[yellow]GitDo is already initialized in this directory.[/yellow]")
        return

    storage.init()
    console.print("[green]✓[/green] GitDo initialized successfully!")
    console.print(f"[dim]Created .gitdo/ folder in {storage.base_path}[/dim]")


@cli.command()
@click.argument("task")
def add(task: str):
    """Add a new task to your project."""
    storage = Storage()
    if not storage.is_initialized():
        console.print("[red]Error:[/red] GitDo is not initialized. Run 'gitdo init' first.")
        raise click.Abort()

    created_task = storage.add_task(task)
    console.print(f"[green]✓[/green] Added task: {created_task.title}")
    console.print(f"[dim]ID: {created_task.id[:8]}[/dim]")


@cli.command()
@click.option("--all", "-a", is_flag=True, help="Show all tasks including completed")
def list(all: bool):
    """List all tasks."""
    storage = Storage()
    if not storage.is_initialized():
        console.print("[red]Error:[/red] GitDo is not initialized. Run 'gitdo init' first.")
        raise click.Abort()

    tasks = storage.load_tasks()
    if not all:
        tasks = [t for t in tasks if t.status.value == "pending"]

    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Task")
    table.add_column("Status", width=12)
    table.add_column("Created", width=20)

    for task in tasks:
        status_color = "green" if task.status.value == "completed" else "yellow"
        table.add_row(
            task.id[:8],
            task.title,
            f"[{status_color}]{task.status.value}[/{status_color}]",
            task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    console.print(table)


@cli.command()
@click.argument("task_id")
def complete(task_id: str):
    """Mark a task as completed."""
    storage = Storage()
    if not storage.is_initialized():
        console.print("[red]Error:[/red] GitDo is not initialized. Run 'gitdo init' first.")
        raise click.Abort()

    if storage.complete_task(task_id):
        console.print(f"[green]✓[/green] Task {task_id} marked as completed!")
    else:
        console.print(f"[red]Error:[/red] Task {task_id} not found.")
        raise click.Abort()


@cli.command()
@click.argument("task_id")
def remove(task_id: str):
    """Remove a task from your project."""
    storage = Storage()
    if not storage.is_initialized():
        console.print("[red]Error:[/red] GitDo is not initialized. Run 'gitdo init' first.")
        raise click.Abort()

    if storage.remove_task(task_id):
        console.print(f"[green]✓[/green] Task {task_id} removed!")
    else:
        console.print(f"[red]Error:[/red] Task {task_id} not found.")
        raise click.Abort()


def main():
    """Entry point for the CLI."""
    cli()
