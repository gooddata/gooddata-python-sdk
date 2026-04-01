#!/usr/bin/env bash
# (C) 2026 GoodData Corporation
#
# Python validation wrapper for AIDA validate_command.
#
# Contract (streaming-first):
# - Emits human-readable progress lines to stdout.
# - Writes raw command output to stderr only when a step fails.
# - Prints the final JSON result as the last non-empty line on stdout.

set -uo pipefail

TOOL="validate_python"

json_escape() {
  local s="${1-}"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\t'/\\t}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\n'/\\n}"
  printf '%s' "$s"
}

emit_line() {
  local msg="${2-${1-}}"
  printf '%s\n' "$msg"
}

usage() {
  cat <<'EOF'
Usage:
  validate_python.sh --project-path <path> --workspace-root <path> [options]

Options:
  --scope <scope>          Validation scope: pre_commit or pre_push (default: pre_push)
                           pre_commit: format,lint,types
                           pre_push:   format,lint,types,test
  --steps-csv "<csv>"      Comma-separated steps (overrides --scope defaults)
  --auto-fix <true|false>  Default: true (uses *-fix Make targets)
  --test-filter <pattern>  Optional pytest selector (runs uv run pytest -v <pattern>)

  -h, --help               Show help
EOF
}

PROJECT_PATH=""
WORKSPACE_ROOT=""
SCOPE=""
STEPS_CSV=""
AUTO_FIX="true"
TEST_FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-path) PROJECT_PATH="${2-}"; shift 2 ;;
    --workspace-root) WORKSPACE_ROOT="${2-}"; shift 2 ;;
    --scope) SCOPE="${2-}"; shift 2 ;;
    --steps-csv) STEPS_CSV="${2-}"; shift 2 ;;
    --auto-fix) AUTO_FIX="${2-}"; shift 2 ;;
    --test-filter) TEST_FILTER="${2-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$PROJECT_PATH" || -z "$WORKSPACE_ROOT" ]]; then
  echo "Missing required args: --project-path and --workspace-root" >&2
  usage >&2
  exit 2
fi

PROJECT_NAME="$(basename "$PROJECT_PATH")"

to_bool() {
  local v="${1-}"
  v="$(printf '%s' "$v" | tr '[:upper:]' '[:lower:]')"
  case "$v" in
    1|true|yes|on) printf 'true' ;;
    *) printf 'false' ;;
  esac
}

AUTO_FIX_BOOL="$(to_bool "$AUTO_FIX")"

split_csv() {
  local csv="${1-}"
  local out=()
  local item
  IFS=',' read -r -a out <<<"$csv"
  for item in "${out[@]}"; do
    item="$(printf '%s' "$item" | xargs)"
    if [[ -n "$item" ]]; then
      printf '%s\n' "$item"
    fi
  done
}

if [[ -n "${STEPS_CSV// }" ]]; then
  mapfile -t STEPS < <(split_csv "$STEPS_CSV")
else
  case "${SCOPE}" in
    pre_commit)
      STEPS=("format" "lint" "types")
      ;;
    pre_push|"")
      STEPS=("format" "lint" "types" "test")
      ;;
    *)
      STEPS=("format" "lint" "types" "test")
      ;;
  esac
fi

if [[ ! -d "$PROJECT_PATH" ]]; then
  emit_line info "Python ${PROJECT_NAME}: project path not found: ${PROJECT_PATH}"
  printf '{"tool":"%s","success":false,"text":"%s"}\n' \
    "$(json_escape "$TOOL")" \
    "$(json_escape "project path not found: ${PROJECT_PATH}")"
  exit 1
fi

if [[ ! -f "${PROJECT_PATH%/}/Makefile" ]]; then
  emit_line info "Python ${PROJECT_NAME}: Makefile missing (required)"
  printf '{"tool":"%s","success":false,"text":"%s"}\n' \
    "$(json_escape "$TOOL")" \
    "$(json_escape "No Makefile found in ${PROJECT_PATH}")"
  exit 1
fi

run_in_project() {
  local label="$1"
  shift
  local -a cmd=("$@")
  local tmp_out
  tmp_out="$(mktemp)"

  emit_line progress "Python ${PROJECT_NAME}: ${label}"

  (cd "$PROJECT_PATH" && env -u VIRTUAL_ENV "${cmd[@]}") >"$tmp_out" 2>&1
  local rc=$?
  if [[ "$rc" -ne 0 ]]; then
    cat "$tmp_out" >&2
  fi
  rm -f "$tmp_out"
  return "$rc"
}

run_in_project_capture() {
  local label="$1"
  local out_file="$2"
  shift 2
  local -a cmd=("$@")

  emit_line progress "Python ${PROJECT_NAME}: ${label}"

  (cd "$PROJECT_PATH" && env -u VIRTUAL_ENV "${cmd[@]}") >"$out_file" 2>&1
  return $?
}

has_make_target() {
  local target="$1"
  local code
  (cd "$PROJECT_PATH" && make -q "$target" >/dev/null 2>&1)
  code=$?
  [[ $code -eq 0 || $code -eq 1 ]]
}

FAIL_STEP=""

for step in "${STEPS[@]}"; do
  case "$step" in
    format)
      if [[ "$AUTO_FIX_BOOL" == "true" ]] && has_make_target "format-fix"; then
        if ! run_in_project "Format (make format-fix)" make format-fix; then FAIL_STEP="Format"; break; fi
      else
        if ! run_in_project "Format (make format)" make format; then FAIL_STEP="Format"; break; fi
      fi
      ;;
    lint)
      if [[ "$AUTO_FIX_BOOL" == "true" ]] && has_make_target "lint-fix"; then
        if ! run_in_project "Lint (make lint-fix)" make lint-fix; then FAIL_STEP="Lint"; break; fi
      else
        if ! run_in_project "Lint (make lint)" make lint; then FAIL_STEP="Lint"; break; fi
      fi
      ;;
    types)
      tmp_types="$(mktemp)"
      if run_in_project_capture "Types (make type-check)" "$tmp_types" make type-check; then
        rm -f "$tmp_types"
      else
        cat "$tmp_types" >&2
        rm -f "$tmp_types"
        FAIL_STEP="Types"
        break
      fi
      ;;
    test)
      if [[ -n "${TEST_FILTER}" ]]; then
        if ! run_in_project "Test (pytest ${TEST_FILTER})" uv run pytest -v "$TEST_FILTER"; then
          FAIL_STEP="Test"; break
        fi
      else
        if ! run_in_project "Test (make test)" make test; then FAIL_STEP="Test"; break; fi
      fi
      ;;
    *)
      emit_line info "Python ${PROJECT_NAME}: skipping unknown step '${step}'"
      ;;
  esac
done

if [[ -n "$FAIL_STEP" ]]; then
  printf '{"tool":"%s","success":false,"text":"%s"}\n' \
    "$(json_escape "$TOOL")" \
    "$(json_escape "Python ${PROJECT_NAME}: FAILED at ${FAIL_STEP}")"
  exit 1
fi

printf '{"tool":"%s","success":true,"text":"%s"}\n' \
  "$(json_escape "$TOOL")" \
  "$(json_escape "Python ${PROJECT_NAME}: PASSED")"
exit 0
