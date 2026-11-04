# BIÊN BẢN CHẠY LẶP VÀ ĐÁNH GIÁ ĐỘ ỔN ĐỊNH SCRIPT KIỂM THỬ 
**Dự án:** Kiểm thử tự động Cổng thông tin Cán bộ - Trường Đại học Kiến trúc Hà Nội (`main.hau.edu.vn`)  
**Người thực hiện:** Chu Bách Trúc Mai  
**Ngày lập biên bản:** 30/10/2026  

---

## 1. MỤC ĐÍCH VÀ PHẠM VI KIỂM THỬ
- **Mục đích:** Kiểm tra độc lập trên môi trường đã ghi nhận, thực hiện chạy lặp lại chuỗi kịch bản kiểm thử nhiều lần nhằm đánh giá mức độ ổn định (Stability Rate), phát hiện lỗi chập chờn (Flaky Test) và hoàn thiện gói bằng chứng Web.
- **Phạm vi kiểm thử:** 
  - Phân hệ Dashboard & Xác thực (Code của Nguyễn Quang Huy: `tests/test_dashboard.py`).
  - Phân hệ Tìm kiếm, Bộ lọc & Bảo mật (Code của Chu Bách Trúc Mai: `tests/pytest_search.py`).

---

## 2. KẾT QUẢ CHẠY LẶP 3 LẦN LIÊN TIẾP (3 ITERATIONS EXECUTION LOG)

| STT | Mã / Tên Kịch bản Kiểm thử (Test Case) | Lần chạy 1 (Run 1) | Lần chạy 2 (Run 2) | Lần chạy 3 (Run 3) | Tỷ lệ Ổn định | Ghi chú & Minh chứng |
| :-: | :--- | :-: | :-: | :-: | :-: | :--- |
| **1** | `test_dashboard_header_and_account` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Xác thực Header & Thương hiệu HAU |
| **2** | `test_filter_tabs_presence` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Kiểm tra 5 tab danh mục chức năng |
| **3** | `test_search_filters_modules` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Tìm kiếm động với từ khóa "nhân sự" |
| **4** | `test_quan_ly_nhan_su_module_is_listed` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Xác minh tồn tại module nhân sự |
| **5** | `test_quan_ly_nhan_su_module_permission_status` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Kiểm tra phân quyền `disabled` |
| **6** | `test_tc01_unauthenticated_access` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Bảo mật: Chặn truy cập chưa đăng nhập |
| **7** | `test_tc02_xss_and_special_chars` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Xử lý an toàn chuỗi XSS Payload |
| **8** | `test_tc03_non_existent_keyword` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Từ khóa không tồn tại (0 kết quả) |
| **9** | `test_tc04_whitespace_only` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Giá trị biên: Khoảng trắng |
| **10** | `test_tc05_max_length_255_chars` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Giá trị biên trên: 255 ký tự |
| **11** | `test_tc06_filter_mismatch` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Xung đột từ khóa & Bộ lọc |
| **12** | `test_tc07_case_insensitive` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Không phân biệt hoa/thường |
| **13** | `test_tc08_partial_keyword_match` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Tìm kiếm một phần từ khóa (Substring) |
| **14** | `test_tc09_leading_trailing_spaces` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Xử lý khoảng trắng thừa hai đầu |
| **15** | `test_tc10_happy_path_search_and_filter` | PASSED ✅ | PASSED ✅ | PASSED ✅ | **100%** | Luồng chuẩn (Happy Path) hoàn chỉnh |

---

## 3. THỐNG KÊ TỔNG HỢP & ĐÁNH GIÁ ĐỘ ỔN ĐỊNH
- **Tổng số ca kiểm thử trong Test Suite:** 15 Test Cases.
- **Tỷ lệ thành công trung bình (Pass Rate):** **100%** xuyên suốt qua cả 3 lượt chạy lặp.
- **Tổng thời gian thực thi trung bình:** ~55 giây / toàn bộ bộ test.
- **Tỷ lệ lỗi chập chờn (Flaky Rate):** **0%** (Không ghi nhận bất kỳ trường hợp timeout hay rớt mạng ngẫu nhiên nhờ áp dụng chuẩn mô hình `WebDriverWait` và Page Object Model).

---

## 4. DANH MỤC GÓI BẰNG CHỨNG WEB ĐÍNH KÈM
1. **Báo cáo HTML tự động:**
   - `reports/full_web_suite_report.html`: Báo cáo chi tiết kết quả 15 ca test đạt PASSED.
2. **Thư mục ảnh chụp màn hình minh chứng (`evidence/`):**
   - Lưu trữ đầy đủ hình ảnh thực tế tại từng bước kịch bản kiểm thử (đăng nhập SSO, thao tác tab, kết quả bộ lọc, trạng thái phân quyền bảo mật).

