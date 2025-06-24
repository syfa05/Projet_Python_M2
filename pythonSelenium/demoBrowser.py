from selenium import webdriver

# This code imports the necessary module from Selenium to control a web browser.
import time

driver = webdriver.Chrome()
# This code initializes a Chrome browser instance using Selenium WebDriver.
driver.get("https://www.google.com")
# This code opens the Google homepage in the browser.
time.sleep(11)  # Wait for 11 seconds to see the browser
driver.quit()