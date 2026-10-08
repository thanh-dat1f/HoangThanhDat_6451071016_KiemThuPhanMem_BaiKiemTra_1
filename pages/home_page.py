from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    __LOC_USER_INFO = (By.CSS_SELECTOR, '.user-info, .profile, header')

    def is_user_logged_in(self) -> bool:
        return not self.driver.current_url.endswith('/Login')
