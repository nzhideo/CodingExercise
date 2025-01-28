from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
import time

# Configuration
BASE_URL = "https://www.tmsandbox.co.nz/"

# Helper Functions
def setup_driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    driver.maximize_window()
    return driver

# Test Case 1: Verify Search Bar Accepts Input
@pytest.mark.functional
def test_search_bar_accepts_input():
    driver = setup_driver()

    try:
        # Arrange
        search_box = driver.find_element(By.ID, "search")
        
        # Act
        search_box.send_keys("test keyword")
        entered_text = search_box.get_attribute("value")
        
        # Assert
        assert entered_text == "test keyword", "Search bar does not accept input correctly."
    finally:
        driver.quit()

# Test Case 2: Verify Search Button Triggers Results
@pytest.mark.functional
def test_search_button_triggers_results():
    driver = setup_driver()

    try:
        # Arrange
        search_box = driver.find_element(By.ID, "search")
        search_button = driver.find_element(By.CLASS_NAME, "tm-global-search__search-form-submit-button")
        
        # Act
        search_box.send_keys("cars")
        search_button.click()
        time.sleep(3)  # Wait for results to load
        results = driver.find_elements(By.CLASS_NAME, "tm-marketplace-search-card__detail-section")
        
        # Assert
        assert len(results) > 0, "No results displayed for the search query."
    finally:
        driver.quit()

# Test Case 3: Verify Auto-Suggestions Appear
@pytest.mark.functional
def test_auto_suggestions_appear():
    driver = setup_driver()

    try:
        # Arrange
        search_box = driver.find_element(By.ID, "search")
        
        # Act
        search_box.send_keys("car")
        time.sleep(2)  # Wait for suggestions to appear
        suggestions = driver.find_elements(By.CLASS_NAME, "ng-star-inserted")
        
        # Assert
        assert len(suggestions) > 0, "Auto-suggestions did not appear."
    finally:
        driver.quit()

# Test Case 4: Verify Auto-Suggestions are Clickable
@pytest.mark.functional
def test_auto_suggestions_are_clickable():
    driver = setup_driver()

    try:
        # Arrange
        search_box = driver.find_element(By.ID, "search")
        
        # Act
        search_box.send_keys("car")
        time.sleep(2)  # Wait for suggestions to appear
        suggestion = driver.find_element(By.XPATH, "//a[contains(@class, 'tm-global-search__search-suggestions-link') and .//span[contains(text(), 'cars')]]")
        
        if suggestion:
            suggestion.click()
            time.sleep(3)  # Wait for results page to load
            current_url = driver.current_url
            
            # Assert
            assert "search" in current_url, "Clicking auto-suggestion did not navigate to results page."
        else:
            pytest.fail("No auto-suggestions to click.")
    finally:
        driver.quit()

# Test Case 5: Verify Long Input Handling
@pytest.mark.functional
def test_long_input_handling():
    driver = setup_driver()

    try:
        # Arrange
        search_box = driver.find_element(By.ID, "search")
        long_text = "a" * 300  # 300-character string
        
        # Act
        search_box.send_keys(long_text)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for results to load
        
        # Assert
        assert driver.current_url.startswith(BASE_URL), "Search with long input caused an error."
        result_message = driver.find_elements(By.CLASS_NAME, "tm-search-header-result-count__heading")
        
        if result_message:
            assert "0 results" in result_message[0].text, "The result count message is incorrect."
    finally:
        driver.quit()

# Test Case 6: Verify Empty Input Handling
@pytest.mark.functional
def test_empty_input_handling():
    driver = setup_driver()

    try:
        # Arrange
        search_box = driver.find_element(By.ID, "search")
        
        # Act
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for any error message or action to happen
        current_url = driver.current_url
        no_results_message = driver.find_elements(By.CLASS_NAME, "tm-search-header-result-count__heading")
        
        # Assert
        assert current_url.startswith(BASE_URL), "Search with empty input caused an error or unexpected behavior."
        assert len(no_results_message) == 0, "No result count message displayed for empty search."
    finally:
        driver.quit()

if __name__ == "__main__":
    pytest.main()
