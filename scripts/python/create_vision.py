#!/usr/bin/env python3
"""Create a new vision for the Goal Kit project."""

import json
import sys
from pathlib import Path


def main():
    """Create vision file."""
    goals_dir = Path(".goalkit/goals")
    goals_dir.mkdir(parents=True, exist_ok=True)
    
    vision_file = goals_dir / "vision.md"
    
    # Simple vision template
    vision_content = """# Project Vision

## Project Purpose
[Describe the core purpose and reason for this project]

## Success Definition
[How will you know this project is successful?]

## Key Principles
1. [First principle]
2. [Second principle]
3. [Third principle]

## Target Outcomes
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]
"""
    
    vision_file.write_text(vision_content)
    print(f"Vision file created: {vision_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
