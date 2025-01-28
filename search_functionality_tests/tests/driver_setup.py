from selenium import webdriver

# Configuration
BASE_URL = "https://www.tmsandbox.co.nz/"

def setup_driver():
    """Initialize the WebDriver and open the base URL."""
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    driver.maximize_window()
    return driver

def teardown_driver(driver):
    """Quit the WebDriver instance."""
    if driver:
        driver.quit()
