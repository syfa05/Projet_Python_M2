from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# This code imports the necessary module from Selenium to control a web browser.
import time
"""
driver = webdriver.Chrome()
# This code initializes a Chrome browser instance using Selenium WebDriver.
driver.get("https://www.google.com")
driver.maximize_window()
print(driver.title)
# This code navigates to the Google homepage and maximizes the browser window.

# This code opens the Google homepage in the browser.
time.sleep(11)  # Wait for 11 seconds to see the browser
driver.quit()
"""
service_obj = Service("C:/Users/fresn/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)
# This code initializes a Chrome browser instance with a specified service object.
driver.get("https://www.google.com")
driver.maximize_window()
print(driver.title)
driver.maximize_window()
# This code navigates to the Google homepage and maximizes the browser window using the service object.
time.sleep(11)  # Wait for 11 seconds to see the browser
driver.quit()
# This code closes the browser after the specified time.