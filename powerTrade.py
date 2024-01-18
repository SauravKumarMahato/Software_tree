from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


import os

# get the current working directory
current_directory = os.getcwd()
# createUser_file_path = os.path.join(current_directory, 'createUser.html')
powerTrade_file_path = os.path.join(current_directory, 'powerTrade_1.html')

class PowerTradeTest:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_page(self):
        self.driver.get('file://' + powerTrade_file_path)

    def fill_power_trade_form(self):
        self.driver.find_element(By.NAME, 'addr').send_keys('Sample Address')

        # time.sleep(2)
        trader_dropdown = Select(self.driver.find_element(By.NAME, 'trader'))
        trader_dropdown.select_by_value('aenergy')
        # time.sleep(2)


        self.driver.find_element(By.NAME, 'tDate').send_keys('2024-01-18')
        # time.sleep(2)


        uom_radio = self.driver.find_element(By.NAME, 'uom')
        uom_radio.click()
        # time.sleep(2)


        self.driver.find_element(By.NAME, 'dfDate').send_keys('2024-01-18')
        self.driver.find_element(By.NAME, 'dtDate').send_keys('2024-01-19')

        # time.sleep(2)

        # Submit the form
        self.driver.find_element(By.NAME, 'vol').send_keys('100')
        # time.sleep(2)

        frequency_dropdown = Select(self.driver.find_element(By.ID, 'freq'))
        frequency_dropdown.select_by_value('daily')
        # time.sleep(2)


        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Wait for a moment to see the result
        # time.sleep(10)


        # current_url = self.driver.current_url
        current_url = 'file://' + powerTrade_file_path

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

    def close_browser(self):
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    # Create a new instance of the Chrome driver
    chrome_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


    try:
        # Create an instance of the PowerTradeTest class
        power_trade_test = PowerTradeTest(chrome_driver)

        # Execute the test
        power_trade_test.navigate_to_page()
        power_trade_test.fill_power_trade_form()

        # You can add assertions or further actions to check for errors or verify the result

    finally:
        # Close the browser window
        power_trade_test.close_browser()
