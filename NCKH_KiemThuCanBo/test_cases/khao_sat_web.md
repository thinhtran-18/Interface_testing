# Bảng danh mục chức năng khảo sát phần mềm quản lý cán bộ (Đã chuẩn hóa NCKH)

| Mã chức năng | Tên chức năng | Nội dung chi tiết cần xác minh | Kỹ thuật kiểm thử áp dụng | Khả năng tự động hóa |
| :---: | :--- | :--- | :--- | :---: |
| **WEB-01** | Tra cứu cán bộ | Xác minh kết quả trả về khi tìm kiếm theo từ khóa tên hoặc mã cán bộ trên ô `#searchInput` theo thời gian thực (real-time). | Phân vùng tương đương (EP) & Kiểm thử Hộp đen | **Cao** (Selenium WebDriver) |
| **WEB-02** | Hiển thị danh sách | Kiểm tra tính chính xác của các cột dữ liệu, định dạng bảng và cơ chế hiển thị trạng thái dữ liệu trống (Empty State). | Kiểm thử giao diện & Giá trị biên | **Cao** (Selenium WebDriver) |
| **WEB-03** | Xem chi tiết | Xác minh tính đầy đủ và chính xác của thông tin cá nhân/cán bộ khi chọn (click) vào một bản ghi cụ thể trên lưới dữ liệu. | Kiểm thử chức năng (Functional Testing) | **Cao** (Selenium WebDriver) |
| **WEB-04** | Điều hướng | Kiểm tra sự mượt mà và chính xác của luồng chuyển đổi trạng thái (Routing/Navigation) giữa trang danh sách và trang chi tiết. | Kiểm thử luồng điều hướng (Navigation Testing) | **Cao** (Selenium WebDriver) |
| **WEB-05** | Xử lý dữ liệu đầu vào | Kiểm tra cơ chế kiểm soát dữ liệu hợp lệ (Happy Path) và không hợp lệ (ký tự đặc biệt, XSS, khoảng trắng, chuỗi cực dài). | Phân tích giá trị biên (BVA) & Kiểm thử bảo mật cơ bản | **Cao** (Selenium WebDriver) |
