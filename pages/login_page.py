from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.getpass_page import GetPassPage

class LoginPage(BasePage):
    URL = 'https://vanphongdientu.utc.edu.vn/Login'
    __username_field = (By.NAME, 'username')
    __password_field = (By.NAME, 'userpwd')
    __login_button = (By.CSS_SELECTOR, 'input.submit_login')
    __checkbox_hidden = (By.ID, 'persistent')
    __checkbox_fake = (By.CSS_SELECTOR, 'label.check')
    __oauth_google_btn = (By.XPATH, "//a[contains(text(),'e-mail UTC')]")
    __forgot_pass_link = (By.CSS_SELECTOR, "a[href='/Login/GetPass']")
    __support_link = (By.CSS_SELECTOR, "a[href*='hotrokythuat.utc.edu.vn']")
    __form_element = (By.TAG_NAME, 'form')

    def get_form_action(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self.__form_element)).get_attribute('action') or ''

    def get_form_method(self) -> str:
        return (self.wait.until(EC.presence_of_element_located(self.__form_element)).get_attribute('method') or '').lower()

    def get_username_placeholder(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self.__username_field)).get_attribute('placeholder') or ''

    def get_password_placeholder(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self.__password_field)).get_attribute('placeholder') or ''

    def get_submit_button_value(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self.__login_button)).get_attribute('value') or ''

    def is_submit_button_enabled(self) -> bool:
        return self.wait.until(EC.presence_of_element_located(self.__login_button)).is_enabled()

    def get_forgot_password_href(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self.__forgot_pass_link)).get_attribute('href') or ''

    def open(self):
        self.open_url(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.__username_field))
        return self

    def navigate(self):
        return self.open()

    def login(self, username: str, password: str):
        return self.login_as(username, password)

    def login_as(self, username: str, password: str) -> HomePage:
        if username:
            self.type(self.__username_field, username)
        else:
            self.wait.until(EC.visibility_of_element_located(self.__username_field)).clear()
        if password:
            self.type(self.__password_field, password)
        else:
            self.wait.until(EC.visibility_of_element_located(self.__password_field)).clear()
        self.click(self.__login_button)
        return HomePage(self.driver)

    def click_remember_me(self) -> bool:
        self.set_remember_me(True)
        return self.is_remember_me_selected()

    def submit_with_enter(self, username: str, password: str) -> HomePage:
        return self.login_with_enter(username, password)

    def get_support_link_details(self) -> tuple:
        el = self.wait.until(EC.presence_of_element_located(self.__support_link))
        return (el.get_attribute('href'), el.get_attribute('target'))

    def login_with_enter(self, username: str, password: str) -> HomePage:
        self.type(self.__username_field, username)
        pwd_el = self.wait.until(EC.visibility_of_element_located(self.__password_field))
        pwd_el.clear()
        pwd_el.send_keys(password)
        pwd_el.send_keys(Keys.ENTER)
        return HomePage(self.driver)

    def is_on_login_page(self) -> bool:
        return '/Login' in self.get_current_url()

    def set_remember_me(self, should_check: bool=True):
        hidden_el = self.driver.find_element(*self.__checkbox_hidden)
        if hidden_el.is_selected() != should_check:
            self.click(self.__checkbox_fake)

    def is_remember_me_selected(self) -> bool:
        hidden_el = self.driver.find_element(*self.__checkbox_hidden)
        return hidden_el.is_selected()

    def get_oauth_google_url(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.__oauth_google_btn))
        return el.get_attribute('href')

    def get_password_input_type(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.__password_field))
        return el.get_attribute('type')

    def go_to_get_pass_page(self) -> GetPassPage:
        self.click(self.__forgot_pass_link)
        return GetPassPage(self.driver)

    def click_support_link_and_switch_tab(self) -> str:
        main_tab = self.driver.current_window_handle
        initial_handles = set(self.driver.window_handles)
        self.click(self.__support_link)
        self.wait.until(lambda d: len(set(d.window_handles) - initial_handles) > 0)
        new_tab = list(set(self.driver.window_handles) - initial_handles)[0]
        self.driver.switch_to.window(new_tab)
        new_tab_url = self.driver.current_url
        self.driver.close()
        self.driver.switch_to.window(main_tab)
        return new_tab_url
