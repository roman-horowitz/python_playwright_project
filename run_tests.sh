#!/bin/bash
set -e

echo "Building Docker image..."
docker compose build

echo "Running tests..."
docker compose run --rm tests "$@"
