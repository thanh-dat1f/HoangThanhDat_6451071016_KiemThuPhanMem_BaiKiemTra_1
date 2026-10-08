import os
import sys
import time
import unittest
import allure
from webdriver_setup import create_driver
from pages.login_page import LoginPage
from pages.getpass_page import GetPassPage
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'screenshots'))

@allure.epic('Hệ Thống Văn Phòng Điện Tử UTC')
@allure.feature('Xác Thực & Quản Lý Truy Cập (Authentication)')
class UTCTestAutomationSuite(unittest.TestCase):
    driver = None
    results = []

    @classmethod
    def setUpClass(cls):
        headless_mode = os.getenv('HEADLESS', '0').lower() in ('1', 'true', 'yes')
        cls.driver = create_driver(headless=headless_mode, browser='chrome')
        cls.login_page = LoginPage(cls.driver)
        cls.getpass_page = GetPassPage(cls.driver)
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def record_result(self, tc_id, name, technique, steps, test_data, expected, actual, status):
        screenshot_file = os.path.join(SCREENSHOT_DIR, f'{tc_id}.png')
        try:
            self.driver.save_screenshot(screenshot_file)
            allure.attach.file(screenshot_file, name=f'MinhChung_{tc_id}', attachment_type=allure.attachment_type.PNG)
        except Exception:
            screenshot_file = ''
        try:
            detail_info = f"Mã Test Case : {tc_id}\nKỹ thuật áp dụng : {technique}\nDữ liệu thử nghiệm: {test_data}\nCác bước thực hiện:\n{steps}\n\nKết quả mong đợi : {expected}\nKết quả thực tế  : {actual}\nTrạng thái       : {('PASS' if status else 'FAIL')}"
            allure.attach(detail_info, name=f'ThongTinChiTiet_{tc_id}', attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass
        self.results.append({'id': tc_id, 'name': name, 'technique': technique, 'steps': steps, 'test_data': test_data, 'expected': expected, 'actual': actual, 'status': 'PASS' if status else 'FAIL', 'screenshot': screenshot_file})

    @allure.story('Chức năng Đăng nhập')
    @allure.title('TC_UTC_01: Đăng nhập với định dạng tài khoản hợp lệ')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc01_login_valid_format(self):
        tc_id = 'TC_UTC_01'
        name = 'Đăng nhập với định dạng tài khoản hợp lệ'
        technique = 'Phân vùng tương đương (EP - Hợp lệ)'
        steps = '1. Mở trang Login\n2. Nhập username, password hợp lệ\n3. Bấm Đăng nhập'
        test_data = "username='cb_giangvien', userpwd='MatKhau@123'"
        expected = 'Hệ thống tiếp nhận yêu cầu, xử lý và phản hồi HTTP 200 (không lỗi 500)'
        with allure.step('1. Điều hướng đến trang Đăng nhập UTC'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập thông tin tài khoản hợp lệ và gửi form'):
            self.login_page.login('cb_giangvien', 'MatKhau@123')
            time.sleep(2)
        with allure.step('3. Kiểm tra phản hồi của máy chủ'):
            source = self.login_page.get_page_source()
            is_pass = '500 Internal Server Error' not in source
            actual = 'Hệ thống phản hồi bình thường, không phát sinh lỗi 500' if is_pass else 'Hệ thống bị lỗi 500'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Chức năng Đăng nhập')
    @allure.title('TC_UTC_02: Đăng nhập thất bại khi để trống cả 2 trường')
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc02_login_empty_fields(self):
        tc_id = 'TC_UTC_02'
        name = 'Đăng nhập thất bại khi để trống cả 2 trường'
        technique = 'Phân tích giá trị biên & Kiểm tra tính hợp lệ dữ liệu'
        steps = '1. Mở trang Login\n2. Bỏ trống cả 2 ô username & password\n3. Bấm Đăng nhập'
        test_data = "username='', userpwd=''"
        expected = 'Từ chối đăng nhập, duy trì ở màn hình Login'
        with allure.step('1. Điều hướng đến trang Đăng nhập'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Bỏ trống cả 2 ô và nhấn Đăng nhập'):
            self.login_page.login('', '')
            time.sleep(1.5)
        with allure.step('3. Xác minh URL hiện tại vẫn ở trang Login'):
            is_pass = 'Login' in self.login_page.get_current_url()
            actual = 'Hệ thống giữ nguyên tại trang đăng nhập, ngăn truy cập trái phép' if is_pass else 'Bị chuyển hướng sai'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Chức năng Đăng nhập')
    @allure.title('TC_UTC_03: Đăng nhập thất bại khi nhập sai mật khẩu')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc03_login_wrong_password(self):
        tc_id = 'TC_UTC_03'
        name = 'Đăng nhập thất bại khi nhập sai mật khẩu'
        technique = 'Phân vùng tương đương (EP - Không hợp lệ)'
        steps = '1. Mở trang Login\n2. Nhập tài khoản và mật khẩu sai\n3. Bấm Đăng nhập'
        test_data = "username='sinhvien_utc', userpwd='SaiMatKhau999'"
        expected = 'Từ chối xác thực, không cấp quyền vào hệ thống'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập mật khẩu sai và gửi form'):
            self.login_page.login('sinhvien_utc', 'SaiMatKhau999')
            time.sleep(2)
        with allure.step('3. Kiểm tra hệ thống từ chối xác thực'):
            is_pass = 'Login' in self.login_page.get_current_url()
            actual = 'Chặn đăng nhập thành công, giữ tại màn hình Login' if is_pass else 'Vào được hệ thống trái phép'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

if __name__ == '__main__':
    unittest.main()
