import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from driver_setup import setup_driver, teardown_driver, BASE_URL  # Import utility functions

# Test Case 1: Verify Search Bar Accepts Input
@pytest.mark.functional
def test_search_bar_accepts_input():
    driver = setup_driver()
    try:
        search_box = driver.find_element(By.ID, "search")
        search_box.send_keys("test keyword")
        entered_text = search_box.get_attribute("value")
        assert entered_text == "test keyword", "Search bar does not accept input correctly."
    finally:
        teardown_driver(driver)

# Test Case 2: Verify Search Button Triggers Results
@pytest.mark.functional
def test_search_button_triggers_results():
    driver = setup_driver()
    try:
        search_box = driver.find_element(By.ID, "search")
        search_button = driver.find_element(By.CLASS_NAME, "tm-global-search__search-form-submit-button")
        search_box.send_keys("cars")
        search_button.click()
        time.sleep(3)
        results = driver.find_elements(By.CLASS_NAME, "tm-marketplace-search-card__detail-section")
        assert len(results) > 0, "No results displayed for the search query."
    finally:
        teardown_driver(driver)

# Test Case 3: Verify Auto-Suggestions Appear
@pytest.mark.functional
def test_auto_suggestions_appear():
    driver = setup_driver()
    try:
        search_box = driver.find_element(By.ID, "search")
        search_box.send_keys("car")
        time.sleep(2)
        suggestions = driver.find_elements(By.CLASS_NAME, "ng-star-inserted")
        assert len(suggestions) > 0, "Auto-suggestions did not appear."
    finally:
        teardown_driver(driver)

# Test Case 4: Verify Auto-Suggestions are Clickable
@pytest.mark.functional
def test_auto_suggestions_are_clickable():
    driver = setup_driver()
    try:
        search_box = driver.find_element(By.ID, "search")
        search_box.send_keys("car")
        time.sleep(2)
        suggestion = driver.find_element(By.XPATH, "//a[contains(@class, 'tm-global-search__search-suggestions-link') and .//span[contains(text(), 'cars')]]")
        if suggestion:
            suggestion.click()
            time.sleep(3)
            current_url = driver.current_url
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
        search_box = driver.find_element(By.ID, "search")
        long_text = "a" * 300
        search_box.send_keys(long_text)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
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
        search_box = driver.find_element(By.ID, "search")
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        current_url = driver.current_url
        no_results_message = driver.find_elements(By.CLASS_NAME, "tm-search-header-result-count__heading")
        assert current_url.startswith(BASE_URL), "Search with empty input caused an error or unexpected behavior."
        assert len(no_results_message) == 0, "No result count message displayed for empty search."
    finally:
        teardown_driver(driver)

# Test Case 7: Verify Search Responds Within Timeout
@pytest.mark.non_functional
def test_search_timeout():
    driver = setup_driver()
    try:
        search_box = driver.find_element(By.ID, "search")
        search_button = driver.find_element(By.CLASS_NAME, "tm-global-search__search-form-submit-button")
        search_box.send_keys("cars")
        search_button.click()
        start_time = time.time()
        results = driver.find_elements(By.CLASS_NAME, "tm-marketplace-search-card__detail-section")
        end_time = time.time()
        elapsed_time = end_time - start_time
        assert elapsed_time < 3, f"Search took too long: {elapsed_time:.2f} seconds."
        assert len(results) > 0, "No results displayed for the search query."
    finally:
        teardown_driver(driver)

if __name__ == "__main__":
    pytest.main()
