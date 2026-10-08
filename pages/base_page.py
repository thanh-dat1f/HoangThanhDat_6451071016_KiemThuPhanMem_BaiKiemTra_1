import os
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver: WebDriver, timeout: int=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.is_visual_mode = os.getenv('HEADLESS', '0').lower() not in ('1', 'true', 'yes')

    def highlight(self, element, action_name: str=''):
        if not self.is_visual_mode:
            return
        try:
            if action_name:
                safe_name = action_name.replace("'", "\\'")
                self.driver.execute_script(f"console.log('%c[F12 STEP]: {safe_name}', 'color: #d9534f; font-weight: bold; font-size: 13px;');")
            self.driver.execute_script("arguments[0].style.outline = '3px solid #ff0000';arguments[0].style.boxShadow = '0 0 10px #ff0000';arguments[0].style.backgroundColor = '#ffffcc';", element)
            time.sleep(0.7)
        except Exception:
            pass

    def unhighlight(self, element):
        if not self.is_visual_mode:
            return
        try:
            self.driver.execute_script("arguments[0].style.outline = '';arguments[0].style.boxShadow = '';arguments[0].style.backgroundColor = '';", element)
        except Exception:
            pass

    def open_url(self, url: str):
        self.driver.get(url)
        if self.is_visual_mode:
            try:
                self.driver.execute_script(f"console.log('%c[F12 NAVIGATE]: Đang mở trang {url}', 'color: #0275d8; font-weight: bold; font-size: 14px;');")
            except Exception:
                pass
            time.sleep(0.8)

    def click(self, locator: tuple):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight(el, f'Click vào {locator[1]}')
        el.click()
        if self.is_visual_mode:
            time.sleep(0.6)

    def type(self, locator: tuple, text: str):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.highlight(el, f"Nhập '{text}' vào {locator[1]}")
        el.clear()
        if self.is_visual_mode and text:
            for char in text:
                el.send_keys(char)
                time.sleep(0.04)
            time.sleep(0.4)
        else:
            el.send_keys(text)
        self.unhighlight(el)

    def get_text(self, locator: tuple) -> str:
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.highlight(el, f'Đọc text từ {locator[1]}')
        val = el.text
        self.unhighlight(el)
        return val

    def is_visible(self, locator: tuple) -> bool:
        try:
            el = self.wait.until(EC.visibility_of_element_located(locator))
            self.highlight(el, f'Kiểm tra hiển thị {locator[1]}')
            visible = el.is_displayed()
            self.unhighlight(el)
            return visible
        except Exception:
            return False

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_source(self) -> str:
        return self.driver.page_source
