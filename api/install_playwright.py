# api/install_playwright.py
import os
import subprocess

# Install Playwright and browsers
subprocess.run(["pip", "install", "-r", "requirements.txt"])
subprocess.run(["playwright", "install"])
subprocess.run(["playwright", "install-deps"])

# Optionally, add additional configuration or commands as needed
