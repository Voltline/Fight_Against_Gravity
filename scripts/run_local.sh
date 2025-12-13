#!/usr/bin/env bash
set -euo pipefail

# 简单的一键本地联机脚本：
# - 使用 settings/settings_local.json（通过 --debug / --local）强制走 127.0.0.1
# - 先起本地注册认证服，再起专用服务器，最后启动客户端

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
SERVER_LOG="${SERVER_LOG:-/tmp/fag_server.log}"
AUTH_LOG="${AUTH_LOG:-/tmp/fag_auth_server.log}"
CONFIG_FILE="${CONFIG_FILE:-settings/settings_local.json}"

read_ports() {
  python3 - <<'PY' "${CONFIG_FILE}" || exit 1
import json,sys
path = sys.argv[1]
with open(path, "r") as f:
    cfg = json.load(f)
c = cfg["Client"]
print(f"{c['Reg_Port']} {c['Game_Local_Port']} {c['Udp_Local_Port']}")
PY
}

PORTS=($(read_ports))
AUTH_PORT="${PORTS[0]}"
GAME_PORT="${PORTS[1]}"
UDP_PORT="${PORTS[2]}"

kill_port_if_busy() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    if lsof -iTCP:"${port}" -sTCP:LISTEN >/dev/null 2>&1; then
      local pids
      pids=$(lsof -tiTCP:"${port}" -sTCP:LISTEN)
      echo "Port ${port} is in use by: ${pids}. Killing..."
      sudo kill -9 ${pids} >/dev/null 2>&1 || true
      sleep 1
      if lsof -iTCP:"${port}" -sTCP:LISTEN >/dev/null 2>&1; then
        echo "Failed to free port ${port}. Please stop the process manually or adjust ${CONFIG_FILE}."
        exit 1
      fi
    fi
  fi
}

check_started() {
  local pid="$1" name="$2" log="$3"
  sleep 1
  if ! ps -p "${pid}" >/dev/null 2>&1; then
    echo "${name} failed to start. Check log: ${log}"
    tail -n 20 "${log}" 2>/dev/null || true
    exit 1
  fi
}

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]] && ps -p "${SERVER_PID}" >/dev/null 2>&1; then
    echo "Stopping local server (pid=${SERVER_PID})..."
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${AUTH_PID:-}" ]] && ps -p "${AUTH_PID}" >/dev/null 2>&1; then
    echo "Stopping auth server (pid=${AUTH_PID})..."
    kill "${AUTH_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

echo "Checking ports... auth:${AUTH_PORT} tcp:${GAME_PORT} udp:${UDP_PORT}"
kill_port_if_busy "${AUTH_PORT}"
kill_port_if_busy "${GAME_PORT}"

echo "Starting local identify/auth server (Reg_Port ${AUTH_PORT}) ..."
"${PYTHON_BIN}" Server/identify_server.py --local --debug >"${AUTH_LOG}" 2>&1 &
AUTH_PID=$!
check_started "${AUTH_PID}" "Auth server" "${AUTH_LOG}"
echo "Auth server log: ${AUTH_LOG}"

echo "Starting local game server with settings_local.json ..."
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dsp \
  "${PYTHON_BIN}" server.py --debug --nogui >"${SERVER_LOG}" 2>&1 &
SERVER_PID=$!
check_started "${SERVER_PID}" "Game server" "${SERVER_LOG}"

echo "Server log: ${SERVER_LOG}"
echo "Launching client (connects to 127.0.0.1:${GAME_PORT}) ..."
exec "${PYTHON_BIN}" main.py --debug "$@"
