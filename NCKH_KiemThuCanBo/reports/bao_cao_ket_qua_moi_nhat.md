# BIÊN BẢN CHẠY KIỂM THỬ TỰ ĐỘNG (TEST EXECUTION REPORT)
**Dự án:** NCKH - Kiểm thử tự động cổng thông tin Đại học Kiến trúc Hà Nội (vanban.hau.edu.vn)  
**Người thực hiện (QA):** Chu Bách Trúc Mai  
**Giai đoạn:** Tuần 4 - Đánh giá độ ổn định và thu thập bằng chứng

## 1. THÔNG TIN MÔI TRƯỜNG (ENVIRONMENT STATUS)
- **Hệ điều hành:** Windows 10 (10.0.19045-SP0)
- **Ngôn ngữ/Framework:** Python 3.13.5 | Pytest 9.2.0
- **Công cụ kiểm thử:** Selenium WebDriver 4.1.0 (Trình duyệt Chrome)
- **Thời gian thực thi:** 290.98 giây (4 phút 50 giây)

## 2. TỔNG QUAN KẾT QUẢ (EXECUTIVE SUMMARY)
- **Tổng số kịch bản thực thi (Total Test Cases):** 15 kịch bản (Test suite Phân hệ Tra cứu & Điều hướng).
- **Số kịch bản chuẩn (PASSED):** 13 kịch bản.
- **Số kịch bản bắt được lỗi hệ thống (FAILED - Bắt đúng Bug):** 2 kịch bản.
- **Tỷ lệ xử lý thành công của kịch bản:** 100% (Không có kịch bản nào bị crash do lỗi code, toàn bộ lệnh FAILED đều do chủ đích giăng bẫy bắt Bug).

## 3. PHÂN TÍCH CHI TIẾT CÁC LỖI (DEFECTS FOUND)
Quá trình chạy tự động 5 phút không có sự can thiệp của con người đã phát hiện và ghi nhận 2 lỗ hổng logic/bảo mật của hệ thống:

1. **Bug 1 - TC_02 (Lỗi xử lý Ký tự đặc biệt / XSS Payload):**
   - *Hành vi:* Script bắn payload `!@#$%^&*()<script>alert(1)</script>` vào ô tìm kiếm. Kỳ vọng bộ lọc sẽ chặn payload này và không trả về kết quả (gây `TimeoutException`).
   - *Thực tế:* Kịch bản báo `Failed: DID NOT RAISE TimeoutException`. Nghĩa là hệ thống đã không chặn triệt để hoặc không mã hóa tốt, dẫn đến việc giao diện vẫn lọt qua bước kiểm tra bộ lọc. Đây là nguy cơ tiềm ẩn về Injection.

2. **Bug 2 - TC_17 (Lỗi Logic bộ lọc khoảng trắng):**
   - *Hành vi:* Nhập chuỗi chỉ toàn khoảng trắng `"   "` vào thanh tra cứu.
   - *Thực tế:* Bắt được thông báo: `[BẮT ĐƯỢC BUG LOGIC] Nhập '   ' nhưng hệ thống KHÔNG TÌM KIẾM/LỌC mà vẫn hiện văn bản`. Lỗi này làm lãng phí tài nguyên máy chủ khi truy vấn những dữ liệu rỗng.

## 4. BẢNG KẾT QUẢ CHI TIẾT (DETAILED METRICS)

| Mã TC | Tên Kịch bản / Luồng kiểm thử | Thời gian ước tính | Kết quả | Trạng thái kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **TC_01** | Kiểm tra chặn truy cập khi chưa xác thực | ~5s | **PASSED** | Xử lý chặn thành công. |
| **TC_02** | Test bảo mật XSS & Ký tự đặc biệt | ~12s | **FAILED** | Bắt được Bug rò rỉ bộ lọc. |
| **TC_03** | Tìm kiếm từ khóa không tồn tại | ~12s | **PASSED** | Trả về 0 kết quả chuẩn xác. |
| **TC_04** | Tìm kiếm chỉ chứa khoảng trắng (Tại trang chủ) | ~10s | **PASSED** | Giao diện trang chủ xử lý tốt. |
| **TC_05** | Tìm kiếm chuỗi tối đa độ dài (Max Length 255) | ~12s | **PASSED** | Không gây tràn bộ nhớ (Buffer Overflow). |
| **TC_06** | Xung đột từ khóa và danh mục bộ lọc | ~10s | **PASSED** | Bộ lọc chéo hoạt động đúng. |
| **TC_07** | Tìm kiếm không phân biệt Hoa/Thường | ~10s | **PASSED** | Lọc chuẩn xác. |
| **TC_08** | Tìm kiếm bằng một phần từ khóa (Partial Match) | ~10s | **PASSED** | Lọc chuẩn xác. |
| **TC_09** | Xử lý khoảng trắng thừa hai đầu (Trim spaces) | ~10s | **PASSED** | Web tự động Trim thành công. |
| **TC_10** | Luồng thao tác tìm kiếm & mở thẻ hoàn chỉnh | ~15s | **PASSED** | Happy path mượt mà. |
| **TC_11_16** | Kiểm tra tính năng Trình ký (△State Engine) | ~20s | **PASSED** | Hệ thống phản hồi thành công ở lần thử đầu tiên. Bộ lọc khoảng ngày hoạt động tốt. |
| **TC_12** | Quét vét cạn DOM menu Văn bản đi/đến | ~120s | **PASSED** | Trích xuất thành công: **2 mục con VB đi**, **2 mục con VB đến**. Số liệu kết quả hiển thị hoàn toàn nhất quán 100%. |
| **TC_13** | Kiểm tra Lịch thời gian thực / Lịch quá khứ | ~15s | **PASSED** | Đối chiếu thành công ngày hiện tại. |
| **TC_14** | Trạng thái tiến độ & Bộ đếm công việc (Regex) | ~20s | **PASSED** | *(Kèm Cảnh báo hệ thống)*: Trạng thái UI khớp với thống kê tổng. Lấy dữ liệu thành công. |
| **TC_17** | Kiểm tra lỗi Logic Tra cứu với giá trị dị thường | ~10s | **FAILED** | Bắt được Bug Logic khoảng trắng. |

## 5. KẾT LUẬN & ĐÁNH GIÁ (CONCLUSION)
- **Độ bền vững của Script (Robustness):** Kịch bản duy trì kết nối với trình duyệt suốt gần 5 phút, xử lý trơn tru các khoảng trễ tải trang (Network Latency) thông qua `WebDriverWait`. Các bẫy giao diện (Flaky UI) như menu ẩn, menu lồng nhau đã được giải quyết hoàn toàn bằng kỹ thuật quét DOM thông minh (TC_12) và Direct Routing.
- **Tính tự động hóa:** Các ảnh bằng chứng (Evidence) đã được hệ thống tự động chụp tại các khoảnh khắc phát hiện lỗi hoặc xác nhận nghiệp vụ, lưu trữ an toàn vào thư mục `evidence/`. Script đã sẵn sàng đóng gói để làm minh chứng cho báo cáo nghiệm thu NCKH cuối kỳ.