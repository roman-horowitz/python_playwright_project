#!/bin/bash
set -e

PROJECT_NAME="playwright-tests"
DOCKER_IMAGE="${PROJECT_NAME}:latest"

function install_local() {
  USE_VENV=$1

  if [[ "$USE_VENV" == "--with-venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment activated"
  else
    echo "Installing dependencies without virtual environment..."
  fi

  pip install --upgrade pip
  pip install -r requirements.txt
  pip install .
  playwright install
  echo "Local setup complete."
  [[ "$USE_VENV" == "--with-venv" ]] && echo "To activate: source venv/bin/activate"
}

function build_image() {
  echo "Building Docker image..."
  docker build --no-cache -t $DOCKER_IMAGE .
  echo "Docker image built: $DOCKER_IMAGE"
}

function run_in_docker() {
  echo "Running tests inside Docker..."
  shift  # remove the --docker-run flag
  docker run --rm $DOCKER_IMAGE "$@"
}

function show_help() {
  echo ""
  echo "Usage:"
  echo "  ./run_tests.sh --install-local [--with-venv|--no-venv]"
  echo "  ./run_tests.sh --docker-build"
  echo "  ./run_tests.sh --docker-run [pytest args]"
  echo ""
  echo "Examples:"
  echo "  ./run_tests.sh --install-local --with-venv"
  echo "  ./run_tests.sh --docker-build"
  echo "  ./run_tests.sh --docker-run --base-url=https://airbnb.com"
  echo ""
  exit 1
}

case $1 in
  --install-local)
    if [[ "$2" == "--with-venv" || "$2" == "--no-venv" ]]; then
      install_local "$2"
    else
      echo "Error: You must specify --with-venv or --no-venv"
      exit 1
    fi
    ;;
  --docker-build)
    build_image
    ;;
  --docker-run)
    run_in_docker "$@"
    ;;
  *)
    show_help
    ;;
esac
