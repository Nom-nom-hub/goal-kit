
# Agent Development Guide for Goal Kit

## Build/Lint/Test Commands

### Build Commands

- **Build package**: `uv build`
- **Install locally**: `uv tool install --from . goalkeeper`
- **Install globally**: `pip install -e .`

### Test Commands

- **Run all tests**: `python scripts/python/optimization_tester.py`
- **Run single test file**: `python scripts/python/optimization_tester.py --single <test_name>`
- **Run integration tests**: `python scripts/python/optimization_tester.py --integration`
- **Run performance tests**: `python scripts/python/optimization_tester.py --performance`

### Lint/Format Commands

- **Format code**: `black src/ scripts/`
- **Lint code**: `ruff check src/ scripts/`
- **Type check**: `mypy src/ scripts/`
- **Fix lint issues**: `ruff fix src/ scripts/`

## Architecture & Codebase Structure

### Core Components

- **CLI Framework**: `src/goalkeeper_cli/__init__.py` - Main Typer-based CLI with agent initialization
- **Agent Templates**: `templates/` - Agent-specific command templates and configurations
- **Python Scripts**: `scripts/python/` - Backend logic for goal management, validation, and optimization
- **Documentation**: `docs/` - MkDocs documentation with GitHub Pages deployment

### Key Subprojects/Modules

- **Goal Management**: Scripts for creating, validating, and tracking goals
- **Project Analysis**: `src/goalkeeper_cli/analyzer.py` - ProjectAnalyzer for goal extraction and health scoring (98% coverage, 23 tests)
- **Status Command**: `src/goalkeeper_cli/commands/status.py` - Project status display with JSON output (100% coverage, 33 tests)
- **Agent Integration**: Support for Claude, Copilot, Gemini, Cursor, and other AI assistants
- **Methodology Validation**: Comprehensive testing framework for Goal-Driven Development processes
- **Documentation System**: MkDocs-based documentation with automated deployment

### Internal APIs

- **Agent Configuration API**: `AGENT_CONFIG` dict mapping agents to their settings
- **ProjectAnalyzer API**: Analysis class with methods for project loading, goal parsing, completion calculation, health scoring, and phase detection
- **Status Command API**: Command-line interface for displaying project status with formatted text or JSON output
- **StepTracker**: Hierarchical progress tracking with Rich console output
- **Template System**: Dynamic template downloading and extraction from GitHub releases
- **Validation Framework**: Comprehensive goal and methodology validation scripts

### External Dependencies

- **Package Management**: uv (Astral) for Python package management
- **CLI Framework**: Typer for command-line interface
- **Rich Output**: Rich library for terminal formatting and progress displays
- **HTTP Client**: httpx for API interactions with GitHub releases

## Code Style Guidelines

### Python Conventions

- **Imports**: Standard library first, then third-party, then local imports (alphabetical within groups)
- **Type Hints**: Use full type annotations for function parameters and return types
- **Docstrings**: Use triple-quoted docstrings following Google style
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants

### Error Handling

- **Exceptions**: Use specific exception types, avoid bare `except:` clauses
- **Logging**: Use structured logging with appropriate levels (INFO, WARNING, ERROR)
- **Graceful Degradation**: Handle missing tools/commands with informative messages
- **User Communication**: Use Rich panels and colored output for user-facing errors

### Code Structure

- **Functions**: Keep functions focused on single responsibilities, max 50 lines
- **Classes**: Use dataclasses for data structures, separate concerns properly
- **CLI Commands**: Each command should be a separate function with clear help text
- **Configuration**: Use dictionaries for agent/tool configurations with descriptive keys

### Formatting & Style

- **Line Length**: 100 characters maximum
- **Quotes**: Use double quotes for strings, single quotes for character literals
- **Trailing Commas**: Include in multi-line structures for cleaner diffs
- **Whitespace**: Follow PEP 8 spacing conventions

### File Organization

- **CLI Logic**: Keep in main `__init__.py` file with clear section separation
- **Utilities**: Common functions in separate modules (common.py)
- **Agent-Specific**: Templates and scripts organized by agent type
- **Testing**: Custom test framework with structured result reporting
