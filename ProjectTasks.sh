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
    curl -LsSf https://astral.sh/uv/install.sh | sh
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

  # Ensure pyenv is initialized
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"

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
    uv venv .venv --python "$(pyenv which python)"
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
  echo "Syncing environment to requirements.lock..."
  uv pip sync requirements.lock
  echo "Environment reset complete."
}

precommit() {
  echo "=== PRECOMMIT ==="

  # Ensure pre-commit is installed
  if ! uv run pre-commit --version &> /dev/null; then
    echo "pre-commit not found. Installing via uv..."
    uv pip install pre-commit
  fi

  # Ensure Ruff is installed
  if ! uv run ruff --version &> /dev/null; then
    echo "Ruff not found. Installing via uv..."
    uv pip install ruff
  fi

  # Generate default config if missing
  if [ ! -f ".pre-commit-config.yaml" ]; then
    echo "No .pre-commit-config.yaml found. Creating default config..."
    cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
EOF
  fi

  echo "Installing git hook..."
  uv run pre-commit install

  echo "Running pre-commit hooks via uv..."
  uv run pre-commit run --all-files
  echo "Pre-commit checks complete."
}

help() {
  echo "=== HELP ==="
  echo "Usage: $0 {precheck|init|update|reset|precommit|help}"
  echo
  echo "Options:"
  echo "  precheck   - Verify OS, uv, pyenv, .python-version, and ensure Python version is installed."
  echo "  init       - Create hidden .venv using uv venv and activate it."
  echo "  update     - Install packages from requirements.txt using uv and save snapshot to requirements.lock."
  echo "  reset      - Sync environment exactly to requirements.lock (removes extras, reinstalls missing)."
  echo "  precommit  - Ensure pre-commit and Ruff are installed, bootstrap config if missing, run hooks."
  echo "  help       - Show this usage guide."
}

case "$ACTION" in
  precheck) precheck ;;
  init) init ;;
  update) update ;;
  reset) reset ;;
  precommit) precommit ;;
  help) help ;;
  *)
    echo "Invalid option. Use: $0 {precheck|init|update|reset|precommit|help}"
    exit 1
    ;;
esac
