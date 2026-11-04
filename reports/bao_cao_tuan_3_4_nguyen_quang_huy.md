# BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI NCKH SINH VIÊN (TUẦN 3 & TUẦN 4)

**Trường Đại học Kiến trúc Hà Nội**  
**Đề tài**: Nghiên cứu phương pháp kiểm thử giao diện người dùng áp dụng cho phần mềm quản lý cán bộ của Trường Đại học Kiến trúc Hà Nội  
**Họ và tên sinh viên thực hiện**: **Nguyễn Quang Huy**  
**Vai trò**: Lập trình viên chính (Code chính) – Phụ trách nhóm Biểu mẫu, Xác thực Dữ liệu đầu vào & Cổng Quản lý văn bản  
**Nhóm trưởng**: Trần Văn Thịnh  
**Các thành viên trong nhóm**: Chu Bách Trúc Mai, Nguyễn Thị Cẩm Vân, Nguyễn Ngọc Thuỳ Trang  
**Thời gian báo cáo**: Tuần 3 & Tuần 4

---

## 1. BÁO CÁO TUẦN 3: CHẠY LẶP, SỬA TEST VÀ ĐỐI CHIẾU BẰNG CHỨNG

### 1.1. Mục tiêu
- Đảm bảo tính ổn định của script thông qua chạy lặp nhiều lần.
- Củng cố và bổ sung đầy đủ bằng chứng minh chứng tự động.
- Thực hiện review chéo bộ mã kiểm thử với Chu Bách Trúc Mai và khắc phục các edge cases giao diện.

### 1.2. Các công việc đã thực hiện

1. **Khắc phục lỗi Renderer Timeout & Tối ưu hóa Browser Driver** (`tests/web/conftest.py`, `tests/web/test_login.py`, `tests/web/test_dashboard.py`):
   - Chuyển đổi chiến lược tải trang sang `page_load_strategy = 'eager'` (chỉ chờ `DOMContentLoaded`) kết hợp các flag `--no-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu` giúp giảm thời gian tải trang từ 60s xuống còn 3.5s và loại bỏ triệt để nguy cơ treo render.
   - Thêm cơ chế đặt `driver.set_page_load_timeout(60)`.
   - Nâng cấp phương thức nhập dữ liệu `enter_username()` và `enter_password()` trong `pages/login_page.py` bằng tổ hợp phím `CONTROL + 'a'` và `BACKSPACE` trước khi `clear()` để bảo đảm input HTML5 được làm sạch hoàn toàn giữa các ca test.

2. **Bổ sung hook tự động chụp ảnh khi test thất bại** (`tests/web/conftest.py`):
   - Triển khai hook `pytest_runtest_makereport` của Pytest để tự động bắt sự kiện `call.failed`, trích xuất đối tượng WebDriver và lưu ảnh chụp màn hình định danh theo tên test case và dấu thời gian (`evidence/web/FAIL_<test_name>_<timestamp>.png`).

3. **Củng cố bộ kịch bản biểu mẫu SSO (8 ca `WEB-FORM-01` → `WEB-FORM-08`)**:
   - Hoàn thiện ca `test_WEB_FORM_02_password_visibility_toggle`: nhập mật khẩu mẫu trước khi toggle con mắt để tuân thủ 100% đặc tả ma trận kiểm thử và bắt đúng sự kiện thay đổi type `'password'` ↔ `'text'`.
   - Hoàn thiện ca `test_WEB_FORM_08_successful_login_with_valid_credentials`: thêm khoảng chờ ổn định form sau ca nhập sai thông tin trước đó, bảo đảm đăng nhập thành công vào Cổng chính.

4. **Review chéo bộ mã nguồn của Chu Bách Trúc Mai từ nhánh `origin/Mai`**:
   - Đã pull nhánh `origin/Mai` từ remote GitHub (`https://github.com/thinhtran-18/Interface_testing.git`).
   - Rà soát chi tiết bộ 10 kịch bản kiểm thử Tìm kiếm, Bộ lọc & Phân quyền (`TC_01` → `TC_10`) trong `tests/pytest_search.py`.
   - **Phát hiện & Đóng góp kỹ thuật**: Script gốc của Mai dùng chiến lược tải trang mặc định (`normal`) dẫn đến nguy cơ Renderer Timeout 120s khi tải trang SSO trong môi trường headless. Huy đã hỗ trợ cấu hình `page_load_strategy = 'eager'` kết hợp `--no-sandbox`, `--disable-gpu`, `--disable-dev-shm-usage` và `set_page_load_timeout(30/60)`.
   - **Kết quả thực nghiệm đối chứng**: Toàn bộ 10/10 ca kiểm thử của Mai chạy thành công mượt mà trong **43.21 giây (100% PASSED)**.
   - **Biên bản bàn giao**: Đã lập Biên bản review chéo mã nguồn chi tiết tại [`reports/bien_ban_review_cheo_script_mai.md`](file:///d:/nckh2026/Interface_testing/reports/bien_ban_review_cheo_script_mai.md).

---

## 2. BÁO CÁO TUẦN 4: MỞ RỘNG KIỂM THỬ ĐẦY ĐỦ CÁC TRANG CẦN THIẾT, CHẠY BỘ TỰ ĐỘNG CUỐI VÀ HOÀN THIỆN SẢN PHẨM

### 2.1. Mục tiêu
- Mở rộng phạm vi kiểm thử tự động sang **tất cả các trang cần thiết** mà tài khoản được phân quyền theo khảo sát thực tế.
- Thực thi lần chạy tự động cuối cùng qua 3 vòng lặp độc lập (3 Iterations) để chứng minh độ bền vững (Stability Rate = 100%, Flaky Rate = 0%).
- Đóng gói toàn bộ mã nguồn, dữ liệu log, ảnh bằng chứng và hoàn thiện báo cáo nghiệm thu.

### 2.2. Các công việc đã thực hiện

1. **Xây dựng Page Object & Bộ kiểm thử Cổng Quản lý văn bản điều hành (`vanban.hau.edu.vn`)**:
   - Khảo sát thực tế hệ thống Quản lý văn bản điều hành sau khi xác thực: bóc tách 31 liên kết menu, 9 ô tra cứu và 7 khối widget dashboard.
   - Xây dựng lớp Page Object `VanBanPage` (`pages/vanban_page.py`).
   - Xây dựng bộ kiểm thử tự động `tests/web/test_vanban.py` gồm 5 kịch bản:
     - `WEB-VB-01`: Xác thực điều hướng Cổng Văn bản và kiểm tra tiêu đề trang.
     - `WEB-VB-02`: Kiểm tra cấu trúc các phân hệ menu cốt lõi (Trình ký, Văn bản đi, Văn bản đến, Lịch, Quản lý công việc).
     - `WEB-VB-03`: Kiểm tra các ô tra cứu nhanh theo nghiệp vụ.
     - `WEB-VB-04`: Kiểm tra bộ lọc khoảng thời gian (`txtTuNgay`, `txtDenNgay`).
     - `WEB-VB-05`: Kiểm tra sự hiện diện của các khối Widget/Thống kê trên Dashboard.

2. **Chạy lặp thực nghiệm 3 vòng (3 Iterations) toàn diện trên tất cả các trang**:
   - Sử dụng script tự động hóa `reports/run_stability.py` chạy tuần tự qua 3 bộ test:
     1. `tests/web/test_login.py` (8 test cases)
     2. `tests/web/test_dashboard.py` (5 test cases)
     3. `tests/web/test_vanban.py` (5 test cases)

### 2.3. Bảng tổng hợp kết quả chạy lặp 3 lần (3 Iterations)

| STT | Mã / Tên Kịch bản Kiểm thử | Phân hệ / Trang | Lần 1 | Lần 2 | Lần 3 | Tỷ lệ ổn định | Trạng thái |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | `test_WEB_FORM_01_elements_display_and_attributes` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 2 | `test_WEB_FORM_02_password_visibility_toggle` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 3 | `test_WEB_FORM_03_remember_login_checkbox_toggle` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 4 | `test_WEB_FORM_04_empty_credentials_validation` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 5 | `test_WEB_FORM_05_empty_password_validation` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 6 | `test_WEB_FORM_06_empty_username_validation` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 7 | `test_WEB_FORM_07_invalid_credentials_error_message` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 8 | `test_WEB_FORM_08_successful_login_with_valid_credentials` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 9 | `test_dashboard_header_and_account` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 10 | `test_filter_tabs_presence` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 11 | `test_search_filters_modules` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 12 | `test_quan_ly_nhan_su_module_is_listed` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 13 | `test_quan_ly_nhan_su_module_permission_status` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 14 | `test_WEB_VANBAN_01_navigation_and_title` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 15 | `test_WEB_VANBAN_02_sidebar_menu_structure` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 16 | `test_WEB_VANBAN_03_quick_search_inputs` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 17 | `test_WEB_VANBAN_04_date_filter_fields` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 18 | `test_WEB_VANBAN_05_dashboard_widgets_presence` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |

- **Tổng số ca kiểm thử tự động**: **18 Test Cases** bao phủ 3 phân hệ cốt lõi.
- **Tổng số lượt chạy thực nghiệm**: 18 × 3 = **54 lượt test**.
- **Tỷ lệ thành công (Pass Rate)**: **100.0% (54/54 PASSED)**.
- **Tỷ lệ lỗi chập chờn (Flaky Rate)**: **0%**.
- **Thời gian thực thi trung bình mỗi lượt**: **~49.8 giây** cho toàn bộ 18 test cases.

---

## 3. DANH MỤC CÁC CA KHÔNG TỰ ĐỘNG HÓA ĐƯỢC (GIỚI HẠN PHẠM VI)

Theo yêu cầu của đề tài và tiêu chuẩn an toàn thông tin:
1. **Module Quản lý nhân sự**: Bị vô hiệu hóa giao diện (`app-disabled`) đối với tài khoản cán bộ giảng viên thông thường; đánh dấu trạng thái **BỊ CHẶN (BLOCKED)**.
2. **Nghiệp vụ Tạo / Xóa dữ liệu văn bản thật**: Không tự động hóa trên môi trường production của Nhà trường để tránh gây sai lệch dữ liệu hành chính thực tế.
3. **Thao tác Tải tệp đính kèm**: Phụ thuộc hộp thoại chọn file của Hệ điều hành (Windows File Dialog), cần kiểm thử thủ công kết hợp hoặc dùng công cụ giả lập upload HTTP trực tiếp.

---

## 4. SẢN PHẨM BÀN GIAO TUẦN 3 & TUẦN 4

1. **Mã nguồn kiểm thử tự động (Selenium + Pytest)**:
   - `pages/login_page.py`: Page Object biểu mẫu xác thực SSO.
   - `pages/dashboard_page.py`: Page Object Cổng quản trị chung.
   - `pages/vanban_page.py`: Page Object Cổng Quản lý văn bản điều hành.
   - `tests/web/conftest.py`: Fixtures và hook tự động bắt ảnh lỗi.
   - `tests/web/test_login.py`: 8 ca kiểm thử biểu mẫu.
   - `tests/web/test_dashboard.py`: 5 ca kiểm thử cổng quản trị.
   - `tests/web/test_vanban.py`: 5 ca kiểm thử cổng quản lý văn bản.
2. **Công cụ thực nghiệm & Báo cáo kết quả**:
   - `reports/run_stability.py`: Bộ chạy lặp 3 vòng đo độ ổn định và xuất biên bản.
   - `reports/Bien_ban_chay_lap_tuan_4.md`: Biên bản kết quả chạy lặp chi tiết.
   - Các file báo cáo HTML: `reports/report_*.html`.
3. **Kho hình ảnh minh chứng thực tế (`evidence/web/`)**:
   - `vanban_dashboard_widgets.png`: Minh chứng giao diện Dashboard Quản lý văn bản.
   - `vanban_survey.png`: Minh chứng khảo sát Cổng Quản lý văn bản.
   - `post_login.png`: Minh chứng Cổng quản trị sau đăng nhập.
   - `WEB_FORM_04_empty_credentials.png`: Minh chứng thông báo lỗi biểu mẫu rỗng.
   - `WEB_FORM_07_invalid_credentials.png`: Minh chứng thông báo sai tài khoản.

---

**XÁC NHẬN CỦA NHÓM TRƯỞNG**  
*(Ký và ghi rõ họ tên)*  

**Trần Văn Thịnh**

**NGƯỜI THỰC HIỆN BÁO CÁO**  
*(Ký và ghi rõ họ tên)*  

**Nguyễn Quang Huy**
