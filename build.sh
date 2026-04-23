#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install --prefer-binary --no-build-isolation -r backend/requirements.txt

echo "Build completed successfully!"
