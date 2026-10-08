import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'screenshots'))

class BaseTest(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        options = Options()
        headless_mode = os.getenv('HEADLESS', '0').lower() in ('1', 'true', 'yes')
        if headless_mode:
            options.add_argument('--headless=new')
        else:
            options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument('--start-maximized')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-notifications')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def capture_screenshot(self, test_name: str) -> str:
        screenshot_path = os.path.join(SCREENSHOT_DIR, f'{test_name}.png')
        if self.driver:
            try:
                self.driver.save_screenshot(screenshot_path)
            except Exception:
                pass
        return screenshot_path
