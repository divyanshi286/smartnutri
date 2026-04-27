#!/bin/bash
set -e

echo "Installing Python dependencies with NO compilation..."
pip install --upgrade pip
pip install --no-cache-dir --no-build-isolation --only-binary :all: --prefer-binary -r backend/requirements.txt 2>&1 || \
pip install --no-cache-dir --prefer-binary -r backend/requirements.txt

echo "Build completed successfully!"
