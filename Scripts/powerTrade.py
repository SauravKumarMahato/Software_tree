import sys
sys.path.append('..') 

from Table.document_power import add_powerTestSheet, create_powerTestSheet

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import os
import json

# get the current working directory
current_directory = os.getcwd()
# createUser_file_path = os.path.join(current_directory, 'createUser.html')
powerTrade_file_path = os.path.join(current_directory, 'powerTrade_1.html')


    
class PowerTraderPageTest:
    def __init__(self, driver):
        self.driver = driver

    def submit_power_trader_form(self):
        # Modify this according to the actual XPath or method you use to submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
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

# Modify the fill_power_trader_form_with_data function
def fill_power_trader_form_with_data(input_data):
    results = []

    for data in input_data:
        driver = setupbrowser('edge', headless=True)
        driver.get(powerTrade_file_path)
        form = PowerTraderPageTest(driver)

        try:

            # Fill form fields with data
            form.driver.find_element(By.NAME, "addr").send_keys(data["Address"])
            form.driver.find_element(By.NAME, "trader").send_keys(data["Trader"])
            form.driver.find_element(By.NAME, "tDate").send_keys(data["Trade Date"])

            # Handle radio buttons based on UOM value
            uom_value = data["UOM Conversion"]
            if uom_value.lower() == "kw":
                form.driver.find_element(By.NAME, "uom").click()
            elif uom_value.lower() == "mw":
                form.driver.find_elements(By.NAME, "uom")[1].click()

            form.driver.find_element(By.NAME, "dfDate").send_keys(data["Delivery Date From"])
            form.driver.find_element(By.NAME, "dtDate").send_keys(data["Delivery Date To"])
            form.driver.find_element(By.NAME, "vol").send_keys(str(data["Volume"]))

            # Handle the frequency dropdown
            frequency_dropdown = Select(form.driver.find_element(By.ID, "freq"))
            frequency_dropdown.select_by_visible_text(data["Frequency"])

            expected_url = form.driver.current_url

            form.submit_power_trader_form()

            # Check the current URL after form submission
            current_url = form.driver.current_url

            if data['validity'] == 1:
                if current_url == expected_url:
                    status = "fail"
                else:
                    status = "pass"
            else:
                if current_url == expected_url:
                    status = "pass"
                else:
                    status = "fail"

        finally:
            form.tearDown()

        data["status"] = status
        results.append(data)

    return results


# Assuming powerTrade_file_path is defined similarly to createUser_file_path
test_data_power_trader_file_path = os.path.join(current_directory, 'powerTrader.json')
output_list_power_trader = fill_power_trader_form_with_data(load_test_data(test_data_power_trader_file_path))
#print(output_list_power_trader)

# Assuming you have defined add_powerTraderSheet and create_powerTraderSheet similarly to add_userTestSheet and create_userTestSheet
create_powerTestSheet()

for dictionary in output_list_power_trader:
    add_powerTestSheet(dictionary)
