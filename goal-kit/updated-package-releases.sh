#!/bin/bash
# Goal-Kit Release Packaging Script
# Packages Goal-Kit templates for different AI agents following spec-kit's agent-specific approach
# Usage: updated-package-releases.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS and/or SCRIPTS env vars to limit what gets built.
#     AGENTS  : space or comma separated subset of: claude gemini copilot cursor qwen opencode windsurf codex kilocode auggie roo (default: all)
#     SCRIPTS : space or comma separated subset of: sh ps (default: both)
#   Examples:
#     AGENTS=claude SCRIPTS=sh ./updated-package-releases.sh v0.2.0
#     AGENTS=\"copilot,gemini\" ./updated-package-releases.sh v0.2.0
#     SCRIPTS=ps ./updated-package-releases.sh v0.2.0

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo \"Usage: $0 <version-with-v-prefix>\" >&2
  exit 1
fi
NEW_VERSION=\"$1\"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\\.[0-9]+\\.[0-9]+$ ]]; then
  echo \"Version must look like v0.0.0\" >&2
  exit 1
fi

echo \"Building Goal-Kit release packages for $NEW_VERSION\"

# Configuration
REPO_ROOT=\"$(git rev-parse --show-toplevel 2>/dev/null || pwd)\"
RELEASE_DIR=\"$REPO_ROOT/releases\"
GOAL_KIT_DIR=\"$REPO_ROOT/goal-kit\"

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

# Logging
log_info()    { echo -e \"${BLUE}[INFO]${NC} $1\"; }
log_success() { echo -e \"${GREEN}[SUCCESS]${NC} $1\"; }
log_warning() { echo -e \"${YELLOW}[WARNING]${NC} $1\"; }
log_error()   { echo -e \"${RED}[ERROR]${NC} $1\"; }

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=\".genreleases\"
mkdir -p \"$GENRELEASES_DIR\"
rm -rf \"$GENRELEASES_DIR\"/* || true

# Function to rewrite paths to goalify structure
rewrite_paths() {
  sed -E \\
    -e 's@(/?)templates/@.goalify/templates/@g' \\
    -e 's@(/?)scripts/@.goalify/scripts/@g' \\
    -e 's@(/?)memory/@.goalify/memory/@g'
}

# Function to generate commands for each agent
generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  mkdir -p \"$output_dir\"
  
  # Process each command template
  for template in \"$GOAL_KIT_DIR/templates/commands/\"*.md; do
    [[ -f \"$template\" ]] || continue
    local name description script_command body
    name=$(basename \"$template\" .md)
    
    # Normalize line endings
    file_content=$(tr -d '\\r' < \"$template\")
    
    # Extract description and script command from YAML frontmatter
    description=$(printf '%s\\n' \"$file_content\" | awk '/^description:/ {sub(/^description:[[:space:]]*/, \"\"); print; exit}')
    script_command=$(printf '%s\\n' \"$file_content\" | awk -v sv=\"$script_variant\" '/^[[:space:]]*'$script_variant':[[:space:]]*/ {sub(/^[[:space:]]*'$script_variant':[[:space:]]*/, \"\"); print; exit}')
    
    if [[ -z $script_command ]]; then
      echo \"Warning: no script command found for $script_variant in $template\" >&2
      script_command=\"(Missing script command for $script_variant)\"
    fi
    
    # Replace {SCRIPT} placeholder with the script command
    body=$(printf '%s\\n' \"$file_content\" | sed \"s|{SCRIPT}|${script_command}|g\")
    
    # Remove the scripts: section from frontmatter while preserving YAML structure
    body=$(printf '%s\\n' \"$body\" | awk '
      /^---$/ { print; if (++dash_count == 1) in_frontmatter=1; else in_frontmatter=0; next }
      in_frontmatter && /^[[:space:]]*scripts:$/ { skip_scripts=1; next }
      in_frontmatter && /^[a-zA-Z].*:/ && skip_scripts { skip_scripts=0 }
      in_frontmatter && skip_scripts && /^[[:space:]]/ { next }
      { print }
    ')
    
    # Apply other substitutions
    body=$(printf '%s\\n' \"$body\" | sed \"s/{ARGS}/$arg_format/g\" | sed \"s/__AGENT__/$agent/g\" | rewrite_paths)
    
    case $ext in
      toml)
        { echo \"description = \\\"$description\\\"\"; echo; echo \"prompt = \\\"\\\"\\\"\"; echo \"$body\"; echo \"\\\"\\\"\\\"\"; } > \"$output_dir/$name.$ext\" ;;
      md)
        echo \"$body\" > \"$output_dir/$name.$ext\" ;;
      prompt.md)
        echo \"$body\" > \"$output_dir/$name.$ext\" ;;
    esac
  done
}

# Function to build for each agent and script variant
build_variant() {
  local agent=$1 script=$2
  local base_dir=\"$GENRELEASES_DIR/goal-kit-${agent}-package-${script}\"
  echo \"Building $agent ($script) package...\"
  mkdir -p \"$base_dir\"
  
  # Copy base structure but filter scripts by variant
  GOALIFY_DIR=\"$base_dir/.goalify\"
  mkdir -p \"$GOALIFY_DIR\"
  
  # Copy templates (excluding commands which are agent-specific)
  [[ -d \"$GOAL_KIT_DIR/templates\" ]] && { 
    mkdir -p \"$GOALIFY_DIR/templates\" 
    find \"$GOAL_KIT_DIR/templates\" -type f -not -path \"$GOAL_KIT_DIR/templates/commands/*\" -exec cp --parents {} \"$GOALIFY_DIR\"/ \\; 
    echo \"Copied templates -> .goalify/templates\" 
  }
  
  # Only copy the relevant script variant directory
  if [[ -d \"$GOAL_KIT_DIR/scripts\" ]]; then
    mkdir -p \"$GOALIFY_DIR/scripts\"
    case $script in
      sh)
        [[ -d \"$GOAL_KIT_DIR/scripts/bash\" ]] && { 
          cp -r \"$GOAL_KIT_DIR/scripts/bash\" \"$GOALIFY_DIR/scripts/\"; 
          echo \"Copied scripts/bash -> .goalify/scripts\" 
        }
        # Copy any script files that aren't in variant-specific directories
        find \"$GOAL_KIT_DIR/scripts\" -maxdepth 1 -type f -exec cp {} \"$GOALIFY_DIR/scripts/\" \\; 2>/dev/null || true
        ;;
      ps)
        [[ -d \"$GOAL_KIT_DIR/scripts/powershell\" ]] && { 
          cp -r \"$GOAL_KIT_DIR/scripts/powershell\" \"$GOALIFY_DIR/scripts/\"; 
          echo \"Copied scripts/powershell -> .goalify/scripts\" 
        }
        # Copy any script files that aren't in variant-specific directories
        find \"$GOAL_KIT_DIR/scripts\" -maxdepth 1 -type f -exec cp {} \"$GOALIFY_DIR/scripts/\" \\; 2>/dev/null || true
        ;;
    esac
  fi
  
  # Agent-specific command generation
  case $agent in
    claude)
      mkdir -p \"$base_dir/.claude/commands\"
      generate_commands claude md \"\\$ARGUMENTS\" \"$base_dir/.claude/commands\" \"$script\" ;;
    gemini)
      mkdir -p \"$base_dir/.gemini/commands\"
      generate_commands gemini toml \"{{args}}\" \"$base_dir/.gemini/commands\" \"$script\"
      [[ -f \"$GOAL_KIT_DIR/agent_templates/gemini/GEMINI.md\" ]] && cp \"$GOAL_KIT_DIR/agent_templates/gemini/GEMINI.md\" \"$base_dir/GEMINI.md\" ;;
    copilot)
      mkdir -p \"$base_dir/.github/prompts\"
      generate_commands copilot prompt.md \"\\$ARGUMENTS\" \"$base_dir/.github/prompts\" \"$script\" ;;
    cursor)
      mkdir -p \"$base_dir/.cursor/commands\"
      generate_commands cursor md \"\\$ARGUMENTS\" \"$base_dir/.cursor/commands\" \"$script\" ;;
    qwen)
      mkdir -p \"$base_dir/.qwen/commands\"
      generate_commands qwen toml \"{{args}}\" \"$base_dir/.qwen/commands\" \"$script\"
      [[ -f \"$GOAL_KIT_DIR/agent_templates/qwen/QWEN.md\" ]] && cp \"$GOAL_KIT_DIR/agent_templates/qwen/QWEN.md\" \"$base_dir/QWEN.md\" ;;
    opencode)
      mkdir -p \"$base_dir/.opencode/command\"
      generate_commands opencode md \"\\$ARGUMENTS\" \"$base_dir/.opencode/command\" \"$script\" ;;
    windsurf)
      mkdir -p \"$base_dir/.windsurf/workflows\"
      generate_commands windsurf md \"\\$ARGUMENTS\" \"$base_dir/.windsurf/workflows\" \"$script\" ;;
    codex)
      mkdir -p \"$base_dir/.codex/prompts\"
      generate_commands codex md \"\\$ARGUMENTS\" \"$base_dir/.codex/prompts\" \"$script\" ;;
    kilocode)
      mkdir -p \"$base_dir/.kilocode/workflows\"
      generate_commands kilocode md \"\\$ARGUMENTS\" \"$base_dir/.kilocode/workflows\" \"$script\" ;;
    auggie)
      mkdir -p \"$base_dir/.augment/commands\"
      generate_commands auggie md \"\\$ARGUMENTS\" \"$base_dir/.augment/commands\" \"$script\" ;;
    roo)
      mkdir -p \"$base_dir/.roo/commands\"
      generate_commands roo md \"\\$ARGUMENTS\" \"$base_dir/.roo/commands\" \"$script\" ;;
  esac

  # Create the zip file
  ( cd \"$base_dir\" && zip -r \"$GENRELEASES_DIR/goal-kit-template-${agent}-${script}-${NEW_VERSION}.zip\" . )
  echo \"Created $GENRELEASES_DIR/goal-kit-template-${agent}-${script}-${NEW_VERSION}.zip\"
}

# Determine agent list
ALL_AGENTS=(claude gemini copilot cursor qwen opencode windsurf codex kilocode auggie roo)
ALL_SCRIPTS=(sh ps)

norm_list() {
  # convert comma+space separated -> space separated unique while preserving order of first occurrence
  tr ',\\n' '  ' | awk '{for(i=1;i<=NF;i++){if(!seen[$i]++){printf((out?\" \":\"\") $i)}}}END{printf(\"\\n\")}'
}

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=(\"$@\")

  local ok=1
  for it in \"${items[@]}\"; do
    local found=0
    for a in \"${allowed[@]}\"; do [[ $it == \"$a\" ]] && { found=1; break; }; done
    if [[ $found -eq 0 ]]; then
      echo \"Error: unknown $type '$it' (allowed: ${allowed[*]})\" >&2
      ok=0
    fi
  done
  return $ok
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' \"$AGENTS\" | norm_list)
  validate_subset agent ALL_AGENTS \"${AGENT_LIST[@]}\" || exit 1
else
  AGENT_LIST=(\"${ALL_AGENTS[@]}\")
fi

if [[ -n ${SCRIPTS:-} ]]; then
  mapfile -t SCRIPT_LIST < <(printf '%s' \"$SCRIPTS\" | norm_list)
  validate_subset script ALL_SCRIPTS \"${SCRIPT_LIST[@]}\" || exit 1
else
  SCRIPT_LIST=(\"${ALL_SCRIPTS[@]}\")
fi

echo \"Agents: ${AGENT_LIST[*]}\"
echo \"Scripts: ${SCRIPT_LIST[*]}\"

# Create release directory
mkdir -p \"$RELEASE_DIR\"

# Build packages for each agent and script variant
for agent in \"${AGENT_LIST[@]}\"; do
  for script in \"${SCRIPT_LIST[@]}\"; do
    build_variant \"$agent\" \"$script\"
  done
done

# Move generated packages to releases directory
mv \"$GENRELEASES_DIR\"/goal-kit-template-*-\"${NEW_VERSION}\".zip \"$RELEASE_DIR\"/

echo \"Archives in $RELEASE_DIR:\"
ls -1 \"$RELEASE_DIR\"/goal-kit-template-*-v\"${NEW_VERSION}\".zip

log_success \"Goal-Kit release packaging completed for $NEW_VERSION!\"