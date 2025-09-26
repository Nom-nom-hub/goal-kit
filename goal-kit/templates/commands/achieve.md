---
description: Execute and complete specific goal tasks with verification and documentation.
scripts:
  sh: scripts/bash/update-progress.sh --complete "{ARGS}"
  ps: scripts/powershell/update-progress.ps1 -Complete "{ARGS}"
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

{ARGS}

The text the user typed after `/achieve` in the triggering message **is** the achievement description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that achievement description, do this:

1. Run the script `{SCRIPT}` from repo root and parse its output for ACHIEVEMENT_STATUS and VERIFICATION_FILE. All file paths must be relative to repo root.
   **IMPORTANT** You must only ever run this script once. The output is provided in the terminal - always refer to it to get the actual content you're looking for.
2. Load `templates/achievement-execution.md` to understand the required achievement tracking structure.
3. Document the achievement in VERIFICATION_FILE using the template structure, replacing placeholders with concrete details derived from the achievement description (arguments) while preserving section order and headings.
4. Report completion with achievement file path, verification status, and next steps.

Note: The script verifies task completion and updates achievement tracking before documenting the detailed achievement.