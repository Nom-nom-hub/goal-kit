#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Goal Kit template release archives for each supported AI assistant and script type.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS and/or SCRIPTS env vars to limit what gets built.
#     AGENTS  : space or comma separated subset of: claude gemini copilot cursor qwen opencode windsurf codex kilocode auggie roo q (default: all)
#     SCRIPTS : space or comma separated subset of: sh ps (default: both)
#   Examples:
#     AGENTS=claude SCRIPTS=sh $0 v0.2.0
#     AGENTS="copilot,gemini" $0 v0.2.0
#     SCRIPTS=ps $0 v0.2.0

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi

NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  sed -E \
    -e 's@\.goalkit/@__TEMP_GOALKIT__/@g' \
    -e 's@(^|[^.])memory/@\1.goalkit/memory/@g' \
    -e 's@(^|[^.])scripts/@\1.goalkit/scripts/@g' \
    -e 's@(^|[^.])templates/@\1.goalkit/templates/@g' \
    -e 's@__TEMP_GOALKIT__/@.goalkit/@g'
}

generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  mkdir -p "$output_dir"
  for template in templates/commands/*.md; do
    [[ -f "$template" ]] || continue
    local name description script_command agent_script_command body
    name=$(basename "$template" .md)

    file_content=$(tr -d '\r' < "$template")
    description=$(awk '/^description:/ {sub(/^description:[[:space:]]*/, ""); print; exit}' <<< "$file_content")
    script_command=$(awk -v sv="$script_variant" '$0 ~ sv ":" {sub(sv ":[[:space:]]*", ""); print; exit}' <<< "$file_content")

    [[ -z $script_command ]] && script_command="(Missing script command for $script_variant)"

    agent_script_command=$(awk -v sv="$script_variant" '
      /^agent_scripts:/ { in_agent_scripts=1; next }
      in_agent_scripts && $0 ~ sv ":" { sub(sv ":[[:space:]]*", ""); print; exit }
      in_agent_scripts && /^[a-zA-Z]/ { in_agent_scripts=0 }
    ' <<< "$file_content")

    body=$(sed "s|{SCRIPT}|${script_command}|g" <<< "$file_content")
    [[ -n $agent_script_command ]] && body=$(sed "s|{AGENT_SCRIPT}|${agent_script_command}|g" <<< "$body")
    body=$(sed "s|{ARGS}|$arg_format|g; s|__AGENT__|$agent|g" <<< "$body" | rewrite_paths)

    case $ext in
      toml)
        {
          echo "description = \"${description}\""
          echo
          echo "prompt = \"\"\""
          echo "$body"
          echo "\"\"\""
        } > "$output_dir/goalkit.$name.$ext"
        ;;
      md|prompt.md)
        echo "$body" > "$output_dir/goalkit.$name.$ext"
        ;;
    esac
  done
}

build_variant() {
  local agent=$1 script=$2
  local base_dir="$GENRELEASES_DIR/gdd-${agent}-package-${script}"
  echo "Building $agent ($script) package..."
  mkdir -p "$base_dir"

  GOALKIT_DIR="$base_dir/.goalkit"
  mkdir -p "$GOALKIT_DIR"

  [[ -d memory ]] && { cp -r memory "$GOALKIT_DIR/"; echo "Copied memory -> .goalkit"; }

  if [[ -d scripts ]]; then
    mkdir -p "$GOALKIT_DIR/scripts"
    case $script in
      sh)
        [[ -d scripts/bash ]] && cp -r scripts/bash/* "$GOALKIT_DIR/scripts/" 2>/dev/null && echo "Copied scripts/bash -> .goalkit/scripts"
        find scripts -maxdepth 1 -type f -exec cp {} "$GOALKIT_DIR/scripts/" \; 2>/dev/null || true
        ;;
      ps)
        [[ -d scripts/powershell ]] && cp -r scripts/powershell/* "$GOALKIT_DIR/scripts/" 2>/dev/null && echo "Copied scripts/powershell -> .goalkit/scripts"
        find scripts -maxdepth 1 -type f -exec cp {} "$GOALKIT_DIR/scripts/" \; 2>/dev/null || true
        ;;
    esac
  fi

  [[ -d templates ]] && {
    mkdir -p "$GOALKIT_DIR/templates"
    find templates -type f -not -path "templates/commands/*" -not -name "vscode-settings.json" -exec cp --parents {} "$GOALKIT_DIR"/ \;
    echo "Copied templates -> .goalkit/templates"
  }

  case $agent in
    claude) mkdir -p "$base_dir/.claude/commands"; generate_commands claude md "\$ARGUMENTS" "$base_dir/.claude/commands" "$script" ;;
    gemini) mkdir -p "$base_dir/.gemini/commands"; generate_commands gemini toml "{{args}}" "$base_dir/.gemini/commands" "$script"; [[ -f agent_templates/gemini/GEMINI.md ]] && cp agent_templates/gemini/GEMINI.md "$base_dir/GEMINI.md" ;;
    copilot) mkdir -p "$base_dir/.github/prompts"; generate_commands copilot prompt.md "\$ARGUMENTS" "$base_dir/.github/prompts" "$script"; mkdir -p "$base_dir/.vscode"; [[ -f templates/vscode-settings.json ]] && cp templates/vscode-settings.json "$base_dir/.vscode/settings.json" ;;
    cursor) mkdir -p "$base_dir/.cursor/commands"; generate_commands cursor md "\$ARGUMENTS" "$base_dir/.cursor/commands" "$script" ;;
    qwen) mkdir -p "$base_dir/.qwen/commands"; generate_commands qwen toml "{{args}}" "$base_dir/.qwen/commands" "$script"; [[ -f agent_templates/qwen/QWEN.md ]] && cp agent_templates/qwen/QWEN.md "$base_dir/QWEN.md" ;;
    opencode) mkdir -p "$base_dir/.opencode/command"; generate_commands opencode md "\$ARGUMENTS" "$base_dir/.opencode/command" "$script" ;;
    windsurf) mkdir -p "$base_dir/.windsurf/workflows"; generate_commands windsurf md "\$ARGUMENTS" "$base_dir/.windsurf/workflows" "$script" ;;
    codex) mkdir -p "$base_dir/.codex/prompts"; generate_commands codex md "\$ARGUMENTS" "$base_dir/.codex/prompts" "$script" ;;
    kilocode) mkdir -p "$base_dir/.kilocode/workflows"; generate_commands kilocode md "\$ARGUMENTS" "$base_dir/.kilocode/workflows" "$script" ;;
    auggie) mkdir -p "$base_dir/.augment/commands"; generate_commands auggie md "\$ARGUMENTS" "$base_dir/.augment/commands" "$script" ;;
    roo) mkdir -p "$base_dir/.roo/commands"; generate_commands roo md "\$ARGUMENTS" "$base_dir/.roo/commands" "$script" ;;
    q) mkdir -p "$base_dir/.amazonq/prompts"; generate_commands q md "\$ARGUMENTS" "$base_dir/.amazonq/prompts" "$script" ;;
  esac

  ( cd "$base_dir" && zip -r "../goal-kit-template-${agent}-${script}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/goal-kit-template-${agent}-${script}-${NEW_VERSION}.zip"
}

ALL_AGENTS=(claude gemini copilot cursor qwen opencode windsurf codex kilocode auggie roo q)
ALL_SCRIPTS=(sh ps)

norm_list() { tr ',\n' '  ' | awk '{for(i=1;i<=NF;i++){if(!seen[$i]++){printf((out?" ":"") $i)}}}END{printf("\n")}' }

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=("$@")
  local ok=1
  for it in "${items[@]}"; do
    local found=0
    for a in "${allowed[@]}"; do [[ $it == "$a" ]] && { found=1; break; }; done
    [[ $found -eq 0 ]] && { echo "Error: unknown $type '$it' (allowed: ${allowed[*]})" >&2; ok=0; }
  done
  return $ok
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' "$AGENTS" | norm_list)
  validate_subset agent ALL_AGENTS "${AGENT_LIST[@]}" || exit 1
else
  AGENT_LIST=("${ALL_AGENTS[@]}")
fi

if [[ -n ${SCRIPTS:-} ]]; then
  mapfile -t SCRIPT_LIST < <(printf '%s' "$SCRIPTS" | norm_list)
  validate_subset script ALL_SCRIPTS "${SCRIPT_LIST[@]}" || exit 1
else
  SCRIPT_LIST=("${ALL_SCRIPTS[@]}")
fi

echo "Agents: ${AGENT_LIST[*]}"
echo "Scripts: ${SCRIPT_LIST[*]}"

for agent in "${AGENT_LIST[@]}"; do
  for script in "${SCRIPT_LIST[@]}"; do
    build_variant "$agent" "$script"
  done
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/goal-kit-template-*-"${NEW_VERSION}".zip
