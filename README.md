# GiTrack

[![CI](https://github.com/yourusername/gitrack/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/gitrack/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yourusername/gitrack/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/gitrack)
[![PyPI version](https://badge.fury.io/py/gitrack.svg)](https://badge.fury.io/py/gitrack)

Simple CLI tool to plan your work. Tasks are stored locally in a `.gitracker/` folder.

## Installation

```bash
pip install gitrack
```

## Usage

```bash
$ gitrack [command] [options]
```

## Commands

- `init`: Initialize a new GiTrack project
- `add <task>`: Add a new task to your project
- `list`: List all tasks (use `--all` to show completed tasks)
- `complete <task_id>`: Mark a task as completed
- `remove <task_id>`: Remove a task from your project

## Example

```bash
# Initialize GiTrack in your project
$ gitrack init
✓ GiTrack initialized successfully!

# Add some tasks
$ gitrack add "Implement user authentication"
✓ Added task: Implement user authentication
ID: a1b2c3d4

$ gitrack add "Write unit tests"
✓ Added task: Write unit tests
ID: e5f6g7h8

# List all pending tasks
$ gitrack list

# Complete a task (you can use just the first few characters of the ID)
$ gitrack complete a1b2

# List all tasks including completed ones
$ gitrack list --all

# Remove a task
$ gitrack remove e5f6
```

## Development

### Setup

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gitrack --cov-report=html

# Run specific test file
pytest tests/test_cli.py
```

### Code Quality

This project uses Ruff for linting and formatting:

```bash
# Check code
ruff check .

# Format code
ruff format .

# Check and fix
ruff check --fix .
```

### Project Structure

```
gitrack/
├── src/
│   └── gitrack/
│       ├── __init__.py
│       ├── cli.py          # CLI interface
│       ├── models.py       # Data models
│       └── storage.py      # Storage handling
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_cli.py         # CLI tests
│   ├── test_models.py      # Model tests
│   └── test_storage.py     # Storage tests
├── pyproject.toml          # Project configuration
└── README.md
```

### Building and Publishing

```bash
# Build the package
pip install build
python -m build

# Upload to PyPI (requires credentials)
pip install twine
twine upload dist/*
```

## License

MIT