from selenium.webdriver.common.by import By

def get_search_box(driver):
    """Retrieve the search box element."""
    return driver.find_element(By.ID, "search")

def get_search_button(driver):
    """Retrieve the search button element."""
    return driver.find_element(By.CLASS_NAME, "tm-global-search__search-form-submit-button")
