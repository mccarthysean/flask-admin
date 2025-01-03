#!/bin/bash

# Enable exit on non 0
set -e
set -x

# Set the current working directory to the directory in which the script is located, for CI/CD
cd "$(dirname "$0")"
# cd ..
echo "Current working directory: $(pwd)"

# Use Ruff to lint everything
echo ""
echo "Running ruff linter..."
# Run the linter
ruff check ../flask_admin --fix --config ../pyproject.toml
ruff check ../flask_admin/tests --fix --config ../pyproject.toml

# Run the formatter
echo ""
echo "Running ruff formatter..."
ruff format ../flask_admin --config ../pyproject.toml
ruff format ../flask_admin/tests --config ../pyproject.toml

# # Run the pyright linter (takes a bit longer)
# echo ""
# echo "Running pyright linter..."
# pyright ../flask_admin --project ../pyproject.toml
# pyright ../flask_admin/tests --project ../pyproject.toml
