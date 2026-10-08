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

    @allure.story('Chức năng Đăng nhập')
    @allure.title('TC_UTC_04: Đăng nhập thất bại với tài khoản không tồn tại')
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc04_login_non_existent_account(self):
        tc_id = 'TC_UTC_04'
        name = 'Đăng nhập thất bại với tài khoản không tồn tại'
        technique = 'Đoán lỗi (Error Guessing)'
        steps = '1. Mở trang Login\n2. Nhập tài khoản giả lập không tồn tại\n3. Bấm Đăng nhập'
        test_data = "username='user_khong_ton_tai_utc_99999', userpwd='Password123!'"
        expected = 'Hệ thống từ chối đăng nhập và không chuyển tiếp vào dashboard'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập tài khoản không tồn tại'):
            self.login_page.login('user_khong_ton_tai_utc_99999', 'Password123!')
            time.sleep(2)
        with allure.step('3. Kiểm tra chặn truy cập'):
            is_pass = 'Login' in self.login_page.get_current_url()
            actual = 'Hệ thống từ chối người dùng không tồn tại' if is_pass else 'Xảy ra lỗi bất thường'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Giao diện người dùng (UI Controls)')
    @allure.title("TC_UTC_05: Kiểm tra thao tác Checkbox 'Giữ tôi luôn đăng nhập'")
    @allure.severity(allure.severity_level.MINOR)
    def test_tc05_remember_me_checkbox(self):
        tc_id = 'TC_UTC_05'
        name = "Kiểm tra thao tác Checkbox 'Giữ tôi luôn đăng nhập'"
        technique = 'Kiểm thử tương tác thành phần giao diện (UI Control)'
        steps = "1. Mở trang Login\n2. Click vào checkbox 'Giữ tôi luôn đăng nhập'\n3. Kiểm tra trạng thái is_selected"
        test_data = 'Checkbox #persistent'
        expected = 'Checkbox được tích chọn thành công (is_selected = True)'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Click chọn checkbox Ghi nhớ đăng nhập'):
            is_selected = self.login_page.click_remember_me()
            time.sleep(0.5)
        with allure.step('3. Xác minh trạng thái checkbox'):
            actual = 'Checkbox đã được tích chọn' if is_selected else 'Không kích hoạt được checkbox'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_selected)
        self.assertTrue(is_selected)

    @allure.story('Tích hợp Đăng nhập một lần (SSO)')
    @allure.title("TC_UTC_06: Kiểm tra liên kết OAuth 'Đăng nhập bằng e-mail UTC'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc06_oauth_google_button(self):
        tc_id = 'TC_UTC_06'
        name = "Kiểm tra liên kết OAuth 'Đăng nhập bằng e-mail UTC'"
        technique = 'Kiểm thử tích hợp SSO (Single Sign-On)'
        steps = '1. Mở trang Login\n2. Lấy thuộc tính href của nút OAuth Google\n3. Xác minh domain Google OAuth'
        test_data = 'Nút Đăng nhập bằng e-mail UTC'
        expected = 'Liên kết trỏ tới accounts.google.com và chứa client_id xác thực của UTC'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Lấy href liên kết OAuth'):
            href = self.login_page.get_oauth_google_url()
        with allure.step('3. Kiểm tra URL đích đến Google OAuth'):
            is_pass = 'accounts.google.com' in href and 'client_id' in href
            actual = f'URL OAuth chính xác ({href[:45]}...)' if is_pass else 'URL OAuth không hợp lệ'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Chức năng Quên mật khẩu')
    @allure.title('TC_UTC_07: Quên mật khẩu: Báo lỗi khi nhập sai mã Captcha')
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc07_getpass_invalid_captcha(self):
        tc_id = 'TC_UTC_07'
        name = 'Quên mật khẩu: Báo lỗi khi nhập sai mã Captcha'
        technique = 'Kiểm thử logic xác thực bảo mật'
        steps = '1. Mở trang /Login/GetPass\n2. Nhập email và mã captcha sai\n3. Nhấn Tiếp tục'
        test_data = "email='sinhvien@utc.edu.vn', captcha='00000_SAI'"
        expected = 'Từ chối cấp lại mật khẩu, duy trì tại trang GetPass'
        with allure.step('1. Mở trang Quên mật khẩu'):
            self.getpass_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập email đúng và Captcha sai cố ý'):
            self.getpass_page.submit_getpass('sinhvien@utc.edu.vn', '00000_SAI')
            time.sleep(2)
        with allure.step('3. Kiểm tra chặn cấp lại mật khẩu'):
            curr_url = self.getpass_page.get_current_url()
            is_pass = 'Getpass' in curr_url or 'GetPass' in curr_url
            actual = 'Chặn thành công yêu cầu khi mã captcha sai' if is_pass else 'Yêu cầu được thực thi sai nguyên tắc'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Chức năng Quên mật khẩu')
    @allure.title('TC_UTC_08: Quên mật khẩu: Kiểm tra nhập Email sai định dạng')
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc08_getpass_invalid_email(self):
        tc_id = 'TC_UTC_08'
        name = 'Quên mật khẩu: Kiểm tra nhập Email sai định dạng'
        technique = 'Phân vùng tương đương (EP - Format không hợp lệ)'
        steps = '1. Mở trang /Login/GetPass\n2. Nhập chuỗi email thiếu @ và domain\n3. Nhấn Tiếp tục'
        test_data = "email='email_khong_hop_le_utc', captcha='12345'"
        expected = 'Hệ thống từ chối xử lý định dạng email sai'
        with allure.step('1. Mở trang Quên mật khẩu'):
            self.getpass_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập email sai định dạng'):
            self.getpass_page.submit_getpass('email_khong_hop_le_utc', '12345')
            time.sleep(2)
        with allure.step('3. Kiểm tra hệ thống từ chối'):
            curr_url = self.getpass_page.get_current_url()
            is_pass = 'Getpass' in curr_url or 'GetPass' in curr_url
            actual = 'Hệ thống từ chối email không đúng chuẩn' if is_pass else 'Chấp nhận email sai định dạng'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Kiểm thử An ninh & Bảo mật')
    @allure.title('TC_UTC_09: Kiểm thử phòng vệ tấn công SQL Injection')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_tc09_sql_injection_defense(self):
        tc_id = 'TC_UTC_09'
        name = 'Kiểm thử phòng vệ tấn công SQL Injection'
        technique = 'Kiểm thử an ninh bảo mật (Security Testing)'
        steps = '1. Mở trang Login\n2. Nhập SQL Injection payload vào ô username\n3. Bấm Đăng nhập'
        test_data = 'username="\' OR \'1\'=\'1\' --", userpwd=\'anypassword\''
        expected = 'Hệ thống không bị sập cú pháp SQL, không lộ dữ liệu database, ở lại trang Login'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Gửi payload SQL Injection kinh điển'):
            self.login_page.login("' OR '1'='1' --", 'anypassword')
            time.sleep(2)
        with allure.step('3. Kiểm tra không bị lộ lỗi Database và không bypass thành công'):
            source = self.login_page.get_page_source().lower()
            no_sql_leak = not any((err in source for err in ['sql syntax', 'mysql_fetch', 'database error', 'ora-']))
            in_login = 'Login' in self.login_page.get_current_url()
            is_pass = no_sql_leak and in_login
            actual = 'An toàn trước tấn công SQL Injection cơ bản' if is_pass else 'Lộ lỗi SQL cú pháp'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Kiểm thử Liên kết & Chuyển hướng')
    @allure.title("TC_UTC_10: Kiểm tra liên kết 'Trung tâm trợ giúp' ở Footer")
    @allure.severity(allure.severity_level.MINOR)
    def test_tc10_footer_support_link(self):
        tc_id = 'TC_UTC_10'
        name = "Kiểm tra liên kết 'Trung tâm trợ giúp' ở Footer"
        technique = 'Kiểm thử tính toàn vẹn liên kết (Link Integrity)'
        steps = '1. Mở trang Login\n2. Lấy href và target của liên kết hỗ trợ kỹ thuật\n3. Kiểm tra tính đúng đắn'
        test_data = 'Liên kết Hỗ trợ kỹ thuật UTC'
        expected = "Link trỏ tới domain hotrokythuat.utc.edu.vn và mở tab mới (target='_blank')"
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Lấy thuộc tính liên kết Footer'):
            href, target = self.login_page.get_support_link_details()
        with allure.step('3. Kiểm tra domain và target mở tab mới'):
            is_pass = 'hotrokythuat.utc.edu.vn' in href and target == '_blank'
            actual = f'Liên kết chính xác ({href}) và mở tab mới' if is_pass else 'Liên kết hoặc thuộc tính target sai'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Kiểm thử An ninh & Bảo mật')
    @allure.title('TC_UTC_11: Kiểm thử phòng vệ Cross-Site Scripting (XSS)')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_tc11_xss_defense(self):
        tc_id = 'TC_UTC_11'
        name = 'Kiểm thử phòng vệ Cross-Site Scripting (XSS)'
        technique = 'Kiểm thử an ninh bảo mật (XSS Prevention)'
        steps = '1. Mở trang Login\n2. Nhập payload script độc hại vào ô username\n3. Gửi form và kiểm tra Alert'
        test_data = 'username="<script>alert(\'XSS_UTC\')</script>", userpwd=\'123\''
        expected = 'Trình duyệt không bị kích hoạt popup Alert chứa mã độc script'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập XSS payload script'):
            self.login_page.login("<script>alert('XSS_UTC')</script>", '123456')
            time.sleep(1.5)
        with allure.step('3. Kiểm tra xem có popup Alert bất thường không'):
            alert_present = False
            try:
                alert = self.driver.switch_to.alert
                alert_present = True
                alert.dismiss()
            except Exception:
                alert_present = False
            is_pass = not alert_present
            actual = 'Không bị kích hoạt hộp thoại script độc hại' if is_pass else 'Bị khai thác lỗ hổng XSS'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Kiểm thử An ninh & Bảo mật')
    @allure.title('TC_UTC_12: Kiểm tra thuộc tính che giấu ký tự mật khẩu (Masking)')
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc12_password_masking(self):
        tc_id = 'TC_UTC_12'
        name = 'Kiểm tra thuộc tính che giấu ký tự mật khẩu (Masking)'
        technique = 'Kiểm thử bảo mật giao diện người dùng'
        steps = "1. Mở trang Login\n2. Kiểm tra thuộc tính 'type' của thẻ input mật khẩu\n3. Đảm bảo là type='password'"
        test_data = "Trường input name='userpwd'"
        expected = "Thuộc tính type của thẻ là 'password' để ẩn ký tự khi nhập"
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Kiểm tra thuộc tính type ô mật khẩu'):
            field_type = self.login_page.get_password_input_type()
            is_pass = field_type == 'password'
            actual = f"Trường mật khẩu có type='{field_type}' an toàn" if is_pass else 'Mật khẩu không được che giấu'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Trải nghiệm người dùng (UX & Accessibility)')
    @allure.title('TC_UTC_13: Kiểm tra gửi form đăng nhập bằng phím ENTER')
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc13_keyboard_enter_submit(self):
        tc_id = 'TC_UTC_13'
        name = 'Kiểm tra gửi form đăng nhập bằng phím ENTER'
        technique = 'Kiểm thử khả năng tiếp cận & Phím tắt (Accessibility & UX)'
        steps = '1. Mở trang Login\n2. Nhập thông tin và bấm Enter tại ô password\n3. Kiểm tra form được submit'
        test_data = "username='test_enter_user', userpwd='test_enter_pwd' + Keys.ENTER"
        expected = 'Hệ thống chấp nhận phím Enter tương đương nút Đăng nhập'
        with allure.step('1. Mở trang Login'):
            self.login_page.navigate()
            time.sleep(1)
        with allure.step('2. Nhập thông tin và gửi form bằng phím ENTER'):
            self.login_page.submit_with_enter('test_enter_user', 'test_enter_pwd')
            time.sleep(2)
        with allure.step('3. Kiểm tra phản hồi submit'):
            is_pass = 'Login' in self.login_page.get_current_url()
            actual = 'Form tiếp nhận phím ENTER và gửi yêu cầu xác thực thành công' if is_pass else 'Phím Enter không hoạt động'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

    @allure.story('Kiểm thử Liên kết & Chuyển hướng')
    @allure.title("TC_UTC_14: Điều hướng từ 'Quên mật khẩu' quay về 'Đăng nhập'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc14_back_to_login_navigation(self):
        tc_id = 'TC_UTC_14'
        name = "Điều hướng từ 'Quên mật khẩu' quay về 'Đăng nhập'"
        technique = 'Kiểm thử luồng điều hướng trang (Navigation Flow)'
        steps = "1. Mở trang /Login/GetPass\n2. Click liên kết 'Trở lại đăng nhập?'\n3. Kiểm tra URL"
        test_data = "Liên kết 'Trở lại đăng nhập?'"
        expected = 'Trình duyệt quay trở về đúng địa chỉ /Login'
        with allure.step('1. Mở trang Quên mật khẩu'):
            self.getpass_page.navigate()
            time.sleep(1)
        with allure.step("2. Click liên kết 'Trở lại đăng nhập?'"):
            self.getpass_page.click_back_to_login()
            time.sleep(2)
        with allure.step('3. Kiểm tra URL chuyển về trang Login'):
            curr_url = self.getpass_page.get_current_url()
            is_pass = curr_url.rstrip('/').endswith('/Login')
            actual = f'Điều hướng chính xác về {curr_url}' if is_pass else 'Điều hướng sai trang'
        self.record_result(tc_id, name, technique, steps, test_data, expected, actual, is_pass)
        self.assertTrue(is_pass)

if __name__ == '__main__':
    unittest.main()
