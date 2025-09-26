---
description: Create and manage goal milestones with dependencies, resource allocation, and progress tracking.
scripts:
  sh: scripts/bash/update-progress.sh --json "{ARGS}"
  ps: scripts/powershell/update-progress.ps1 -Json "{ARGS}"
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

{ARGS}

The text the user typed after `/milestone` in the triggering message **is** the milestone description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that milestone description, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for MILESTONE_STATUS and PROGRESS_FILE. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load `templates/milestone-planning.md` to understand required sections.
3. Update the milestone tracking in PROGRESS_FILE using the template structure, replacing placeholders with concrete details derived from the milestone description (arguments) while preserving section order and headings.
4. Report completion with milestone file path, progress status, and next steps.

Note: The script updates the milestone progress and generates progress reports before updating the detailed milestone definition.