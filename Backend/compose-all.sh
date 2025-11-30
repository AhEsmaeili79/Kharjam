#!/usr/bin/env bash
set -euo pipefail

# Orchestrate docker compose actions across services in order.
# Order: system_service -> others
#
# Usage:
#   ./compose-all.sh up
#   ./compose-all.sh build
#   ./compose-all.sh down
#   ./compose-all.sh up-build     # same as: docker compose up --build -d
#   ./compose-all.sh ps           # optional: show status for each service
#
# Optional flags:
#   --no-cache   (for build or up-build)
#   --pull       (for build or up-build)
#
# Notes:
# - Works with both "docker compose" (v2) and legacy "docker-compose".
# - Runs each service one-by-one from its directory if a compose file exists.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect docker compose command
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  echo "Error: docker compose not found. Install Docker with Compose v2 or docker-compose." >&2
  exit 1
fi

ACTION="${1:-}"
shift || true

if [[ -z "${ACTION}" ]]; then
  echo "Usage: $(basename "$0") {up|build|down|up-build|ps} [--no-cache] [--pull]" >&2
  exit 1
fi

# Service order: system sub-services first, then the rest
SERVICES=(
  "system_service/redis"
  "system_service/rabbitmq"
  "system_service/nginx"
  "communication_service"
  "user_service"
  "split_service"
)

# Recognize common compose filenames
has_compose_file() {
  local dir="$1"
  [[ -f "${dir}/docker-compose.yml" || -f "${dir}/docker-compose.yaml" || -f "${dir}/compose.yml" || -f "${dir}/compose.yaml" ]]
}

run_in_service_dir() {
  local service_dir="$1"
  shift
  ( cd "${service_dir}" && "${COMPOSE[@]}" "$@" )
}

do_up() {
  local extra_args=("$@")
  for svc in "${SERVICES[@]}"; do
    local path="${SCRIPT_DIR}/${svc}"
    if has_compose_file "${path}"; then
      echo "==> Bringing up ${svc}..."
      run_in_service_dir "${path}" up -d "${extra_args[@]}"
    else
      echo "-- Skipping ${svc}: no compose file found"
    fi
  done
}

do_build() {
  local extra_args=("$@")
  for svc in "${SERVICES[@]}"; do
    local path="${SCRIPT_DIR}/${svc}"
    if has_compose_file "${path}"; then
      echo "==> Building ${svc}..."
      run_in_service_dir "${path}" build "${extra_args[@]}"
    else
      echo "-- Skipping ${svc}: no compose file found"
    fi
  done
}

do_down() {
  for svc in "${SERVICES[@]}"; do
    local path="${SCRIPT_DIR}/${svc}"
    if has_compose_file "${path}"; then
      echo "==> Stopping and removing ${svc}..."
      run_in_service_dir "${path}" down
    else
      echo "-- Skipping ${svc}: no compose file found"
    fi
  done
}

do_ps() {
  for svc in "${SERVICES[@]}"; do
    local path="${SCRIPT_DIR}/${svc}"
    if has_compose_file "${path}"; then
      echo "==> Status for ${svc}:"
      run_in_service_dir "${path}" ps
      echo
    fi
  done
}

# Parse optional flags for build-related actions
BUILD_FLAGS=()
while [[ "${1:-}" == --* ]]; do
  case "$1" in
    --no-cache) BUILD_FLAGS+=("--no-cache"); shift ;;
    --pull)     BUILD_FLAGS+=("--pull"); shift ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

case "${ACTION}" in
  up)
    do_up
    ;;
  build)
    do_build "${BUILD_FLAGS[@]}"
    ;;
  down)
    do_down
    ;;
  up-build|rebuild)
    # Equivalent to: build [flags] then up -d; but we can just use up --build -d
    do_up --build "${BUILD_FLAGS[@]}"
    ;;
  ps|status)
    do_ps
    ;;
  *)
    echo "Unknown action: ${ACTION}" >&2
    echo "Usage: $(basename "$0") {up|build|down|up-build|ps} [--no-cache] [--pull]" >&2
    exit 1
    ;;
esac

echo "Done."


