"""Storage handling for GitDo."""

import json
from pathlib import Path
from uuid import uuid4

from .models import Task


class Storage:
    """Handle task storage in .gitdo/ folder."""

    def __init__(self, base_path: Path | None = None):
        """Initialize storage.

        Args:
            base_path: Base path for storage. Defaults to current directory.
        """
        self.base_path = base_path or Path.cwd()
        self.storage_dir = self.base_path / ".gitdo"
        self.tasks_file = self.storage_dir / "tasks.json"

    def init(self) -> None:
        """Initialize .gitdo folder and files."""
        self.storage_dir.mkdir(exist_ok=True)
        if not self.tasks_file.exists():
            self._save_tasks([])

    def is_initialized(self) -> bool:
        """Check if .gitracker folder exists."""
        return self.storage_dir.exists() and self.tasks_file.exists()

    def add_task(self, title: str) -> Task:
        """Add a new task.

        Args:
            title: Task title

        Returns:
            Created task
        """
        tasks = self.load_tasks()
        task = Task(id=str(uuid4()), title=title)
        tasks.append(task)
        self._save_tasks(tasks)
        return task

    def load_tasks(self) -> list[Task]:
        """Load all tasks from storage.

        Returns:
            List of tasks
        """
        if not self.tasks_file.exists():
            return []

        with open(self.tasks_file) as f:
            data = json.load(f)
            return [Task.from_dict(task_data) for task_data in data]

    def get_task(self, task_id: str) -> Task | None:
        """Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task if found, None otherwise
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id.startswith(task_id):
                return task
        return None

    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed.

        Args:
            task_id: Task ID

        Returns:
            True if task was found and completed, False otherwise
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id.startswith(task_id):
                task.complete()
                self._save_tasks(tasks)
                return True
        return False

    def remove_task(self, task_id: str) -> bool:
        """Remove task.

        Args:
            task_id: Task ID

        Returns:
            True if task was found and removed, False otherwise
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id.startswith(task_id):
                tasks.pop(i)
                self._save_tasks(tasks)
                return True
        return False

    def _save_tasks(self, tasks: list[Task]) -> None:
        """Save tasks to storage.

        Args:
            tasks: List of tasks to save
        """
        with open(self.tasks_file, "w") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)
