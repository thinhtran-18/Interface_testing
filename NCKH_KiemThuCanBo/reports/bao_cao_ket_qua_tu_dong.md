# BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG 

- **Thời gian xuất báo cáo:** 28/10/2026 15:53:25
- **Hệ thống kiểm thử:** `https://main.hau.edu.vn`
- **Tổng số Test Cases:** 10 kịch bản
- **Tỷ lệ Đạt (Pass Rate):** **100.00%** (10/10 PASS, 0/10 FAIL)
- **Tổng thời gian hệ thống xử lý:** 35.40s (Trung bình: 3.54s/TC)

## Bảng kết quả thực thi chi tiết

| Mã TC | Tên kịch bản | Nhóm kỹ thuật | Kết quả | Thời gian (s) | Bằng chứng (Screenshot) | Ghi chú |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **TC_01** | Truy cập khi chưa xác thực | Bảo mật & Xác thực | **PASS** | 8.74s | `evidence/TC_01_Unauthenticated.png` | Chặn truy cập và chuyển hướng SSO |
| **TC_02** | Tìm kiếm ký tự đặc biệt / XSS | Bảo mật & Dữ liệu rác | **PASS** | 4.31s | `evidence/TC_02_XSS_SpecialChars.png` | Xử lý an toàn, 0 kết quả |
| **TC_03** | Tìm kiếm từ khóa không tồn tại | Phủ định (Negative) | **PASS** | 4.17s | `evidence/TC_03_NonExistent.png` | Trả về 0 kết quả đúng kỳ vọng |
| **TC_04** | Tìm kiếm toàn khoảng trắng | Giá trị biên (Boundary) | **PASS** | 1.53s | `evidence/TC_04_WhitespaceOnly.png` | Giao diện không bị treo khi nhập dấu cách |
| **TC_05** | Chuỗi cực dài (255 ký tự) | Giá trị biên (Boundary) | **PASS** | 4.65s | `evidence/TC_05_MaxLength_255.png` | Không vỡ layout, trả về 0 kết quả |
| **TC_06** | Xung đột Từ khóa & Bộ lọc | Phủ định (Negative) | **PASS** | 4.99s | `evidence/TC_06_FilterMismatch.png` | Ẩn đúng các thẻ không thỏa mãn cả 2 điều kiện |
| **TC_07** | Tìm kiếm không phân biệt Hoa/Thường | Tương đương hợp lệ | **PASS** | 1.60s | `evidence/TC_07_CaseInsensitive.png` | Nhận diện tốt chữ thường toàn bộ |
| **TC_08** | Tìm kiếm một phần từ khóa (Substring) | Tương đương hợp lệ | **PASS** | 1.51s | `evidence/TC_08_PartialMatch.png` | Hỗ trợ tìm kiếm theo chuỗi con |
| **TC_09** | Từ khóa có khoảng trắng thừa 2 đầu | Giá trị biên (Boundary) | **PASS** | 1.48s | `evidence/TC_09_TrimSpaces.png` | Tự động cắt khoảng trắng (trim) |
| **TC_10** | Tìm kiếm chuẩn + Lọc Hành chính + Mở thẻ | Luồng chính (Happy Path) | **PASS** | 2.42s | `evidence/TC_10_HappyPath.png` | Mở phần mềm thành công |
