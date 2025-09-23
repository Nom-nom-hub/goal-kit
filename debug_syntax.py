#!/usr/bin/env python3
"""
Debug script to find the exact syntax error in the cicd.py file
"""

file_path = r'C:\Users\Kaiden\Desktop\goal-dev-spec\src\goal_cli\cicd.py'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    compile(content, file_path, 'exec')
    print("No syntax error found")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    lines = content.splitlines()
    start = max(0, e.lineno - 6)
    end = min(len(lines), e.lineno + 5)
    for i in range(start, end):
        marker = ">>> " if i == e.lineno - 1 else "    "
        print(f"{marker}{i+1:3d}: {repr(lines[i])}")
except Exception as e:
    print(f"Other error: {e}")