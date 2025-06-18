from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import yaml
import logging

logger = logging.getLogger(__name__)

def setup_chrome_driver():
    logger.debug("Setting up ChromeDriver")
    with open('config/variables.yaml', 'r') as file:
        config = yaml.safe_load(file)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if you don't need a UI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=config['chrome_driver_path'])  # Use path from variables.yaml
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.debug("ChromeDriver setup complete")
    return driver

def teardown_chrome_driver(driver):
    logger.debug("Tearing down ChromeDriver")
    driver.quit()
