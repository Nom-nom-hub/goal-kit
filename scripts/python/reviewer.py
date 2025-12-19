import os
import sys
import subprocess
import re

def validate_branch_name(branch_name):
    """Ensure branch name contains only safe characters."""
    if not re.match(r"^[a-zA-Z0-9/_.-]+$", branch_name):
        raise ValueError(f"Invalid branch name: {branch_name}")
    return branch_name

def get_changed_files(base_branch="origin/main"):
    """Get list of changed files compared to base branch."""
    # Validate input to prevent injection
    try:
        safe_branch = validate_branch_name(base_branch)
    except ValueError as e:
        print(f"Security error: {e}", file=sys.stderr)
        return []

    try:
        # Inline list to satisfy security scanner
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{safe_branch}...HEAD"],
            capture_output=True, text=True, check=False, shell=False
        )
        raw = result.stdout.strip()
    except Exception as e:
        print(f"Error running git diff: {e}", file=sys.stderr)
        raw = ""
    return [f for f in raw.split('\n') if f.strip()]

def analyze_complexity(files):
    """Run radon complexity check on python files."""
    python_files = [f for f in files if f.endswith('.py') and os.path.exists(f)]
    issues = []
    
    if not python_files:
        return issues

    try:
        # Inline list construction
        result = subprocess.run(
            [sys.executable, "-m", "radon", "cc", "-s", "-n", "C"] + python_files,
            capture_output=True, text=True, check=False, shell=False
        )
        output = result.stdout.strip()
    except Exception as e:
        print(f"Error running radon: {e}", file=sys.stderr)
        output = ""
    
    if output:
        for line in output.split('\n'):
            if line.strip():
                 issues.append(f"🧠 **Complexity Alert**: `{line.strip()}`")
    
    return issues

def scan_patterns(base_branch="origin/main"):
    """Scan diff for regex patterns."""
    issues = []
    
    # Validate input
    try:
        safe_branch = validate_branch_name(base_branch)
    except ValueError:
        return []

    try:
        # Inline list construction
        result = subprocess.run(
            ["git", "diff", f"{safe_branch}...HEAD"],
            capture_output=True, text=True, check=False, shell=False
        )
        diff_output = result.stdout.strip()
    except Exception as e:
        print(f"Error running git diff contents: {e}", file=sys.stderr)
        diff_output = ""
    
    # Simple regex for patterns
    # 1. TODOs
    todo_matches = re.findall(r"^\+.*(TODO|FIXME):", diff_output, re.MULTILINE)
    if todo_matches:
        issues.append(f"📝 **Maintenance**: Found {len(todo_matches)} new `TODO` or `FIXME` comments.")

    # 2. Secrets (Basic heuristics)
    # Look for "key", "token", "secret" followed by assignment
    # Case insensitive flag (?i) must be at start, or just use re.IGNORECASE
    secret_pattern = r"^\+.*(api_?key|auth_?token|secret_?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]"
    secret_matches = re.findall(secret_pattern, diff_output, re.MULTILINE | re.IGNORECASE)
    if secret_matches:
        issues.append("🔒 **Security Warning**: Possible secret key detected in diff. Please verify.")

    return issues

def main():
    print("Starting Smart Code Review...")
    
    # We assume 'origin/main' is available. In GH actions we might need to fetch it.
    base_ref = os.environ.get("GITHUB_BASE_REF", "main")
    # GITHUB_BASE_REF is only set for PR events. 
    # Try to use origin/main as default fallback
    base = f"origin/{base_ref}" if base_ref != "main" else "origin/main"
    
    changed_files = get_changed_files(base)
    print(f"Scanning {len(changed_files)} changed files...")

    report = []
    report.append("# 🤖 Smart Code Review Summary")
    
    # 1. Complexity
    complexity_issues = analyze_complexity(changed_files)
    if complexity_issues:
        report.append("## 🧠 Complexity Analysis")
        report.append("Found code that might be too complex to maintain:")
        report.extend([f"- {i}" for i in complexity_issues])
    else:
        report.append("## 🧠 Complexity Analysis")
        report.append("✅ No high-complexity functions detected in changed files.")

    # 2. Pattern Scan
    pattern_issues = scan_patterns(base)
    if pattern_issues:
        report.append("## 🔍 Code Patterns")
        report.extend([f"- {i}" for i in pattern_issues])
    else:
        report.append("## 🔍 Code Patterns")
        report.append("✅ No concerning code patterns (TODOs, secrets) found.")

    # Write output
    with open("ai_review_summary.md", "w", encoding="utf-8") as f:
        f.write("\n\n".join(report))
    
    print("Review complete. Report generated.")

if __name__ == "__main__":
    main()
