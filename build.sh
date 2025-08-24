#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip to latest version
pip install --upgrade pip

# Install conservative dependencies first
pip install -r SkinDisease/requirements-conservative.txt

# Create necessary directories
mkdir -p SkinDisease/staticfiles
mkdir -p SkinDisease/media

# Collect static files
python SkinDisease/manage.py collectstatic --noinput

# Run migrations
python SkinDisease/manage.py migrate