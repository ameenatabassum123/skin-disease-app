#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r SkinDisease/requirements.txt

# Collect static files
python SkinDisease/manage.py collectstatic --noinput

# Run migrations
python SkinDisease/manage.py migrate