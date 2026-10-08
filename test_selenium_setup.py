import os
import sys
import time
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_setup import create_driver

def test_selenium():
    print('==================================================')
    print(' BẮT ĐẦU KIỂM TRA MÔI TRƯỜNG CÔNG CỤ SELENIUM ')
    print('==================================================')
    screenshot_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    print('1. Khởi tạo Chrome WebDriver qua Selenium 4...')
    driver = create_driver(headless=True, browser='chrome')
    try:
        target_url = 'https://www.google.com'
        print(f'2. Điều hướng đến {target_url}...')
        driver.get(target_url)
        time.sleep(1)
        page_title = driver.title
        print(f"   => Tiêu đề trang: '{page_title}'")
        print("3. Thử tìm kiếm từ khóa 'Selenium Automation Test'...")
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('Selenium Automation Test')
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        screenshot_path = os.path.join(screenshot_dir, 'kiem_tra_selenium_thanh_cong.png')
        driver.save_screenshot(screenshot_path)
        print(f'4. Đã chụp ảnh màn hình lưu tại: {screenshot_path}')
        print('==================================================')
        print(' [THÀNH CÔNG] Công cụ Selenium đã sẵn sàng 100%! ')
        print('==================================================')
        return True
    except Exception as e:
        print(f'[LỖI]: {e}')
        return False
    finally:
        driver.quit()
if __name__ == '__main__':
    success = test_selenium()
    sys.exit(0 if success else 1)
