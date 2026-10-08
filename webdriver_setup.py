from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def create_driver(headless: bool=False, browser: str='chrome') -> webdriver.Remote:
    browser = browser.lower()
    if browser == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        else:
            options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-infobars')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        return driver
    elif browser == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Edge(options=options)
        return driver
    else:
        raise ValueError(f"Trình duyệt không hỗ trợ: {browser}. Vui lòng chọn 'chrome' hoặc 'edge'.")
