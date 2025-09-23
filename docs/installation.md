# Installation

There are several ways to install and use Goal-Dev-Spec:

## Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust. It's significantly faster than pip.

```bash
# Install using uv
uv pip install -e .

# Or run directly without installing
uv run goal init my-project
```

## Using pip

```bash
# Install using pip
pip install -e .
```

## Requirements

- Python 3.10 or higher
- Git (optional, but recommended)