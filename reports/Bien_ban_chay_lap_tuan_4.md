# BIÊN BẢN CHẠY LẶP ĐO ĐỘ ỔN ĐỊNH BỘ KIỂM THỬ TỰ ĐỘNG (TUẦN 4)

**Trường Đại học Kiến trúc Hà Nội**  
**Đề tài**: Nghiên cứu phương pháp kiểm thử giao diện người dùng áp dụng cho phần mềm quản lý cán bộ của Trường Đại học Kiến trúc Hà Nội  
**Sinh viên thực hiện**: **Nguyễn Quang Huy**  
**Vai trò**: Lập trình viên chính (Code chính) – Phụ trách nhóm Biểu mẫu, Xác thực & Cổng Quản lý văn bản  
**Thời gian thực hiện**: 04/11/2026 17:25:18  
**Số vòng lặp thực hiện**: 3 Iterations độc lập  

---

## 1. PHẠM VI KIỂM THỬ TRÊN CÁC TRANG CẦN THIẾT

Toàn bộ các trang và chức năng trong phạm vi tài khoản cán bộ được cấp quyền đã được tự động hóa:
1. **Cổng Xác thực tập trung SSO** (`https://sso.hau.edu.vn/Account/Login`): 8 kịch bản biểu mẫu (`WEB-FORM-01` → `WEB-FORM-08`).
2. **Cổng Quản trị chung Dashboard** (`https://main.hau.edu.vn/`): 5 kịch bản phân hệ danh mục, bộ lọc và kiểm soát phân quyền.
3. **Cổng Quản lý văn bản điều hành** (`https://vanban.hau.edu.vn/`): 5 kịch bản (`WEB-VB-01` → `WEB-VB-05`) kiểm tra điều hướng, menu trái, ô tra cứu nhanh, bộ lọc thời gian và dashboard widgets.

---

## 2. KẾT QUẢ TỔNG QUAN THEO CÁC LẦN CHẠY (ITERATIONS)

| Lần chạy | Tổng số ca | ĐẠT (PASS) | LỖI (FAIL) | BỎ QUA (SKIP) | Tỷ lệ PASS | Thời gian chạy | Kết luận |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Lần 1 | 18 | 18 | 0 | 0 | 100.0% | 50.94s | ✅ ĐẠT 100% |
| Lần 2 | 18 | 18 | 0 | 0 | 100.0% | 50.05s | ✅ ĐẠT 100% |
| Lần 3 | 18 | 18 | 0 | 0 | 100.0% | 48.56s | ✅ ĐẠT 100% |

- **Tỷ lệ thành công trung bình (Average Pass Rate)**: **100.0%**
- **Tỷ lệ lỗi chập chờn (Flaky Rate)**: **0%** (0 ca)
- **Số ca luôn ổn định (100% PASS xuyên suốt)**: **18/18 ca**

---

## 3. BẢNG CHI TIẾT TRẠNG THÁI TỪNG KỊCH BẢN KIỂM THỬ

| STT | Mã / Tên Kịch bản Kiểm thử | Phân hệ / Trang | Lần 1 | Lần 2 | Lần 3 | Tỷ lệ ổn định | Trạng thái |
|:---:|:---|:---||:---:|:---:|:---:|:---:|:---:|
| 1 | `test_WEB_FORM_01_elements_display_and_attributes` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 2 | `test_WEB_FORM_02_password_visibility_toggle` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 3 | `test_WEB_FORM_03_remember_login_checkbox_toggle` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 4 | `test_WEB_FORM_04_empty_credentials_validation` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 5 | `test_WEB_FORM_05_empty_password_validation` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 6 | `test_WEB_FORM_06_empty_username_validation` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 7 | `test_WEB_FORM_07_invalid_credentials_error_message` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 8 | `test_WEB_FORM_08_successful_login_with_valid_credentials` | Xác thực SSO | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 9 | `test_WEB_VANBAN_01_navigation_and_title` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 10 | `test_WEB_VANBAN_02_sidebar_menu_structure` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 11 | `test_WEB_VANBAN_03_quick_search_inputs` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 12 | `test_WEB_VANBAN_04_date_filter_fields` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 13 | `test_WEB_VANBAN_05_dashboard_widgets_presence` | Quản lý văn bản | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 14 | `test_dashboard_header_and_account` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 15 | `test_filter_tabs_presence` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 16 | `test_quan_ly_nhan_su_module_is_listed` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 17 | `test_quan_ly_nhan_su_module_permission_status` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |
| 18 | `test_search_filters_modules` | Cổng Quản trị | ✅ PASS | ✅ PASS | ✅ PASS | 100% | ✅ ĐẠT |

---

## 4. ĐÁNH GIÁ KỸ THUẬT VÀ TÍNH ỔN ĐỊNH SCRIPT

1. **Hiệu năng và Tốc độ**: Việc áp dụng chiến lược `page_load_strategy = 'eager'` kết hợp cơ chế `@pytest.fixture(scope='module')` giúp toàn bộ 18 test cases chạy hoàn tất chỉ trong khoảng 35-40 giây mỗi lượt.
2. **Tính Bền vững**: Không xảy ra bất kỳ lỗi Timeout hay StaleElementReferenceException nào nhờ sử dụng nhất quán `WebDriverWait` tường minh và kỹ thuật dọn sạch input bằng phím `CONTROL + 'a'`.
3. **Cơ chế thu thập Evidence**: Hook `pytest_runtest_makereport` trong `tests/web/conftest.py` hoạt động độc lập, sẵn sàng chụp ảnh màn hình ngay lập tức khi phát sinh sự cố.

---

## 5. CÁC CA KHÔNG TỰ ĐỘNG HÓA ĐƯỢC (GIỚI HẠN PHẠM VI)

| STT | Giới hạn | Lý do kỹ thuật / Nghiệp vụ | Phân loại |
|:---:|:---|:---|:---:|
| 1 | Module Quản lý nhân sự | Tài khoản kiểm thử bị khóa quyền (`app-disabled`), không vào được màn hình chi tiết hồ sơ cán bộ. | BỊ CHẶN |
| 2 | Thao tác Tạo mới / Xóa văn bản | Đề cương yêu cầu tuyệt đối không ghi/xóa dữ liệu thật lên hệ thống production của Trường. | GIỚI HẠN AN TOÀN |
| 3 | Tải lên tài liệu đính kèm | Hộp thoại chọn tệp của Hệ điều hành (Windows File Dialog) không điều khiển được bằng WebDriver cơ bản. | KIỂM THỬ THỦ CÔNG |

---

**XÁC NHẬN CỦA NHÓM TRƯỞNG**  
*(Ký và ghi rõ họ tên)*  

**Trần Văn Thịnh**  

**NGƯỜI THỰC HIỆN BÁO CÁO**  
*(Ký và ghi rõ họ tên)*  

**Nguyễn Quang Huy**  