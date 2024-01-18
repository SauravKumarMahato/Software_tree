import os
import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# get the current working directory
current_directory = os.getcwd()
createUser_file_path = os.path.join(current_directory, 'createUser.html')
# powerTrade_file_path = os.path.join(current_directory, 'powerTrade_1.html')

class BrowserCompatibilityChecker:
    def __init__(self, browser_name):
        self.browser_name = browser_name

    def check_compatibility(self):
        try:
            if self.browser_name == "chrome":
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif self.browser_name == "firefox":
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif self.browser_name == "edge":
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            else:
                raise ValueError(f"Unsupported browser: {self.browser_name}")
            
            driver.get('file://' + createUser_file_path)
            print(f"{self.browser_name} is compatible!")
            sleep(5)
            driver.quit()
        except Exception as e:
            print(f"{self.browser_name} is not compatible: {e}")

class SignUpPageTest:
    def __init__(self, driver):
        self.driver = driver

    def open_signup_modal(self):
        # Click the "Sign Up" button to open the modal
        signup_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Sign Up')]")
        signup_button.click()

    def test_successful_sign_up(self):
        email_field = self.driver.find_element(By.NAME, "email")
        password_field = self.driver.find_element(By.NAME, "psw")
        repeat_password_field = self.driver.find_element(By.NAME, "psw-repeat")
        location_dropdown = Select(self.driver.find_element(By.NAME, "loc"))
        male_radio = self.driver.find_element(By.XPATH, "//input[@name='gender' and @value='male']")
        signup_button = self.driver.find_element(By.CLASS_NAME, "signupbtn")

        email_field.send_keys("test@example.com")
        sleep(1)
        password_field.send_keys("password123")
        sleep(1)
        repeat_password_field.send_keys("password123")
        sleep(1)
        location_dropdown.select_by_visible_text("Kathmandu")
        sleep(1)
        male_radio.click()
        sleep(1)

        # Assert successful sign-up (replace with your specific success condition)
        # success_message = self.driver.find_element(By.ID, "success-message")
        # self.assertEqual(success_message.text, "Sign up successful!")

    
    def test_empty_fields(self):
        signup_button = self.driver.find_element(By.CLASS_NAME, "signupbtn")
        signup_button.click()
        # # Assert errors for all required fields
        # error_messages = self.driver.find_elements(By.CLASS_NAME, "error-message")
        # self.assertEqual(len(error_messages), 7)  # Assuming all fields are required

    def test_invalid_email_format(self):
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("invalid_email")
        signup_button = self.driver.find_element(By.CLASS_NAME, "signupbtn")
        signup_button.click()

        # # Assert error for email field
        # email_error = self.driver.find_element(By.ID, "email-error")
        # self.assertEqual(email_error.text, "Please enter a valid email address")

    def submit_form(self):
        # Submit the form
        submit_button = self.driver.find_element(By.CLASS_NAME, "signupbtn")
        submit_button.click()

    def tearDown(self):
        self.driver.quit()

    def get_url(self):
        #  current_url = self.driver.current_url
        current_url = createUser_file_path

        # Check the current URL after form submission
        expected_url = self.driver.current_url

        print(current_url + '\n' + expected_url)

        if current_url == expected_url:
            print("Test Failed!")
            with open('text.txt', 'a') as file:
                file.write('Failed')
        else:
            print("Test Passed!")
            with open('text.txt', 'a') as file:
                file.write('Pass')



def test_compatibility():
    checker = BrowserCompatibilityChecker('edge')
    checker.check_compatibility()

# setup browser for testing
def setupbrowser(browser_name):
    if browser_name == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_name == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        print(f"Unsupported browser: {browser_name}")
    return driver


def fill_signup_form():
    driver = setupbrowser('edge')
    driver.get(createUser_file_path)
    form =  SignUpPageTest(driver)
    form.open_signup_modal()
    form.test_successful_sign_up()
    form.submit_form()
    form.get_url()
    sleep(5)
    form.tearDown()
    # driver.quit()

fill_signup_form()



    