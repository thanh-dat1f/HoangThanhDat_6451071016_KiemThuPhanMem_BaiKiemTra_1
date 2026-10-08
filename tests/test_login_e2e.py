import os
import unittest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_test import BaseTest
from pages.login_page import LoginPage

@allure.epic('Kiểm Thử Web UI Tự Động: Selenium & POM (Buổi 8)')
@allure.feature('Kịch Bản E2E Login - Văn Phòng Điện Tử UTC')
class LoginE2ETest(BaseTest):

    def setUp(self):
        self.login_page = LoginPage(self.driver).open()

    @allure.story('LMS Bài Tập 1: Đăng nhập thành công / hợp lệ (Slide 54, 63)')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_whenValidCredentials_submitsFormSuccessfully(self):
        user = os.getenv('UTC_USER', 'cb_giangvien')
        pwd = os.getenv('UTC_PASS', 'MatKhau@123')
        with allure.step('1. Đăng nhập với tài khoản hợp lệ'):
            home_page = self.login_page.login_as(user, pwd)
        with allure.step('2. Xác minh máy chủ phản hồi bình thường, không gặp lỗi 500'):
            WebDriverWait(self.driver, 10).until(lambda d: '500 Internal Server Error' not in d.page_source)
            self.assertNotIn('500 Internal Server Error', self.driver.page_source)

    @allure.story('LMS Bài Tập 2: Kiểm tra lỗi validation khi bỏ trống trường (Slide 55, 63)')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_whenEmptyPassword_staysOnLoginPage(self):
        with allure.step('1. Nhập username và bỏ trống mật khẩu'):
            self.login_page.login_as('sinhvien_utc', '')
        with allure.step('2. Xác minh người dùng vẫn ở lại trang Đăng nhập (Slide 55)'):
            WebDriverWait(self.driver, 10).until(lambda d: self.login_page.is_on_login_page())
            self.assertTrue(self.login_page.is_on_login_page())

    @allure.story('LMS Bổ Sung: Đăng nhập sai mật khẩu (Slide 55)')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_whenWrongPassword_staysOnLoginPage(self):
        with allure.step('1. Đăng nhập với mật khẩu sai'):
            self.login_page.login_as('sinhvien_utc', 'SaiMatKhau999')
        with allure.step('2. Xác minh hệ thống chặn và giữ tại trang /Login (Slide 55)'):
            WebDriverWait(self.driver, 10).until(lambda d: self.login_page.is_on_login_page())
            self.assertTrue(self.login_page.is_on_login_page())

    @allure.story('Bẫy Checkbox: Thao tác checkbox Ghi nhớ đăng nhập (Slide 38)')
    @allure.severity(allure.severity_level.MINOR)
    def test_remember_me_checkbox_toggle(self):
        with allure.step("1. Tích chọn checkbox 'Giữ tôi luôn đăng nhập'"):
            self.login_page.set_remember_me(True)
        with allure.step('2. Đọc trạng thái isSelected() từ ô thật #persistent (Slide 38)'):
            self.assertTrue(self.login_page.is_remember_me_selected())

    @allure.story('Chuyển Tab: Mở liên kết hỗ trợ kỹ thuật ở Footer (Slide 40)')
    @allure.severity(allure.severity_level.NORMAL)
    def test_support_link_opens_new_tab(self):
        with allure.step('1. Click link Hỗ trợ kỹ thuật và switch sang tab mới'):
            target_url = self.login_page.click_support_link_and_switch_tab()
        with allure.step('2. Xác minh URL tab mới trỏ tới đúng domain hỗ trợ (Slide 40)'):
            self.assertIn('hotrokythuat.utc.edu.vn', target_url)

    @allure.story('Kiểm thử HTML 1: Cấu trúc thẻ <form> Action & Method')
    @allure.title('TC_HTML_01: Kiểm tra thuộc tính action và method của form đăng nhập')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_html_form_action_and_method(self):
        with allure.step('1. Kiểm tra thuộc tính method của form là POST'):
            method = self.login_page.get_form_method()
            self.assertEqual(method, 'post', "Form đăng nhập phải sử dụng method='post'")
        with allure.step('2. Kiểm tra thuộc tính action của form trỏ tới /Login'):
            action = self.login_page.get_form_action()
            self.assertIn('/Login', action, 'Thuộc tính action phải trỏ tới /Login')

    @allure.story('Kiểm thử HTML 2: Thuộc tính Placeholder của các ô Input')
    @allure.title('TC_HTML_02: Kiểm tra placeholder hướng dẫn người dùng')
    @allure.severity(allure.severity_level.NORMAL)
    def test_html_input_placeholders(self):
        with allure.step('1. Đọc placeholder của ô username'):
            user_ph = self.login_page.get_username_placeholder()
            self.assertIn('Tên đăng nhập', user_ph)
        with allure.step('2. Đọc placeholder của ô mật khẩu'):
            pwd_ph = self.login_page.get_password_placeholder()
            self.assertIn('Mật khẩu', pwd_ph)

    @allure.story('Kiểm thử HTML 3: Thuộc tính & Trạng thái nút Đăng nhập')
    @allure.title('TC_HTML_03: Kiểm tra thuộc tính value và trạng thái enabled của nút submit')
    @allure.severity(allure.severity_level.NORMAL)
    def test_html_submit_button_attributes(self):
        with allure.step('1. Kiểm tra text hiển thị trên nút qua thuộc tính value'):
            btn_val = self.login_page.get_submit_button_value()
            self.assertEqual(btn_val, 'Đăng nhập')
        with allure.step('2. Kiểm tra nút submit ở trạng thái enabled'):
            self.assertTrue(self.login_page.is_submit_button_enabled())

    @allure.story('Kiểm thử HTML 4: Thuộc tính Type của ô Mật khẩu')
    @allure.title("TC_HTML_04: Kiểm tra thuộc tính type='password' che giấu ký tự")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_html_password_input_type(self):
        with allure.step('1. Kiểm tra thuộc tính type của ô mật khẩu'):
            pwd_type = self.login_page.get_password_input_type()
            self.assertEqual(pwd_type, 'password', "Trường mật khẩu bắt buộc phải có type='password'")

    @allure.story('Kiểm thử HTML 5: Thuộc tính Href của liên kết Quên mật khẩu')
    @allure.title('TC_HTML_05: Kiểm tra thuộc tính href của thẻ <a> Quên mật khẩu')
    @allure.severity(allure.severity_level.NORMAL)
    def test_html_forgot_password_link_href(self):
        with allure.step('1. Kiểm tra thuộc tính href của link Quên mật khẩu'):
            href = self.login_page.get_forgot_password_href()
            self.assertIn('/Login/GetPass', href)

    @allure.story('Kiểm thử Bắt Lỗi: Sai lệch tiêu đề trang (Cố tình FAIL 1)')
    @allure.title('TC_FAIL_01: Cố tình kiểm tra sai tiêu đề trang web')
    @allure.severity(allure.severity_level.NORMAL)
    def test_fail_01_expect_incorrect_page_title(self):
        with allure.step('1. Đọc tiêu đề trang web thực tế'):
            actual_title = self.driver.title
        with allure.step('2. So sánh với tiêu đề giả định sai (Kỳ vọng gây FAIL)'):
            expected_wrong_title = 'Hệ Thống Đào Tạo Trực Tuyến Toàn Diện UTC 2099'
            self.assertEqual(actual_title, expected_wrong_title, f"LỖI CỐ Ý: Tiêu đề thực tế là '{actual_title}', không khớp với '{expected_wrong_title}'")

    @allure.story('Kiểm thử Bắt Lỗi: Cho phép đăng nhập tài khoản giả lập (Cố tình FAIL 2)')
    @allure.title('TC_FAIL_02: Cố tình kỳ vọng tài khoản sai đăng nhập thành công')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fail_02_expect_login_success_with_dummy_account(self):
        with allure.step('1. Nhập tài khoản giả lập hoàn toàn không tồn tại'):
            self.login_page.login_as('tai_khoan_ao_12345', 'mat_khau_sai_999')
        with allure.step('2. Cố tình khẳng định hệ thống phải chuyển sang trang chủ /Dashboard (Gây FAIL)'):
            current_url = self.driver.current_url
            self.assertIn('/Dashboard', current_url, f"LỖI CỐ Ý: Kỳ vọng URL chuyển sang /Dashboard nhưng thực tế hệ thống đã chặn lại tại '{current_url}'")
if __name__ == '__main__':
    unittest.main()
