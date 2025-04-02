#test functions
import os
import io
import time
import json
import base64
import config
import requests
import test_functions
from PIL import Image
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def send_test_data(name, status, message, image):
    # Headers with Authorization token from config
    headers = {
        'Authorization': f'Bearer {config.auth_token}',
        'Content-type': 'application/json'
    }

    # Prepare the data to send in the POST request
    data = {
        'name': name,
        'status': status,
        'datetime': datetime.now().isoformat(),  # Current datetime in ISO format
        'message': message,
        'image': image
    }

    # Send POST request with headers
    response = requests.post(config.auth_url, headers=headers, json=data)

    # Check the status code of the response
    if response.status_code == 201:
        print('Success!')
        print('Response Content:', response.json())  # or response.json() for JSON data
    else:
        print(f'Failed to send data. Status code: {response.status_code}')

def initialize_driver():
#    global driver  # Ensure we're modifying the global variable
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--disable-gpu")  # Helps with some headless issues
    options.add_argument("--window-size=1024,768")  # Set window size
    options.add_argument("--no-sandbox")  # Bypass OS security model (useful in Linux)
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources problems
    
    driver = webdriver.Chrome(options=options)  # Assign to the global variable
    return driver


def close_driver(driver):
    # Close the driver after the test
    driver.quit()

def click_element(driver, by, value):
    element = driver.find_element(by, value)
    element.click()

def send_keys_to_element(driver, by, value, keys):
    element = driver.find_element(by, value)
    element.send_keys(keys)

def get_element_text(driver, by, value):
    element = driver.find_element(by, value)
    return element.text

def accept_alert(driver):
    alert = driver.switch_to.alert
    alert.accept()

def dismiss_alert(driver):
    alert = driver.switch_to.alert
    alert.dismiss()

def get_alert_text(driver):
    alert = driver.switch_to.alert
    return alert.text

def switch_to_window(driver, window_index=0):
    windows = driver.window_handles
    driver.switch_to.window(windows[window_index])

def close_current_window(driver):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_to_element(driver, by, value):
    element = driver.find_element(by, value)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    
def wait_for_page_to_load(driver):
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

def wait_for_and_click(driver, by, value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    driver.find_element(by, value).click()

# Function to take a screenshot and save it to a specific directory
def take_screenshot(driver, file_name):
    # Define the directory where screenshots should be saved
    directory = r"C:\Users\JosephRahmey\scripts\screenshots"
    
    # Check if the directory exists
    print(f"Checking if directory exists: {directory}")
    if not os.path.exists(directory):
        print(f"Directory does not exist. Creating: {directory}")
        os.makedirs(directory)  # Create the directory if it doesn't exist
    else:
        print(f"Directory exists: {directory}")
    
    # Define the full file path for the screenshot
    file_path = os.path.join(directory, file_name)
    
    # Debugging: Check the file path
    print(f"Full file path to save screenshot: {file_path}")
    
    # Save the screenshot
    try:
        driver.save_screenshot(file_path)
        print(f"Screenshot successfully saved to: {file_path}")
    except Exception as e:
        print(f"Error saving screenshot: {e}")
# Define the function check_http_status before calling it


def check_page_status(driver):
    try:
        # Get the current page URL
        current_url = driver.current_url

        # Get the HTTP status code using JavaScript
        status_code = driver.execute_script("return window.performance.getEntries()[0].responseStatus || 200;")

        # Check if the status code indicates an error
        if 400 <= status_code < 600:
            print(f"Error Code: {status_code} encountered at {current_url}")
            return status_code
        else:
            print(f"Status Code: {status_code} - Everything looks fine.")
            return status_code

    except WebDriverException as e:
        print(f"Error while checking page status: {e}")
        return None
    
# Function to measure the page load time using JavaScript
def get_page_load_time(driver):
    # Execute JavaScript to get the page load time
    timing = driver.execute_script("""
        return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
    """)
    return timing


def take_small_screenshot(driver):
    # Capture the screenshot as PNG Base64
    screenshot_png = base64.b64decode(driver.get_screenshot_as_base64())

    # Open image with PIL
    image = Image.open(io.BytesIO(screenshot_png))
    
    # Resize to reduce size (adjust width/height)
    image = image.resize((800, 600))  # Example: Shrinks to 800x600

    # Convert to JPEG (smaller than PNG) and compress
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="JPEG", quality=45)  # Lower quality = smaller size

    # Convert back to Base64
    compressed_base64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")
    
    return compressed_base64