#!/usr/bin/env bash

set -e

ACTION=$1

precheck() {
  echo "=== PRECHECK ==="
  echo "Operating System: $(uname -s)"
  echo "Version: $(uname -r)"

  # Check uv
  if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv..."
    pip install uv
  else
    echo "uv is installed."
  fi

  # Check pyenv
  if ! command -v pyenv &> /dev/null; then
    echo "pyenv not found. Installing pyenv..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      curl -fsSL https://pyenv.run | bash
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      brew install pyenv
    else
      echo "Unsupported OS for automatic pyenv install."
    fi
  else
    echo "pyenv is installed."
  fi

  # Check .python-version
  if [ ! -f ".python-version" ]; then
    echo "Warning: .python-version not found. Creating with default 3.14.4"
    echo "3.14.4" > .python-version
  else
    echo ".python-version exists."
  fi

  # Ensure Python version installed
  PYVER=$(cat .python-version)
  if ! pyenv versions --bare | grep -q "$PYVER"; then
    echo "Installing Python $PYVER via pyenv..."
    pyenv install "$PYVER"
  else
    echo "Python $PYVER already installed."
  fi
}

init() {
  echo "=== INIT ==="
  PYVER=$(cat .python-version)
  echo "Using Python version $PYVER"

  if [ ! -d ".venv" ]; then
    echo "Creating hidden virtual environment .venv with uv..."
    uv venv .venv
  fi

  echo "Activating environment..."
  source .venv/bin/activate
}

update() {
  echo "=== UPDATE ==="
  if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found!"
    exit 1
  fi
  echo "Installing packages with uv..."
  uv pip install -r requirements.txt
  uv pip freeze > requirements.lock
  echo "Snapshot saved to requirements.lock"
}

reset() {
  echo "=== RESET ==="
  if [ ! -f "requirements.lock" ]; then
    echo "requirements.lock not found!"
    exit 1
  fi
  echo "Uninstalling packages from snapshot..."
  while read -r pkg; do
    uv pip uninstall -y "$pkg"
  done < requirements.lock
  echo "Environment reset complete."
}

help() {
  echo "=== HELP ==="
  echo "Usage: $0 {precheck|init|update|reset|help}"
  echo
  echo "Options:"
  echo "  precheck   - Verify OS, uv, pyenv, .python-version, and ensure Python version is installed."
  echo "  init       - Create hidden .venv using uv venv and activate it."
  echo "  update     - Install packages from requirements.txt using uv and save snapshot to requirements.lock."
  echo "  reset      - Uninstall all packages listed in requirements.lock from the current environment."
  echo "  help       - Show this usage guide."
}

case "$ACTION" in
  precheck) precheck ;;
  init) init ;;
  update) update ;;
  reset) reset ;;
  help) help ;;
  *)
    echo "Invalid option. Use: $0 {precheck|init|update|reset|help}"
    exit 1
    ;;
esac
