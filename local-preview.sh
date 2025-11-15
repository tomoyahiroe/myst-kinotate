#!/usr/bin/env bash
set -euo pipefail

# Repository root
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# GitHub Pages (カスタムドメイン) と同じプレフィックスをデフォルトにする
# ルート配信が前提なのでデフォルトは空文字（= BASE_URL 未指定）
# サブパスで確認したい場合は BASE_URL=/something を指定
BASE_URL="${BASE_URL:-}"
# プレビュー用のポート
PORT="${PORT:-8000}"
# サーバーを起動したくない場合は SERVE=0 を指定
SERVE="${SERVE:-1}"

if [[ -n "${BASE_URL}" ]]; then
  echo "[myst] Using BASE_URL='${BASE_URL}'"
else
  echo "[myst] Using BASE_URL='<unset>' (root)"
fi

cd "${ROOT_DIR}"

echo "[uv] Syncing dependencies into .venv"
uv sync

echo "[uv] Activating local virtual environment"
# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"

echo "[myst] Building static HTML"
if [[ -n "${BASE_URL}" ]]; then
  BASE_URL="${BASE_URL}" myst build --html
else
  myst build --html
fi

echo "[myst] Copying feeds into _build/html"
cp atom.xml _build/html/atom.xml
cp rss.xml _build/html/rss.xml

if [[ "${SERVE}" == "1" ]]; then
  echo "[preview] Starting local server at http://localhost:${PORT}"
  if [[ -n "${BASE_URL}" ]]; then
    echo "[preview] Open http://localhost:${PORT}${BASE_URL} で見てください (BASE_URL がサブパスのため)"
  else
    echo "[preview] Open http://localhost:${PORT}/"
  fi
  cd _build/html
  python -m http.server "${PORT}"
else
  echo "[preview] Skipping local server start (SERVE=${SERVE})"
fi
