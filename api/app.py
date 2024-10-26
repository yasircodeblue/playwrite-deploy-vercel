from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time
import os
import subprocess
# Configure Imgbb
subprocess.run(["python3", "install_playwright.py"])
app = Flask(__name__)

def take_screenshot_and_upload():
    """Automate steps to take a screenshot, then upload to Imgbb."""
    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the target page
        page.goto("https://mockup.epiccraftings.com/")

        # Wait for textarea and input text
        print("Waiting for textarea...")
        page.wait_for_selector(".form-control.txt_area_1")
        textarea = page.locator(".form-control.txt_area_1")
        textarea.fill("Yasir")

        # Wait for font divs to load
        print("Processing font divs...")
        time.sleep(2)  # Allow time for page to load fully
        font_divs = page.locator("div.font-div[data-path]").all()
        for div in font_divs[:7]:  # Click the first 7 font divs
            div.click()
            time.sleep(0.5)

        # Wait for the screenshot element to be available
        print("Waiting for screenshot element...")
        screenshot_elem = page.wait_for_selector("#takeScreenShoot")

        # Take screenshot of the specified element
        time.sleep(2)  # Add delay if necessary
        screenshot_bytes = screenshot_elem.screenshot(type="png")
        print("captured")
        # # Upload screenshot to Imgbb
        # screenshot_url = upload_to_imgbb(screenshot_bytes)
        # return {"Screenshot URL": screenshot_url}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Error": str(e)}
    
    finally:
        if browser:
            browser.close()
        playwright.stop()

@app.route('/api/hey', methods=['GET'])
def home():
    if request.method == 'GET':
        result = take_screenshot_and_upload()
        return jsonify(result)

# For local development
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
