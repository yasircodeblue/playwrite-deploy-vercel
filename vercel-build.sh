#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright and its dependencies
pip install playwright

# Install browsers
playwright install

# Install any necessary dependencies for running browsers in a server environment
playwright install-deps
