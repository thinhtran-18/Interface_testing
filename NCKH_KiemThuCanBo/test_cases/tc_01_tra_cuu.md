# Test Case: Kiểm tra chức năng tra cứu và lọc phần mềm

* **Mã Test Case:** TC-WEB-01
* **Mục tiêu:** Xác minh kết quả tìm kiếm và lọc danh mục phần mềm trên giao diện Web hoạt động chính xác.
* **Tiền điều kiện:**
  - Đã đăng nhập vào hệ thống quản trị (`main.hau.edu.vn`).
  - Đang ở màn hình danh mục phần mềm có tích hợp ô tìm kiếm và bộ lọc.
* **Các bước thực hiện:**
  1. Truy cập vào màn hình chính cổng quản trị.
  2. Nhập từ khóa cần tìm vào ô tìm kiếm (`#searchInput`).
  3. Nhấn phím Enter hoặc nút tìm kiếm.
  4. Quan sát kết quả hiển thị trên bảng danh sách kết quả.
* **Kết quả mong đợi:** Hệ thống lọc và hiển thị chính xác các thẻ phần mềm khớp với từ khóa tìm kiếm.
* **Trạng thái:** Đạt (Passed) / Đã thực thi tự động qua Selenium.

# Test Case: Kiểm tra chức năng lọc danh mục nhóm chức năng

* **Mã Test Case:** TC-WEB-02
* **Mục tiêu:** Xác minh chức năng lọc danh sách ứng dụng theo nhóm Hành chính hoạt động chính xác.
* **Tiền điều kiện:**
  - Đang ở màn hình danh mục phần mềm.
* **Các bước thực hiện:**
  1. Quan sát thanh bộ lọc nhóm chức năng (`#filterTabs`).
  2. Nhấn chọn nút bộ lọc **Hành chính** (`button:nth-child(3)`).
  3. Quan sát danh sách ứng dụng thay đổi trên giao diện.
* **Kết quả mong đợi:** Giao diện thu gọn và chỉ hiển thị các ứng dụng thuộc nhóm Hành chính.
* **Trạng thái:** Đạt (Passed) / Đã thực thi tự động qua Selenium.

# Test Case: Kiểm tra thao tác mở thẻ chi tiết và điều hướng phần mềm

* **Mã Test Case:** TC-WEB-03
* **Mục tiêu:** Xác minh thao tác tương tác click trực tiếp vào thẻ phần mềm giúp điều hướng chính xác sang giao diện/tab chức năng chi tiết của ứng dụng.
* **Tiền điều kiện:** 
  - Đã thực hiện thành công tìm kiếm (`WEB-01`) và lọc nhóm (`WEB-02`) trên cổng quản trị `main.hau.edu.vn`.
  - Thẻ phần mềm cần mở (ví dụ: *"Văn bản điều hành"*) đang hiển thị trên màn hình.
* **Các bước thực hiện:**
  1. Chờ phần tử thẻ chứa văn bản `"Văn bản điều hành"` sẵn sàng tương tác (`element_to_be_clickable`) bằng XPath.
  2. Thực hiện hành động click vào thẻ phần mềm đó.
  3. Quan sát sự thay đổi trên giao diện và URL của trình duyệt.
* **Kết quả mong đợi:** Trình duyệt điều hướng thành công sang giao diện làm việc hoặc tab chức năng chi tiết của phần mềm "Văn bản điều hành", không xảy ra lỗi xung đột tải trang (Timeout).
* **Trạng thái:** Đạt (Passed) / Đã thực thi tự động qua Selenium WebDriver.


# Test Case: Kiểm tra tính năng quay lại danh mục từ trang chi tiết

* **Mục tiêu:** Xác minh luồng điều hướng quay trở lại màn hình danh mục chính hoạt động mượt mà, giữ nguyên trạng thái hoặc bộ lọc trước đó.
* **Tiền điều kiện:** 
  - Đã thực hiện mở thành công một thẻ phần mềm cụ thể (ví dụ: màn hình chi tiết của "Văn bản điều hành" thông qua TC-WEB-03).
* **Các bước thực hiện:**
  1. Từ trang chi tiết phần mềm, tìm và nhấn nút **Quay lại** (Back) trên trình duyệt hoặc nút điều hướng trở về danh mục trên giao diện ứng dụng.
  2. Quan sát màn hình hiển thị sau khi điều hướng.
* **Kết quả mong đợi:** Trình duyệt điều hướng thành công trở lại màn hình chính của cổng danh mục phần mềm, hiển thị ổn định, không bị lỗi mất phiên làm việc.
* **Trạng thái:** Đạt (Passed) / Đã xác thực trên hệ thống.