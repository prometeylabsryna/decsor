#!/usr/bin/env bash
# Спільні функції для скриптів проєкту (локально та на хостингу).

set -o errexit
set -o pipefail

project_dir() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[1]:-$0}")" && pwd)"
  cd "$script_dir/.." && pwd
}

load_env_file() {
  local env_file="$1"
  if [[ ! -f "$env_file" ]]; then
    return 0
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%%#*}"
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    [[ -z "$line" ]] && continue
    [[ "$line" != *=* ]] && continue

    local key="${line%%=*}"
    local value="${line#*=}"
    key="${key%"${key##*[![:space:]]}"}"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"

    if [[ "$value" =~ ^\".*\"$ ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "$value" =~ ^\'.*\'$ ]]; then
      value="${value:1:${#value}-2}"
    fi

    if [[ -z "${!key:-}" ]]; then
      export "$key=$value"
    fi
  done < "$env_file"
}

resolve_python_bin() {
  local project_root="$1"
  local candidate="${PYTHON_BIN:-$project_root/.venv/bin/python}"
  if [[ -x "$candidate" ]]; then
    echo "$candidate"
    return 0
  fi
  command -v python3
}

ensure_log_dir() {
  local log_dir="$1"
  mkdir -p "$log_dir"
}
