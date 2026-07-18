#!/usr/bin/env python3
"""
Generate professional terminal-style SVG screenshots for the README.

Outputs SVGs to docs/screenshots/ directory.
"""

import os
import xml.sax.saxutils as saxutils

# ── configuration ──────────────────────────────────────────────────────────

WINDOW_TITLE  = "goalkit — terminal"
FONT_FAMILY   = "'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Courier New', monospace"
FONT_SIZE     = 14
LINE_HEIGHT   = 20
PADDING_X     = 20
PADDING_Y     = 16
WINDOW_BG     = "#1e1e2e"       # Catppuccin Mocha base
SIDEBAR_BG    = "#181825"       # Catppuccin Mocha mantle
TITLE_BG      = "#2d2d44"       # slightly lighter bar
TEXT_COLOR    = "#cdd6f4"
GREEN         = "#a6e3a1"
YELLOW        = "#f9e2af"
RED           = "#f38ba8"
BLUE          = "#89b4fa"
CYAN          = "#89dceb"
DIM           = "#585b70"
ORANGE        = "#fab387"
WHITE         = "#ffffff"
MAGENTA       = "#cba6f7"
BORDER_COLOR  = "#45475a"
CORNER_RADIUS = 8

# ── helpers ────────────────────────────────────────────────────────────────

def esc(text: str) -> str:
    """XML-escape text for SVG."""
    return saxutils.escape(text)

def ansi_to_svg(text):
    """Convert a line of text to SVG span tuples (plain text fallback, no ANSI)."""
    return [('text', text, TEXT_COLOR, None, False)]

def generate_svg(lines: list, filename: str, width: int = 780):
    """Generate a terminal-style SVG from a list of text lines."""
    
    # Calculate image dimensions
    max_line_len = max(len(line.replace('\t', '    ')) for line in lines) if lines else 40
    char_width = FONT_SIZE * 0.6
    content_width = max(max_line_len * char_width, 400)
    svg_width = max(width, content_width + PADDING_X * 2 + 40)  # +40 for sidebar
    
    # Sidebar (window controls area)
    sidebar_w = 70
    
    # Calculate height
    content_h = len(lines) * LINE_HEIGHT + PADDING_Y * 2
    title_h = 36  # window title bar height
    svg_height = title_h + content_h + 20  # extra bottom padding
    
    # Title bar
    title_bg_h = title_h
    
    # Start SVG
    svg = []
    svg.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;display=swap');
      text {{ font-family: {esc(FONT_FAMILY)}; font-size: {FONT_SIZE}px; }}
    </style>
    <filter id="shadow" x="-2%" y="-2%" width="104%" height="106%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <linearGradient id="title-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{SIDEBAR_BG}"/>
      <stop offset="100%" stop-color="{TITLE_BG}"/>
    </linearGradient>
  </defs>
  <!-- Terminal window shadow -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" fill="{WINDOW_BG}" filter="url(#shadow)"/>
  
  <!-- Title bar -->
  <rect x="0" y="0" width="{svg_width}" height="{title_bg_h}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" fill="url(#title-grad)"/>
  <rect x="0" y="{title_bg_h - CORNER_RADIUS}" width="{svg_width}" height="{CORNER_RADIUS}" fill="{TITLE_BG}"/>
  
  <!-- Window controls -->
  <circle cx="22" cy="18" r="6" fill="#f38ba8"/>
  <circle cx="40" cy="18" r="6" fill="#f9e2af"/>
  <circle cx="58" cy="18" r="6" fill="#a6e3a1"/>
  
  <!-- Title text -->
  <text x="{svg_width / 2}" y="24" fill="{DIM}" font-size="12" text-anchor="middle" font-family="{esc(FONT_FAMILY)}">{esc(WINDOW_TITLE)}</text>
  
  <!-- Content area -->
  <g transform="translate({sidebar_w}, {title_h + PADDING_Y})">
''')
    
    current_y = 0
    for line_idx, line in enumerate(lines):
        # Process ANSI escapes
        spans = ansi_to_svg(line)
        x_pos = 0
        
        # Check if line is a box-drawing line (contains special characters)
        any(c in line for c in '╭╮╰╯├┤│─┌┐└┘')
        
        for span in spans:
            if span[0] == 'span':
                continue
            elif span[0] == 'text':
                text_content = span[1]
                color = span[2] if len(span) > 2 else TEXT_COLOR
                bg_color = span[3] if len(span) > 3 else None
                bold = span[4] if len(span) > 4 else False
                
                if text_content.strip() or text_content == ' ':
                    if bg_color:
                        text_w = len(text_content) * char_width
                        svg.append(f'    <rect x="{x_pos:.1f}" y="{current_y - 3}" width="{text_w:.1f}" height="{LINE_HEIGHT}" fill="{bg_color}" rx="2"/>\n')
                    
                    font_weight = "700" if bold else "400"
                    svg.append(f'    <text x="{x_pos:.1f}" y="{current_y + FONT_SIZE - 3}" fill="{color}" font-weight="{font_weight}">{esc(text_content)}</text>\n')
                x_pos += len(text_content) * char_width
        
        current_y += LINE_HEIGHT
    
    svg.append('  </g>\n')
    svg.append('</svg>')
    
    return ''.join(svg)


# ── screenshot definitions ─────────────────────────────────────────────────

def screenshot_goalkit_help():
    """goalkit --help output"""
    lines = [
        "",
        "      ######    #######     ###    ##             ##    ## #### ########",
        "      ##    ##  ##     ##   ## ##   ##             ##   ##   ##     ##  ",
        "      ##        ##     ##  ##   ##  ##             ##  ##    ##     ##  ",
        "      ##   #### ##     ## ##     ## ##             #####     ##     ##  ",
        "      ##    ##  ##     ## ######### ##             ##  ##    ##     ##  ",
        "      ##    ##  ##     ## ##     ## ##             ##   ##   ##     ##  ",
        "       ######    #######  ##     ## ########       ##    ## ####    ##  ",
        "",
        "             Goal Kit - Goal-Driven Development Toolkit",
        "",
        "╭─────────────────── Goal Kit Project Detected ────────────────────╮",
        "│                                                                  │",
        "│  Project: goal-kit                                               │",
        "│  Phase: Setup                                                    │",
        "│  Health Score: 0.0/100                                           │",
        "│  Completion: 0.0%                                                │",
        "│                                                                  │",
        "│  Goals: 0  |  Milestones: 0/0                                    │",
        "│                                                                  │",
        "╰──────────────────────────────────────────────────────────────────╯",
        "",
        " Usage: goalkit [OPTIONS] COMMAND [ARGS]...",
        "",
        " Goal-Driven Development tool for AI agents.",
        " Use /goalkit.* commands through your AI agent for the main workflow.",
        "",
        "╭─ Options ────────────────────────────────────────────────────────╮",
        "│  --help   Show this message and exit.                            │",
        "╰──────────────────────────────────────────────────────────────────╯",
        "╭─ Commands ───────────────────────────────────────────────────────╮",
        "│  init           Initialize a new Goalkit project                 │",
        "│  check          Check that all required tools are installed      │",
        "│  status         Display project status and health information    │",
        "│  milestones     Display milestone progress and history           │",
        "│  metrics        Display project metrics and health trends        │",
        "│  tasks          Display and manage project tasks                 │",
        "│  report         Display project reports and metrics              │",
        "│  insights       Display actionable insights                      │",
        "│  dependencies   Manage task dependencies and critical paths      │",
        "│  projects       Manage multiple projects in a workspace          │",
        "│  export         Export project data in multiple formats          │",
        "│  analytics      Analytics, trends, and forecasting               │",
        "│  webhooks       Webhook management and event notifications       │",
        "╰──────────────────────────────────────────────────────────────────╯",
        "",
    ]
    return lines


def screenshot_check():
    """goalkit check output"""
    lines = [
        "",
        "      ######    #######     ###    ##             ##    ## #### ########",
        "      ##    ##  ##     ##   ## ##   ##             ##   ##   ##     ##  ",
        "      ##        ##     ##  ##   ##  ##             ##  ##    ##     ##  ",
        "      ##   #### ##     ## ##     ## ##             #####     ##     ##  ",
        "      ##    ##  ##     ## ######### ##             ##  ##    ##     ##  ",
        "      ##    ##  ##     ## ##     ## ##             ##   ##   ##     ##  ",
        "       ######    #######  ##     ## ########       ##    ## ####    ##  ",
        "",
        "             Goal Kit - Goal-Driven Development Toolkit",
        "",
        "╭─────────────────── Goal Kit Project Detected ────────────────────╮",
        "│                                                                  │",
        "│  Project: goal-kit                                               │",
        "│  Phase: Setup                                                    │",
        "│  Health Score: 0.0/100                                           │",
        "│  Completion: 0.0%                                                │",
        "│                                                                  │",
        "│  Goals: 0  |  Milestones: 0/0                                    │",
        "│                                                                  │",
        "╰──────────────────────────────────────────────────────────────────╯",
        "",
        "  Checking for installed tools...",
        "",
        "  ◆ Check Available Tools",
        "    ├── ✓ Git version control (available)",
        "    ├── ✗ GitHub Copilot (not found)",
        "    ├── ✗ Claude Code (not found)",
        "    ├── ✗ Gemini CLI (not found)",
        "    ├── ✗ Cursor (not found)",
        "    ├── ✓ Qwen Code (available)",
        "    ├── ✓ opencode (available)",
        "    ├── ✗ Codex CLI (not found)",
        "    ├── ✗ Windsurf (not found)",
        "    ├── ✗ Kilo Code (not found)",
        "    ├── ✗ Auggie CLI (not found)",
        "    ├── ✗ CodeBuddy (not found)",
        "    ├── ✗ Roo Code (not found)",
        "    ├── ✗ Amazon Q (not found)",
        "    ├── ✗ VS Code (not found)",
        "    └── ✗ VS Code Insiders (not found)",
        "",
        "  ✓ Goalkit CLI is ready to use!",
        "",
    ]
    return lines


def screenshot_status():
    """goalkit status output"""
    lines = [
        "",
        "      ######    #######     ###    ##             ##    ## #### ########",
        "      ##    ##  ##     ##   ## ##   ##             ##   ##   ##     ##  ",
        "      ##        ##     ##  ##   ##  ##             ##  ##    ##     ##  ",
        "      ##   #### ##     ## ##     ## ##             #####     ##     ##  ",
        "      ##    ##  ##     ## ######### ##             ##  ##    ##     ##  ",
        "      ##    ##  ##     ## ##     ## ##             ##   ##   ##     ##  ",
        "       ######    #######  ##     ## ########       ##    ## ####    ##  ",
        "",
        "             Goal Kit - Goal-Driven Development Toolkit",
        "",
        "╭─────────────────── Goal Kit Project Detected ────────────────────╮",
        "│                                                                  │",
        "│  Project: goal-kit                                               │",
        "│  Phase: Setup                                                    │",
        "│  Health Score: 0.0/100                                           │",
        "│  Completion: 0.0%                                                │",
        "│                                                                  │",
        "│  Goals: 0  |  Milestones: 0/0                                    │",
        "│                                                                  │",
        "╰──────────────────────────────────────────────────────────────────╯",
        "",
        "  ╭──────────╮",
        "  │ goal-kit │",
        "  ╰──────────╯",
        "  ╭───── Status ─────╮",
        "  │                  │",
        "  │  Phase: Setup    │",
        "  │  Completion: 0%  │",
        "  │  Health: 0.0/100 │",
        "  │                  │",
        "  ╰──────────────────╯",
        "",
        "  💡 Insights",
        "    • Focus on making progress — break down goals into smaller milestones",
        "    • Define success metrics for goals to improve tracking",
        "",
        "  ⚠️  Concerns",
        "    • Health score is below critical threshold",
        "",
        "  ✓ Strengths",
        "    • Most goals have defined metrics for tracking",
        "",
        "  Goals (0)",
        "    No goals found",
        "",
    ]
    return lines


# ── main ───────────────────────────────────────────────────────────────────

def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "screenshots")
    os.makedirs(output_dir, exist_ok=True)

    screenshots = [
        ("goalkit-help.svg", screenshot_goalkit_help(), 820, "goalkit --help"),
        ("goalkit-check.svg", screenshot_check(), 820, "goalkit check"),
        ("goalkit-status.svg", screenshot_status(), 820, "goalkit status"),
    ]

    for filename, lines, width, title in screenshots:
        global WINDOW_TITLE
        original_title = WINDOW_TITLE
        WINDOW_TITLE = f"{title} — terminal"
        svg_content = generate_svg(lines, filename, width=width)
        WINDOW_TITLE = original_title
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"Created: {filepath} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
