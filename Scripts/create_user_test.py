import sys
sys.path.append('..')  # Adjust the path if needed

from Table.document_user import add_userTestSheet, create_userTestSheet

import os
import json

from selenium import webdriver
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

class BrowserCompatibilityChecker:
    def __init__(self, browser_name):
        self.browser_name = browser_name

    def check_compatibility(self):
        try:
            options = webdriver.ChromeOptions()  # Use options to set headless mode
            if self.browser_name == "chrome":
                options.add_argument("--headless")
                options.add_argument("--disable-dev-shm-usage")  # For improved headless mode performance
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            elif self.browser_name == "firefox":
                options.add_argument("--headless")
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            elif self.browser_name == "edge":
                options.add_argument("--headless")
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            else:
                raise ValueError(f"Unsupported browser: {self.browser_name}")

            driver.get('file://' + createUser_file_path)
            print(f"{self.browser_name} is compatible!")
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

    def submit_form(self):
        # Submit the form
        submit_button = self.driver.find_element(By.CLASS_NAME, "signupbtn")
        submit_button.click()

    def tearDown(self):
        self.driver.quit()

def setupbrowser(browser_name, headless=True):
    options = webdriver.ChromeOptions() if browser_name == "chrome" else webdriver.FirefoxOptions() if browser_name == "firefox" else webdriver.EdgeOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")  # For improved headless mode performance

    if browser_name == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_name == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    else:
        print(f"Unsupported browser: {browser_name}")
        return None

    return driver

def load_test_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def fill_signup_form_with_data(input_data):
    results = []

    for data in input_data:
        driver = setupbrowser('edge', headless=True)  # Set headless mode to True for background execution
        driver.get(createUser_file_path)
        form = SignUpPageTest(driver)

        try:
            form.open_signup_modal()

            # Fill form fields with data
            form.driver.find_element(By.NAME, "email").send_keys(data["email"])
            form.driver.find_element(By.NAME, "psw").send_keys(data["password"])
            form.driver.find_element(By.NAME, "psw-repeat").send_keys(data["repassword"])
            location_dropdown = Select(form.driver.find_element(By.NAME, "loc"))
            location_dropdown.select_by_visible_text(data["location"])
            if data["gender"].lower() == "male":
                form.driver.find_element(By.XPATH, "//input[@name='gender' and @value='male']").click()
            elif data["gender"].lower() == "female":
                form.driver.find_element(By.XPATH, "//input[@name='gender' and @value='female']").click()

            expected_url = form.driver.current_url

            form.submit_form()

            # Check the current URL after form submission
            current_url = form.driver.current_url

            # print(current_url + '\n' + expected_url)

            if current_url == expected_url:
                status = "fail"
            else:
                status = "pass"

        finally:
            form.tearDown()

        data["status"] = status
        results.append(data)

    return results

test_data_file_path = os.path.join(current_directory, 'createUser.json')
output_list = fill_signup_form_with_data(load_test_data(test_data_file_path))
#print(output_list)


create_userTestSheet()

for dictionary in output_list:
    add_userTestSheet(dictionary)
