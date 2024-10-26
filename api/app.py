import cloudinary
import cloudinary.uploader
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time

# Configure Cloudinary
cloudinary.config(
    cloud_name='dsfr7nm3a',
    api_key='914261393664548',
    api_secret='7uckXI5naaQOjW8xnQ_G34YrRB0'
)

app = Flask(__name__)

def upload_to_cloudinary(image_bytes):
    """Upload an image to Cloudinary"""
    try:
        result = cloudinary.uploader.upload(
            image_bytes,
            resource_type="image",
            upload_preset="pinterest"  # Adjust to your preset
        )
        print(f"Screenshot uploaded to Cloudinary: {result['secure_url']}")
        return result['secure_url']
    except Exception as error:
        print(f"Error uploading to Cloudinary: {error}")
        raise

def take_screenshot_and_upload():
    """Automate steps and take screenshot, then upload to Cloudinary"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the target page
        page.goto("https://mockup.epiccraftings.com/")

        # Wait for textarea and input text
        print("Waiting for textarea...")
        page.wait_for_selector(".form-control.txt_area_1")
        textarea = page.locator(".form-control.txt_area_1")
        textarea.fill("Yasir")

        # Wait a moment for fonts to load and then click on font divs
        print("Processing font divs...")
        time.sleep(2)  # Allow time for page to load fully
        font_divs = page.locator("div.font-div[data-path]").nth(1).all()
        for div in font_divs[:7]:  # Click the first 7 font divs
            div.click()
            time.sleep(0.5)

        # Wait for the screenshot element to be available
        print("Waiting for screenshot element...")
        screenshot_elem = page.wait_for_selector("#takeScreenShoot")

        # Take screenshot of the specified element
        time.sleep(2)  # Add delay if necessary
        screenshot_bytes = screenshot_elem.screenshot(type="png")

        # Close the browser
        browser.close()

        # Upload screenshot to Cloudinary
        screenshot_url = upload_to_cloudinary(screenshot_bytes)
        return {"Screenshot URL": screenshot_url}

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        result = take_screenshot_and_upload()
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
