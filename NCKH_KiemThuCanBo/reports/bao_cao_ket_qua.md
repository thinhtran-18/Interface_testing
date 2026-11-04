# BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG 
**Dự án:** NCKH_KiemThuCanBo  
**Học phần/Nội dung:** Kiểm thử giao diện Web hệ thống quản trị (`main.hau.edu.vn`)  
**Người thực hiện:** Chu Bách Trúc Mai  

---

## 1. Mục tiêu kiểm thử
* Kiểm tra tính năng tìm kiếm thông tin/phần mềm trên cổng quản trị chính.
* Kiểm tra chức năng lọc danh mục phần mềm theo nhóm chức năng (Hành chính, Quản lý đào tạo, ...).
* Tự động hóa các thao tác tương tác giao diện bằng script Python kết hợp Selenium WebDriver và mô hình Page Object Model (POM).

---

## 2. Kết quả thực hiện Test Case

| Mã Test Case | Tên Chức Năng / Thao Tác | Kết Quả Mong Đợi | Kết Quả Thực Tế (Selenium) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- |
| **WEB-01** | Tìm kiếm phần mềm ("Văn bản điều hành") | Hệ thống nhận diện từ khóa và lọc ra đúng các thẻ ứng dụng khớp từ khóa. | Ô tìm kiếm (`#searchInput`) hoạt động mượt mà, tự động điền từ khóa và trả về chính xác **1 kết quả** phần mềm "Văn bản điều hành". | **ĐẠT (Passed)** |
| **WEB-02** | Lọc theo nhóm chức năng ("Hành chính") | Giao diện thu gọn danh sách theo danh mục nhóm chức năng đã chọn. | Nút lọc thuộc nhóm Hành chính (`#filterTabs > button:nth-child(3)`) được kích hoạt thành công, làm nổi bật trạng thái chọn và hiển thị danh mục tương ứng. | **ĐẠT (Passed)** |
| **WEB-03** | Mở thẻ chi tiết phần mềm | Thao tác click vào thẻ điều hướng người dùng sang giao diện/tab chức năng của ứng dụng. | Trình duyệt nhận diện đúng phần tử thẻ (Card element) qua XPath, thực hiện click thành công và mở ra giao diện làm việc của phần mềm "Văn bản điều hành". | **ĐẠT (Passed)** |

---

## 3. Nhận xét & Đánh giá
* **Ưu điểm:** Script chạy ổn định nhờ áp dụng cơ chế `WebDriverWait` (Explicit Wait) giúp khắc phục triệt để các lỗi xung đột do tốc độ tải trang thực tế.
* **Cấu trúc mã nguồn:** Tổ chức mã theo mô hình Page Object Model với thư mục `pages/` và `tests/` giúp dễ dàng bảo trì và mở rộng thêm các kịch bản kiểm thử mới trong các tuần tới.

---
## 4. Minh chứng hình ảnh (Evidence)
* **Hình ảnh kết quả thực thi Test Case (WEB-01, WEB-02, WEB-03):** 

  ![Minh chứng kết quả chạy test 2](/evidence/test.png)
  ![Minh chứng kết quả chạy test mới](/evidence/test_chon_tim_kiem.png)
  ![Minh chứng kết quả chạy test mới](evidence/phan_loai.png)
  ![Minh chứng kết quả chạy test mới](evidence/chuyen_trang.png) 

  # BÁO CÁO TỔNG THỂ NHIỆM VỤ & KẾT QUẢ KIỂM THỬ (NCKH_KiemThuCanBo)

- **Hệ thống kiểm thử:** Cổng thông tin Cán bộ HAU (`https://main.hau.edu.vn`)
- **Hạng mục:** Kiểm thử tự động chức năng Tìm kiếm & Bộ lọc danh mục
- **Công cụ:** Python 3.13.5 + Selenium WebDriver

---

## 1. Tiến độ thực hiện nhiệm vụ

| STT | Hạng mục công việc | File / Thư mục kết quả | Trạng thái | Hoàn thành (%) |
| :-: | :--- | :--- | :-: | :-: |
| 1 | Khảo sát giao diện & DOM Selector | `test_cases/khao_sat_web.md` | Hoàn thành | **100%** |
| 2 | Thiết kế kịch bản kiểm thử (Test Cases) | `test_cases/tc_01_tra_cuu.md` | Hoàn thành | **100%** |
| 3 | Thiết lập môi trường & Base Page | `.venv`, `pages/base_page.py`, `smoke_test.py` | Hoàn thành | **100%** |
| 4 | Xây dựng script kiểm thử tự động | `tests/test_search.py` | Hoàn thành | **100%** |
| 5 | Chạy kiểm thử & Chụp bằng chứng | Thư mục `evidence/` | Hoàn thành | **100%** |
| 6 | Tổng hợp báo cáo kết quả | `reports/bao_cao_ket_qua.md` | Hoàn thành | **100%** |
| | **TỔNG TIẾN ĐỘ NHIỆM VỤ** | | **Hoàn tất** | **100%** |

---

## 2. Thống kê kết quả kiểm thử theo tỷ lệ (%)

### 2.1. Tỷ lệ Đạt / Lỗi (Pass / Fail Rate)
- **Tổng số kịch bản thực thi:** 06 Test Cases (100%)
- **Số kịch bản Đạt (PASSED):** 06/06 (**100%**)
- **Số kịch bản Lỗi (FAILED):** 00/06 (**0%**)
- **Số kịch bản Bị chặn (BLOCKED):** 00/06 (**0%**)

### 2.2. Tỷ trọng bao phủ theo nhóm trường hợp kiểm thử

| Phân nhóm kiểm thử | Mã Test Case | Số lượng | Tỷ trọng (%) | Tỷ lệ Pass (%) |
| :--- | :--- | :-: | :-: | :-: |
| Kiểm thử truy cập chưa xác thực (Unauthenticated) | `TC_01` | 1 | 16.67% | **100%** |
| Kiểm thử đầu vào không hợp lệ / XSS (Invalid Input) | `TC_02` | 1 | 16.67% | **100%** |
| Kiểm thử biên / Khoảng trắng (Edge Case) | `TC_04` | 1 | 16.67% | **100%** |
| Kiểm thử không có kết quả & Xung đột bộ lọc | `TC_03`, `TC_05` | 2 | 33.32% | **100%** |
| Kiểm thử tìm kiếm hợp lệ & Mở phần mềm (Happy Path) | `TC_06` | 1 | 16.67% | **100%** |
| **TỔNG CỘNG** | **TC_01 -> TC_06** | **6** | **100.0%** | **100%** |