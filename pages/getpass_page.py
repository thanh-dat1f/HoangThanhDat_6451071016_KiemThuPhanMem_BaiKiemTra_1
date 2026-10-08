from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class GetPassPage(BasePage):
    URL = 'https://vanphongdientu.utc.edu.vn/Login/GetPass'
    __email_field = (By.NAME, 'email')
    __captcha_field = (By.NAME, 'captcha')
    __submit_btn = (By.CSS_SELECTOR, "input[type='submit']")
    __back_to_login_link = (By.XPATH, "//a[contains(text(),'Trở lại đăng nhập?')]")

    def open(self):
        self.open_url(self.URL)
        return self

    def navigate(self):
        return self.open()

    def submit_get_pass(self, email: str, captcha: str):
        if email:
            self.type(self.__email_field, email)
        if captcha:
            self.type(self.__captcha_field, captcha)
        self.click(self.__submit_btn)

    def submit_getpass(self, email: str, captcha: str):
        return self.submit_get_pass(email, captcha)

    def go_back_to_login(self):
        from pages.login_page import LoginPage
        self.click(self.__back_to_login_link)
        return LoginPage(self.driver)

    def click_back_to_login(self):
        return self.go_back_to_login()

    def is_on_get_pass_page(self) -> bool:
        url = self.get_current_url().lower()
        return 'getpass' in url
