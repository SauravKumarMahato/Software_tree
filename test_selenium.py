import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from time import sleep

# get the current working directory
current_directory = os.getcwd()
createUser_file_path = os.path.join(current_directory, 'createUser.html')
powerTrade_file_path = os.path.join(current_directory, 'powerTrade_1.html')


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

# create object from the class 
checker = BrowserCompatibilityChecker('edge')
checker.check_compatibility()


