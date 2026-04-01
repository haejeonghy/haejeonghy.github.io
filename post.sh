#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

PUSH="true"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-push)
      PUSH="false"
      shift 1
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Usage: ./post.sh [--no-push]" >&2
      exit 1
      ;;
  esac
done

if ! command -v codex >/dev/null 2>&1; then
  echo "codex command not found" >&2
  exit 1
fi

CURRENT_TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"
TMP_DIR="$(mktemp -d)"
PROMPT_FILE="$TMP_DIR/prompt.txt"
DRAFT_FILE="$TMP_DIR/draft.md"
RAW_OUTPUT_FILE="$TMP_DIR/codex-output.txt"
POST_FILE="$TMP_DIR/post.md"
COMMIT_FILE="$TMP_DIR/commit.txt"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cat > "$DRAFT_FILE"

if [[ ! -s "$DRAFT_FILE" ]]; then
  echo "No markdown content received on stdin" >&2
  exit 1
fi

echo "Converting pasted markdown and publishing post..." >&2

sed "s/__CURRENT_TIMESTAMP__/$CURRENT_TIMESTAMP/g" \
  ".codex/skills/blog-post-automation/references/exec-prompt.md" > "$PROMPT_FILE"

cat "$DRAFT_FILE" | codex exec \
  -C "$ROOT_DIR" \
  --skip-git-repo-check \
  -s workspace-write \
  -o "$RAW_OUTPUT_FILE" \
  "$(cat "$PROMPT_FILE")"

extract_section() {
  local start_marker="$1"
  local end_marker="$2"
  awk -v start="$start_marker" -v end="$end_marker" '
    $0 == start { flag=1; next }
    $0 == end { flag=0; exit }
    flag { print }
  ' "$RAW_OUTPUT_FILE"
}

FILEPATH="$(extract_section '===FILEPATH===' '===FILE===' | sed '/^[[:space:]]*$/d' | head -n 1)"
extract_section '===FILE===' '===COMMIT===' > "$POST_FILE"
awk 'found { print } $0 == "===COMMIT===" { found=1; next }' "$RAW_OUTPUT_FILE" > "$COMMIT_FILE"

if [[ -z "$FILEPATH" ]]; then
  echo "Failed to parse FILEPATH from Codex output" >&2
  cat "$RAW_OUTPUT_FILE" >&2
  exit 1
fi

if [[ ! -s "$POST_FILE" ]]; then
  echo "Failed to parse FILE content from Codex output" >&2
  cat "$RAW_OUTPUT_FILE" >&2
  exit 1
fi

if [[ ! -s "$COMMIT_FILE" ]]; then
  echo "Failed to parse COMMIT content from Codex output" >&2
  cat "$RAW_OUTPUT_FILE" >&2
  exit 1
fi

CREATE_POST_ARGS=(
  --filepath "$FILEPATH"
  --content-file "$POST_FILE"
  --commit-message-file "$COMMIT_FILE"
)

if [[ "$PUSH" == "true" ]]; then
  CREATE_POST_ARGS+=(--push)
fi

".codex/skills/blog-post-automation/scripts/create_post.sh" "${CREATE_POST_ARGS[@]}"
