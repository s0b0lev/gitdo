"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner

from gitdo.cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_init_command(runner):
    """Test init command."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "initialized successfully" in result.output.lower()


def test_init_already_initialized(runner):
    """Test init command when already initialized."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "already initialized" in result.output.lower()


def test_add_command(runner):
    """Test add command."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["add", "Test task"])
        assert result.exit_code == 0
        assert "added task" in result.output.lower()


def test_add_without_init(runner):
    """Test add command without initialization."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["add", "Test task"])
        assert result.exit_code != 0
        assert "not initialized" in result.output.lower()


def test_list_command(runner):
    """Test list command."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        runner.invoke(cli, ["add", "Task 1"])
        runner.invoke(cli, ["add", "Task 2"])

        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" in result.output


def test_list_empty(runner):
    """Test list command with no tasks."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "no tasks" in result.output.lower()


def test_list_without_init(runner):
    """Test list command without initialization."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["list"])
        assert result.exit_code != 0
        assert "not initialized" in result.output.lower()


def test_complete_command(runner):
    """Test complete command."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        add_result = runner.invoke(cli, ["add", "Test task"])

        # Extract task ID from output (first 8 characters of UUID)
        task_id = add_result.output.split("ID: ")[1].split("\n")[0]

        result = runner.invoke(cli, ["complete", task_id])
        assert result.exit_code == 0
        assert "marked as completed" in result.output.lower()


def test_complete_nonexistent_task(runner):
    """Test complete command with non-existent task."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["complete", "nonexistent"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()


def test_remove_command(runner):
    """Test remove command."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        add_result = runner.invoke(cli, ["add", "Test task"])

        # Extract task ID from output
        task_id = add_result.output.split("ID: ")[1].split("\n")[0]

        result = runner.invoke(cli, ["remove", task_id])
        assert result.exit_code == 0
        assert "removed" in result.output.lower()


def test_remove_nonexistent_task(runner):
    """Test remove command with non-existent task."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["remove", "nonexistent"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()


def test_list_all_flag(runner):
    """Test list command with --all flag."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ["init"])
        add_result = runner.invoke(cli, ["add", "Test task"])
        task_id = add_result.output.split("ID: ")[1].split("\n")[0]
        runner.invoke(cli, ["complete", task_id])

        # Without --all, completed tasks should not be shown
        result = runner.invoke(cli, ["list"])
        assert "Test task" not in result.output

        # With --all, completed tasks should be shown
        result = runner.invoke(cli, ["list", "--all"])
        assert "Test task" in result.output
        assert "completed" in result.output.lower()
