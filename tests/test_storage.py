"""Tests for storage functionality."""

import json

from gitdo.models import TaskStatus


def test_storage_init(storage):
    """Test storage initialization."""
    assert not storage.is_initialized()
    storage.init()
    assert storage.is_initialized()
    assert storage.storage_dir.exists()
    assert storage.tasks_file.exists()


def test_add_task(initialized_storage):
    """Test adding a task."""
    task = initialized_storage.add_task("Test task")

    assert task.title == "Test task"
    assert task.status == TaskStatus.PENDING
    assert len(task.id) > 0


def test_load_tasks(initialized_storage):
    """Test loading tasks."""
    initialized_storage.add_task("Task 1")
    initialized_storage.add_task("Task 2")

    tasks = initialized_storage.load_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_get_task(initialized_storage):
    """Test getting a task by ID."""
    task = initialized_storage.add_task("Test task")

    # Test full ID
    found_task = initialized_storage.get_task(task.id)
    assert found_task is not None
    assert found_task.id == task.id

    # Test partial ID
    found_task = initialized_storage.get_task(task.id[:8])
    assert found_task is not None
    assert found_task.id == task.id

    # Test non-existent ID
    found_task = initialized_storage.get_task("nonexistent")
    assert found_task is None


def test_complete_task(initialized_storage):
    """Test completing a task."""
    task = initialized_storage.add_task("Test task")

    result = initialized_storage.complete_task(task.id[:8])
    assert result is True

    completed_task = initialized_storage.get_task(task.id)
    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.completed_at is not None


def test_complete_nonexistent_task(initialized_storage):
    """Test completing a non-existent task."""
    result = initialized_storage.complete_task("nonexistent")
    assert result is False


def test_remove_task(initialized_storage):
    """Test removing a task."""
    task = initialized_storage.add_task("Test task")

    result = initialized_storage.remove_task(task.id[:8])
    assert result is True

    tasks = initialized_storage.load_tasks()
    assert len(tasks) == 0


def test_remove_nonexistent_task(initialized_storage):
    """Test removing a non-existent task."""
    result = initialized_storage.remove_task("nonexistent")
    assert result is False


def test_persistence(storage):
    """Test that tasks persist across storage instances."""
    storage.init()
    task = storage.add_task("Test task")

    # Create new storage instance with same path
    new_storage = type(storage)(base_path=storage.base_path)
    tasks = new_storage.load_tasks()

    assert len(tasks) == 1
    assert tasks[0].id == task.id
    assert tasks[0].title == task.title


def test_tasks_json_format(initialized_storage):
    """Test that tasks.json has correct format."""
    task = initialized_storage.add_task("Test task")

    with open(initialized_storage.tasks_file) as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == task.id
    assert data[0]["title"] == "Test task"
