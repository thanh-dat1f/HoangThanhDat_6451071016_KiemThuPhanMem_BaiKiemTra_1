import os
import sys
import shutil
import subprocess
import pytest
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from utils.excel_exporter import export_test_cases_to_excel

def main():
    print('=' * 80)
    print(' HỆ THỐNG KIỂM THỬ TỰ ĐỘNG - VĂN PHÒNG ĐIỆN TỬ UTC ')
    print(' TÍCH HỢP XUẤT ĐỒNG THỜI: EXCEL REPORT + ALLURE DASHBOARD (ĐỒNG BỘ 100%)')
    print('=' * 80)
    allure_results_dir = os.path.join(PROJECT_ROOT, 'reports', 'allure-results')
    allure_report_dir = os.path.join(PROJECT_ROOT, 'reports', 'allure-report')
    excel_file = os.path.join(PROJECT_ROOT, 'reports', 'BaoCao_KiemThu_UTC.xlsx')
    print('\n[BƯỚC 0/3] Dọn dẹp dữ liệu Allure cũ để đồng bộ chính xác với Báo cáo Excel...')
    if os.path.exists(allure_results_dir):
        shutil.rmtree(allure_results_dir, ignore_errors=True)
    os.makedirs(allure_results_dir, exist_ok=True)
    print('\n[BƯỚC 1/3] Đang thực thi Suite Kiểm Thử (tests/test_utc_cases.py) bằng Pytest + Selenium...')
    target_suite = os.path.join(PROJECT_ROOT, 'tests', 'test_utc_cases.py')
    pytest_args = [target_suite, f'--alluredir={allure_results_dir}', '--clean-alluredir', '-v']
    exit_code = pytest.main(pytest_args)
    test_module = sys.modules.get('test_utc_cases') or sys.modules.get('tests.test_utc_cases')
    results = test_module.UTCTestAutomationSuite.results if test_module else []
    total_run = len(results)
    pass_count = sum((1 for r in results if r.get('status') == 'PASS'))
    fail_count = total_run - pass_count
    allure_json_files = [f for f in os.listdir(allure_results_dir) if f.endswith('-result.json')]
    allure_count = len(allure_json_files)
    print(f'\n[BƯỚC 2/3] Đang xuất Báo cáo Excel (.xlsx) cho {total_run} Test Cases...')
    print(f'  - Số ca ghi nhận trong Allure JSON: {allure_count}')
    print(f'  - Số ca ghi nhận trong Excel Table: {total_run}')
    if allure_count == total_run:
        print(f'  => [XÁC NHẬN]: Dữ liệu Allure và Excel ĐỒNG NHẤT 100% ({total_run}/{total_run} TCs, {pass_count} PASS, {fail_count} FAIL)')
    else:
        print(f'  => [LƯU Ý]: Chênh lệch {abs(allure_count - total_run)} test case giữa Allure và Excel.')
    exported_excel = export_test_cases_to_excel(results, excel_file)
    print('\n[BƯỚC 3/3] Đang biên dịch Allure HTML Dashboard Report...')
    try:
        subprocess.run(['allure', 'generate', allure_results_dir, '--single-file', '-o', allure_report_dir, '--clean'], check=True, capture_output=True, shell=True)
        print(f'[XUẤT ALLURE THÀNH CÔNG]: {allure_report_dir}')
        allure_success = True
    except Exception as e:
        print(f'[LƯU Ý ALLURE]: Không thể tạo Allure HTML Report tự động ({e}).')
        allure_success = False
    print('\n' + '=' * 80)
    print(' TỔNG KẾT KẾT QUẢ KIỂM THỬ TỰ ĐỘNG:')
    print('=' * 80)
    print(f"{'MÃ TC':<12} | {'TÊN KỊCH BẢN KIỂM THỬ':<40} | {'TRẠNG THÁI':<10}")
    print('-' * 80)
    for r in results:
        print(f"{r['id']:<12} | {r['name'][:40]:<40} | {r['status']:<10}")
    print('=' * 80)
    print(f'Tổng số Test Cases : {total_run}')
    print(f'Số ca PASS         : {pass_count}')
    print(f'Số ca FAIL         : {fail_count}')
    print(f'Tỷ lệ đạt (Rate)   : {(round(pass_count / total_run * 100, 1) if total_run > 0 else 0)}%')
    print(f'Báo cáo Excel      : {exported_excel}')
    if allure_success:
        print(f'Báo cáo Allure     : {allure_report_dir}')
        print('  => Để mở giao diện Allure trên trình duyệt, chạy lệnh:')
        print(f'     allure open reports/allure-report')
    print(f"Ảnh minh chứng     : {os.path.abspath('screenshots')}")
    print('=' * 80)
    return exit_code
if __name__ == '__main__':
    sys.exit(main())
