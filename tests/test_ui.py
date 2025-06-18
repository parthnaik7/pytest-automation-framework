import pytest
import logging
from utils.selenium_util import setup_chrome_driver, teardown_chrome_driver

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def driver():
    driver = setup_chrome_driver()
    yield driver
    teardown_chrome_driver(driver)

def test_open_google(driver):
    logger.info("Opening Google homepage")
    driver.get("https://www.google.com")
    assert "Google" in driver.title, "Google page title does not match"
    logger.info("Google homepage opened successfully")