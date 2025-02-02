import pytest
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from driver_setup import setup_driver, teardown_driver, BASE_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import get_search_box, get_search_button

# Test Case 1: Verify Search Bar Accepts Input
@pytest.mark.functional
def test_search_bar_accepts_input():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        
        # Act
        search_box.send_keys("test keyword")
        entered_text = search_box.get_attribute("value")
        
        # Assert
        assert entered_text == "test keyword", "Search bar does not accept input correctly."
    finally:
        teardown_driver(driver)

# Test Case 2: Verify Search Button Triggers Results
@pytest.mark.functional
def test_search_button_triggers_results():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        search_button = get_search_button(driver)
        
        # Act
        search_box.send_keys("cars")
        search_button.click()
        wait = WebDriverWait(driver, 3)
        results = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tm-marketplace-search-card__detail-section")))
        
        # Assert
        assert len(results) > 0, "No results displayed for the search query."
    finally:
        teardown_driver(driver)

# Test Case 3: Verify Auto-Suggestions Appear
@pytest.mark.functional
def test_auto_suggestions_appear():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        
        # Act
        search_box.send_keys("car")
        wait = WebDriverWait(driver, 3)
        suggestions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ng-star-inserted")))
        
        # Assert
        assert len(suggestions) > 0, "Auto-suggestions did not appear."
    finally:
        teardown_driver(driver)

# Test Case 4: Verify Auto-Suggestions are Clickable
@pytest.mark.functional
def test_auto_suggestions_are_clickable():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        
        # Act
        search_box.send_keys("car")
        wait = WebDriverWait(driver, 3)
        suggestion = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'tm-global-search__search-suggestions-link') and .//span[contains(text(), 'cars')]]")))
        if suggestion:
            suggestion.click()
            # implicit wait
            time.sleep(3)  # Wait for navigation to the results page
            current_url = driver.current_url
            
            # Assert
            assert "search" in current_url, "Clicking auto-suggestion did not navigate to results page."
        else:
            pytest.fail("No auto-suggestions to click.")
    finally:
        teardown_driver(driver)

# Test Case 5: Verify Long Input Handling
@pytest.mark.functional
def test_long_input_handling():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        long_text = "a" * 300  # 300-character input
        
        # Act
        search_box.send_keys(long_text)
        search_box.send_keys(Keys.RETURN)
        # implicit wait
        time.sleep(3)  # Wait for results to load
        
        # Assert
        assert driver.current_url.startswith(BASE_URL), "Search with long input caused an error."
        result_message = driver.find_elements(By.CLASS_NAME, "tm-search-header-result-count__heading")
        if result_message:
            assert "0 results" in result_message[0].text, "The result count message is incorrect."
    finally:
        teardown_driver(driver)

# Test Case 6: Verify Empty Input Handling
@pytest.mark.functional
def test_empty_input_handling():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        
        # Act
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        # implicit wait
        time.sleep(2)  # Wait for any error message or behavior
        current_url = driver.current_url
        no_results_message = driver.find_elements(By.CLASS_NAME, "tm-search-header-result-count__heading")
        
        # Assert
        assert current_url.startswith(BASE_URL), "Search with empty input caused an error or unexpected behavior."
        assert len(no_results_message) == 0, "No result count message displayed for empty search."
    finally:
        teardown_driver(driver)

# Test Case 7: Verify Search Responds Within Timeout
@pytest.mark.non_functional
def test_search_timeout():
    driver = setup_driver()
    try:
        # Arrange
        search_box = get_search_box(driver)
        search_button = get_search_button(driver)
        
        # Act
        search_box.send_keys("cars")
        search_button.click()

        # Measure time taken for results to load
        start_time = time.time()
        results = driver.find_elements(By.CLASS_NAME, "tm-marketplace-search-card__detail-section")
        end_time = time.time()

        elapsed_time = end_time - start_time
        
        # Assert
        assert elapsed_time < 3, f"Search took too long: {elapsed_time:.2f} seconds."
        assert len(results) > 0, "No results displayed for the search query."
    finally:
        teardown_driver(driver)

if __name__ == "__main__":
    pytest.main()
