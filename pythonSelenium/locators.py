import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


"""Class to hold locators for web elements."""
# Locators for the Google search page
service_obj = Service("C:/Users/fresn/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)
driver.get("https://rahulshettyacademy.com/angularpractice/")
#driver.maximize_window()
# Locators for the form fields
driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("syfa aubin")
driver.find_element(By.NAME, "email").send_keys("hello@gmail.com")
driver.find_element(By.ID, "exampleInputPassword1").send_keys("password123")
driver.find_element(By.ID, "exampleCheck1").click()
driver.find_element(By.ID, "exampleFormControlSelect1").send_keys("Male")
driver.find_element(By.ID, "inlineRadio2").click()
driver.find_element(By.NAME, "bday").send_keys("01/01/2000")
driver.find_element(By.XPATH, "//input[@type='submit']").click()
driver.
message= driver.find_element(By.CLASS_NAME, "alert-success").text
print(message)
assert "Success" in message


# Wait for a few seconds to see the result



# This code defines a class `Locators` that contains locators for web elements on a form.
# It uses Selenium to interact with the web page, filling out a form and submitting it.
# The browser is closed after a specified time to allow the user to see the result.

# Note: Ensure that the path to the ChromeDriver executable is correct for your system.
# The `time.sleep(10)` is used to pause the execution for 10 seconds to allow the user to see the result before closing the browser.
# The `driver.quit()` method is called to close the browser after the operations are completed.


