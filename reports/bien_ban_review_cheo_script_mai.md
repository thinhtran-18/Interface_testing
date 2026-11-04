# BIÊN BẢN REVIEW CHÉO MÃ NGUỒN KIỂM THỬ TỰ ĐỘNG (TUẦN 3 & TUẦN 4)

**Đề tài**: Nghiên cứu phương pháp kiểm thử giao diện người dùng áp dụng cho phần mềm quản lý cán bộ của Trường Đại học Kiến trúc Hà Nội  
**Người thực hiện Review**: **Nguyễn Quang Huy** (Lập trình viên chính)  
**Người được Review**: **Chu Bách Trúc Mai** (Lập trình viên chính)  
**Nhánh Git kiểm tra**: `origin/Mai` (Remote GitHub: `https://github.com/thinhtran-18/Interface_testing.git`)  
**Tập tin mã nguồn đối chiếu**: `tests/test_search.py` và `tests/pytest_search.py` (Bộ 10 kịch bản `TC_01` → `TC_10`)  
**Thời gian thực hiện**: 04/11/2026  

---

## 1. MỤC TIÊU VÀ PHẠM VI REVIEW CHÉO

Thực hiện theo đúng phân công nhiệm vụ Tuần 3 trong Đề cương NCKH (Trang 6 & Trang 14):
> *"Nguyễn Quang Huy: Sửa test biểu mẫu theo kết quả thực tế; bổ sung ảnh khi thất bại; review chéo script của Chu Bách Trúc Mai. Bàn giao: Script biểu mẫu ổn định, bằng chứng lỗi/script."*

Phạm vi đánh giá tập trung vào phân hệ **Tìm kiếm & Bộ lọc (Search/Filter & Access Control)** trên Cổng Quản trị chung `https://main.hau.edu.vn`.

---

## 2. NỘI DUNG ĐÁNH GIÁ CHI TIẾT

### 2.1. Độ bao phủ kịch bản kiểm thử (Test Coverage) – ĐẠT XUẤT SẮC ✅
Bộ mã nguồn của Chu Bách Trúc Mai bao phủ trọn vẹn 10 ca kiểm thử chức năng và phi chức năng:
- **Bảo mật & Kiểm soát truy cập (TC_01)**: Kiểm tra chặn truy cập trái phép khi chưa đăng nhập SSO.
- **Bảo mật mã độc & Ký tự đặc biệt (TC_02)**: Kiểm thử chuỗi XSS Payload (`!@#$%^&*()<script>alert(1)</script>`).
- **Xử lý dữ liệu biên (TC_03, TC_04, TC_05, TC_09)**: Kiểm thử từ khóa không tồn tại, chuỗi chỉ chứa khoảng trắng, chuỗi cực đại 255 ký tự (`"A" * 255`), và chuỗi có khoảng trắng thừa ở hai đầu.
- **Logic xung đột nghiệp vụ (TC_06)**: Kiểm tra xung đột logic khi nhập từ khóa thuộc nhóm này nhưng lại chọn tab bộ lọc của nhóm khác.
- **Tính năng tìm kiếm thông minh (TC_07, TC_08)**: Kiểm tra tính không phân biệt hoa/thường (Case Insensitivity) và tìm kiếm khớp một phần (Substring Partial Match).
- **Luồng nghiệp vụ chuẩn (TC_10 - Happy Path)**: Kiểm thử chu trình khép kín: Tìm kiếm → Lọc danh mục → Nhận diện thẻ phần mềm → Click mở ứng dụng.

### 2.2. Đánh giá kiến trúc mã nguồn (Code Architecture) – ĐẠT ✅
- **Cấu trúc Pytest**: Đã chuyển đổi thành công từ script dạng tuần tự sang chuẩn `pytest` với việc sử dụng fixture `@pytest.fixture(scope="module")` (`auth_driver`), giúp đăng nhập 1 lần duy nhất đầu phiên cho chuỗi test liên tiếp.
- **Cơ chế chờ (Waits)**: Sử dụng kết hợp giữa `WebDriverWait` tường minh (Explicit Wait) và `short_wait` (chờ 2s cho các ca kỳ vọng kết quả rỗng), giúp giảm thiểu thời gian chờ không cần thiết.
- **Cơ chế lưu bằng chứng (Evidence)**: Hàm `chup_bang_chung()` tự động lưu ảnh màn hình tương ứng với từng mã kịch bản (`evidence/TC_xx.png`).

### 2.3. Các hạn chế kỹ thuật phát hiện & Đề xuất cải tiến (Đã khắc phục) ⚠️ ➔ ✅

1. **Vấn đề Renderer Timeout khi tải trang trong môi trường Headless**:
   - *Phát hiện*: Script gốc khởi tạo Chrome với cấu hình mặc định (Page Load Strategy: `normal`), khiến trình duyệt chờ tải tất cả tài nguyên ngoài. Khi redirect SSO qua mạng trường, Selenium dễ bị treo ở `driver.get(URL)` và ném lỗi `ReadTimeoutError (120s)`.
   - *Giải pháp Huy đã tối ưu*: Bổ sung `options.page_load_strategy = "eager"` cùng các tham số `--no-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu` và `driver.set_page_load_timeout(30/60)`.
   - *Kết quả sau cải tiến*: Thời gian chạy toàn bộ 10 ca kiểm thử giảm từ nguy cơ timeout xuống chỉ còn **43.21 giây (10/10 PASSED)**.

2. **Xử lý làm sạch ô tìm kiếm (Input Cleaning)**:
   - *Nhận xét tốt*: Mai đã sử dụng tổ hợp phím ảo `Keys.CONTROL, "a"` kết hợp `Keys.BACKSPACE` trong hàm `reset_bo_loc_va_tim_kiem()`. Đây là cách xử lý chuẩn xác trên các input HTML5 có ràng buộc sự kiện động.

3. **Lưu ý về lệnh dừng người dùng trong script độc lập**:
   - *Phát hiện*: Trong tệp `test_search.py` (chạy script độc lập) có dòng lệnh `input(...)` ở cuối để chờ nhấn phím Enter. Điều này sẽ làm treo tiến trình nếu chạy tự động trên CI/CD hoặc chạy nền.
   - *Khuyến nghị*: Đã khuyến nghị sử dụng tệp `pytest_search.py` (tương ứng `tests/web/test_search.py`) làm chuẩn tích hợp chính thức của đề tài.

---

## 3. KẾT QUẢ CHẠY THỰC NGHIỆM ĐỐI CHỨNG TẠI LOCAL

Nguyễn Quang Huy đã tích hợp và thực thi trực tiếp bộ mã của Chu Bách Trúc Mai trên môi trường máy trạm:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\nckh2026\Interface_testing
configfile: pytest.ini
collected 10 items

tests/web/test_search.py::test_tc01_unauthenticated_access PASSED        [ 10%]
tests/web/test_search.py::test_tc02_xss_and_special_chars PASSED         [ 20%]
tests/web/test_search.py::test_tc03_non_existent_keyword PASSED          [ 30%]
tests/web/test_search.py::test_tc04_whitespace_only PASSED               [ 40%]
tests/web/test_search.py::test_tc05_max_length_255_chars PASSED          [ 50%]
tests/web/test_search.py::test_tc06_filter_mismatch PASSED               [ 60%]
tests/web/test_search.py::test_tc07_case_insensitive PASSED              [ 70%]
tests/web/test_search.py::test_tc08_partial_keyword_match PASSED         [ 80%]
tests/web/test_search.py::test_tc09_leading_trailing_spaces PASSED       [ 90%]
tests/web/test_search.py::test_tc10_happy_path_search_and_filter PASSED  [100%]

============================= 10 passed in 43.21s =============================
```

---

## 4. KẾT LUẬN VÀ THỐNG NHẤT

- **Đánh giá chung**: Bộ mã nguồn kiểm thử tìm kiếm và bộ lọc của Chu Bách Trúc Mai đạt chất lượng tốt, tính bao phủ cao, tuân thủ đúng định hướng kỹ thuật của nhóm.
- **Thống nhất bàn giao**: Bộ mã nguồn sau khi được Huy hỗ trợ tối ưu cấu hình Driver đã được tích hợp hoàn chỉnh vào kho mã chung để chuẩn bị cho buổi nghiệm thu nội bộ toàn nhóm.

---

**NGƯỜI LẬP BIÊN BẢN REVIEW**  
*(Ký và ghi rõ họ tên)*  

**Nguyễn Quang Huy**

