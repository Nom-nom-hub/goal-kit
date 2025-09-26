---
description: Track and report on goal progress with metrics, achievements, and next steps.
scripts:
  sh: scripts/bash/generate-report.sh --json "{ARGS}"
  ps: scripts/powershell/generate-report.ps1 -Json "{ARGS}"
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

{ARGS}

The text the user typed after `/progress` in the triggering message **is** the progress query. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that progress query, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for PROGRESS_DATA and REPORT_FILE. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load `templates/progress-report.md` to understand required sections.
3. Generate a progress report to REPORT_FILE using the template structure, replacing placeholders with concrete details derived from the progress query (arguments) while preserving section order and headings.
4. Report completion with report file path, progress metrics, and next steps.

Note: The script aggregates progress data and generates detailed reports before writing the progress report.