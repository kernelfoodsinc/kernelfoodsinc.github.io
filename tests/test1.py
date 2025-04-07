#test1
import time
import json
import base64
import config
import requests
import test_functions
from PIL import Image
import io
from test_functions import *
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
import pickle
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium.webdriver.support.ui import Select




# Main testing function
def test_counterservice():
    url = "https://counterservice.com"
    
    # Check if the webpage returns an error code

    
 #   if error_code:  # If there's an error code between 400 and 600, we will exit the script
  #      print(f"Exiting test due to error code {error_code}.")
 #       return
#
    # If no error code, proceed with the Selenium tests
    driver = initialize_driver()
    error_code = check_page_status(driver)
    

    try:
        # Start timer to measure load time
        start_time = time.time()

        # Navigate to the website
        driver.get(url)
        print(f"Navigated to {url}")

        # Measure the page load time
        load_time = get_page_load_time(driver)
        print(f"Page load time: {load_time} ms")

       # time.sleep(20)

        # Take a screenshot of the home page
       #take_screenshot(driver, "counterservice_home_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:23] + ".png")
        #driver.save_screenshot(f"test.png")
      # print("Screenshot taken for homepage.")
        small_base64 = take_small_screenshot(driver)



        name = url
        status = error_code
        message = f"{load_time}ms"
        image = small_base64
        #print(small_base64)
        send_test_data(name, status, message, image)

        # Wait for and click a menu item or link (example: click the first menu item)
        wait_for_and_click(driver, By.XPATH, "/html/body/div/div[2]/div[1]/div/div[2]/div/a[1]/div/div")  # Example XPath for the first menu item
        print("Clicked on the first menu item.")

        # Wait for some other element to load (for example, a specific section or product)
       # wait_for_and_click(driver, By.XPATH, "//section[@id='some_section']//a[1]")  # Example XPath
      #  print("Clicked on an item in the section.")

        # Take a screenshot of the second page (after click)
        #take_screenshot(driver, "counterservice_menu_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:23] + ".png")
        print("Screenshot taken for second page.")

        error_code = check_page_status(driver)
    

        # Example: fill out a search form (if available)
      #  send_keys_to_element(driver, By.NAME, "search", "test query")
      #  print("Entered text in search field.")

        # Optionally, click on search button
       # wait_for_and_click(driver, By.XPATH, "//button[@type='submit']")  # Update with correct XPath for search button
       # print("Clicked on search button."
        small_base64 = take_small_screenshot(driver)
        url =  driver.current_url
        load_time = get_page_load_time(driver)
        print(f"Page load time: {load_time} ms")
        #time.sleep(20)

        name = url
        status = error_code
        message = f"{load_time}ms"
        image = small_base64
        send_test_data(name, status, message, image)


        order_now_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Order Now')]")
        order_now_button.click()
        switch_to_window(driver,1)
        wait_for_page_to_load(driver)
        time.sleep(3)  

        #take_screenshot(driver, "counterservice_olo_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:23] + ".png")
        print("Screenshot taken for second page.")

        error_code = check_page_status(driver)
    

        # Example: fill out a search form (if available)
      #  send_keys_to_element(driver, By.NAME, "search", "test query")
      #  print("Entered text in search field.")

        # Optionally, click on search button
       # wait_for_and_click(driver, By.XPATH, "//button[@type='submit']")  # Update with correct XPath for search button
       # print("Clicked on search button."
        small_base64 = take_small_screenshot(driver)
        url =  driver.current_url
        load_time = get_page_load_time(driver)
        print(f"Page load time: {load_time} ms")
       # time.sleep(20)                                                                

        name = url
        status = error_code
        message = f"{load_time}ms"
        image = small_base64
        send_test_data(name, status, message, image)

    except Exception as e:
        print(f"Error encountered: {e}")

    finally:
        # Close the driver
        close_driver(driver)
        print("Driver closed.")
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)

        sender = 'joseph.rahmey@kernel.inc'  # Replace with your email address
        to = 'joseph.rahmey@kernel.inc'  # Replace with the recipient's email address
        subject = 'Web Status'
        body = f'Hi there,\n\nBelow is the current status: \n{name} \n{status} \n{message}  \n\nTo check the current website status and view previous status history click here: https://kernelfoodsinc.github.io/status/'
        #attachment = 'C:\\Users\\JosephRahmey\\Downloads\\DSR_02_11_2025.pdf'  # Replace with the path to your downloaded file

    # Corrected function name here
        raw_message = create_message(sender, to, subject, body, attachments=None)
        send_message(service, sender, raw_message)  # Send the email using the send_message function

# Run the test
test_counterservice()



