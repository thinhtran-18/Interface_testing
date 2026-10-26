# BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI NCKH SINH VIÊN (TUẦN 1 & TUẦN 2)

**Trường Đại học Kiến trúc Hà Nội**  
**Đề tài**: Nghiên cứu phương pháp kiểm thử giao diện người dùng áp dụng cho phần mềm quản lý cán bộ của Trường Đại học Kiến trúc Hà Nội  
**Họ và tên sinh viên thực hiện**: **Nguyễn Quang Huy**  
**Vai trò**: Lập trình viên chính (Code chính) – Phụ trách nhóm Biểu mẫu (Form Testing) & Xác thực Dữ liệu đầu vào  
**Nhóm trưởng**: Trần Văn Thịnh  
**Các thành viên trong nhóm**: Chu Bách Trúc Mai, Nguyễn Thị Cẩm Vân, Nguyễn Ngọc Thuỳ Trang  
**Thời gian báo cáo**: Tuần 1 & Tuần 2  

---

## 1. BÁO CÁO TUẦN 1: KHẢO SÁT VÀ KHÓA THIẾT KẾ

### 1.1. Mục tiêu
Khảo sát luồng giao diện Web thực tế, phân tích cấu trúc biểu mẫu xác thực người dùng tập trung (SSO) và chuẩn bị nền tảng kỹ thuật kiểm thử tự động.

### 1.2. Các công việc đã thực hiện
1. **Khảo sát hệ thống xác thực tập trung SSO HAU**:
   - Truy cập và khảo sát cơ chế điều hướng tự động giữa Cổng quản trị chung `https://main.hau.edu.vn/` và Cổng xác thực tập trung `https://sso.hau.edu.vn/Account/Login`.
   - Nhận diện kiến trúc OAuth2 / OpenID Connect: URL xác thực có gắn mã `code_challenge` và `state` dùng một lần. Nhận diện nguy cơ treo kiểm thử nếu tái sử dụng URL tĩnh có tham số phiên đã hết hạn.
2. **Khảo sát cấu trúc DOM và bộ chọn phần tử (Selectors)**:
   - Sử dụng Chrome DevTools bóc tách chi tiết các thẻ HTML trên trang đăng nhập:
     - Ô nhập tên đăng nhập: `id="Username"`, thuộc tính `placeholder="Nhập tên đăng nhập"`.
     - Ô nhập mật khẩu: `id="Password"`, thuộc tính `type="password"`.
     - Checkbox duy trì phiên: `id="RememberLogin"`.
     - Icon con mắt bật/tắt mật khẩu: `a.toggle-password`.
     - Nút gửi biểu mẫu: `button.btn-login` (nhãn *"Đăng nhập"*).
     - Khung thông báo lỗi xác thực: `.alert.alert-danger` chứa danh sách lỗi `ul > li`.
3. **Phân loại dữ liệu đầu vào và thiết kế kịch bản kiểm thử (Test Case Design)**:
   - Áp dụng kỹ thuật phân lớp tương đương (Equivalence Partitioning) và phân tích giá trị biên (Boundary Value Analysis):
     - *Dữ liệu hợp lệ*: Tài khoản định danh cán bộ được cấp (`035187013852` / `123@123`).
     - *Dữ liệu biên*: Để trống cả 2 trường, để trống tài khoản có nhập mật khẩu, để trống mật khẩu có nhập tài khoản.
     - *Dữ liệu tiêu cực*: Tài khoản hoặc mật khẩu sai.
4. **Phối hợp công việc trong nhóm**:
   - Thống nhất cấu trúc kho mã Selenium/Pytest theo mô hình Page Object Model (POM) do Trưởng nhóm Trần Văn Thịnh khởi tạo.
   - Bàn giao danh mục luồng biểu mẫu cho Nguyễn Thị Cẩm Vân để lập ma trận ca kiểm thử chung.

### 1.3. Sản phẩm bàn giao Tuần 1
- Sơ đồ luồng đăng nhập và điều hướng xác thực Web.
- Danh mục 8 ca kiểm thử biểu mẫu dự kiến (`WEB-FORM-01` đến `WEB-FORM-08`).

---

## 2. BÁO CÁO TUẦN 2: VIẾT CODE, KIỂM THỬ VÀ GHI NHẬN KẾT QUẢ

### 2.1. Mục tiêu
Chuyển đổi thiết kế thành mã nguồn kiểm thử tự động Selenium/Pytest, hoàn thiện Page Object cho biểu mẫu, thực thi kiểm thử vòng một và thu thập hình ảnh minh chứng.

### 2.2. Các công việc đã thực hiện
1. **Xây dựng Page Object `LoginPage` (`pages/login_page.py`)**:
   - Đóng gói toàn bộ thao tác biểu mẫu vào lớp đối tượng: `enter_username()`, `enter_password()`, `click_login()`, `login()`.
   - Xây dựng các hàm tương tác giao diện chuyên biệt: `toggle_password_visibility()` (kiểm tra chuyển đổi kiểu mật khẩu), `toggle_remember()` (kiểm tra trạng thái checkbox), `get_error_message()` (bắt nội dung thông báo lỗi từ `.alert-danger`).
   - Tích hợp cơ chế chờ tường minh `WebDriverWait` và `EC.visibility_of_element_located` để đảm bảo tương tác ổn định, chống lỗi tải trang.
2. **Xây dựng Page Object `DashboardPage` (`pages/dashboard_page.py`)**:
   - Hỗ trợ kiểm tra trạng thái điều hướng sau đăng nhập thành công vào Cổng quản trị `main.hau.edu.vn`.
   - Trích xuất mã cán bộ hiển thị trên thanh tiêu đề `(035187013852)`.
3. **Lập trình bộ kịch bản kiểm thử tự động (`tests/web/test_login.py`)**:
   - Hiện thực hóa đầy đủ 8 kịch bản kiểm thử tự động theo tiêu chuẩn Pytest:

| Mã test case | Tên kịch bản kiểm thử | Loại kiểm thử | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **WEB-FORM-01** | Kiểm tra hiển thị & thuộc tính phần tử biểu mẫu | Giao diện / DOM | Truy cập cổng SSO HAU | Ô input hiển thị đúng placeholder, type="password", nút bấm hiển thị "Đăng nhập" | **PASSED** |
| **WEB-FORM-02** | Kiểm tra nút toggle ẩn/hiện mật khẩu (Con mắt) | Tương tác UI | Nhập mật khẩu, click icon con mắt | Thuộc tính `type` chuyển đổi linh hoạt giữa `"password"` và `"text"` | **PASSED** |
| **WEB-FORM-03** | Kiểm tra checkbox "Nhớ thông tin đăng nhập" | Tương tác UI | Click checkbox RememberLogin | Trạng thái `is_selected()` thay đổi chính xác khi click | **PASSED** |
| **WEB-FORM-04** | Kiểm tra validation khi gửi biểu mẫu rỗng (Biên) | Kiểm thử biên | Bỏ trống User & Pass, Submit | Hiển thị cảnh báo màu đỏ: *"Vui lòng nhập tên đăng nhập"* và *"Vui lòng nhập mật khẩu"* | **PASSED** |
| **WEB-FORM-05** | Kiểm tra validation khi bỏ trống mật khẩu | Kiểm thử biên | User = `"035187013852"`, Pass = `""` | Hiển thị thông báo: *"Vui lòng nhập mật khẩu"*; không báo lỗi tài khoản | **PASSED** |
| **WEB-FORM-06** | Kiểm tra validation khi bỏ trống tên đăng nhập | Kiểm thử biên | User = `""`, Pass = `"123@123"` | Hiển thị thông báo: *"Vui lòng nhập tên đăng nhập"*; không báo lỗi mật khẩu | **PASSED** |
| **WEB-FORM-07** | Kiểm tra thông báo khi nhập sai thông tin xác thực | Bảo mật / Tiêu cực | User = `"tai_khoan_gia_dinh_9999"`, Pass = `"mat_khau_sai_123"` | Hiển thị cảnh báo: *"Tên đăng nhập hoặc mật khẩu không đúng."* | **PASSED** |
| **WEB-FORM-08** | Kiểm tra đăng nhập thành công với tài khoản hợp lệ | Chức năng / Tích hợp | User & Password hợp lệ từ `.env` | Hệ thống xác thực thành công, điều hướng về Cổng chính `main.hau.edu.vn`, header hiển thị đúng mã tài khoản | **PASSED** |

4. **Thực thi kiểm thử tự động vòng một**:
   - Thực thi riêng bộ test biểu mẫu: **8/8 ca kiểm thử PASSED (100%)** trong thời gian 17.16s.
   - Thực thi kết hợp toàn diện cùng bộ khung của Trần Văn Thịnh: **14/14 ca kiểm thử PASSED (100%)** trong 59.13s.
5. **Thu thập ảnh chụp minh chứng thực tế (Evidence)**:
   - Đã chụp và lưu trữ ảnh màn hình kiểm thử vào thư mục `evidence/web/`:
     - `WEB_FORM_04_empty_credentials.png`: Minh chứng thông báo lỗi form rỗng.
     - `WEB_FORM_07_invalid_credentials.png`: Minh chứng cảnh báo nhập sai tài khoản.
     - `post_login.png`: Minh chứng giao diện sau đăng nhập thành công.
     - `search_nhan_su.png`: Minh chứng tìm kiếm phân hệ Quản lý nhân sự.
     - `user_dropdown.png`: Minh chứng menu tài khoản người dùng.

### 2.3. Sản phẩm bàn giao Tuần 2
- Bộ script kiểm thử tự động nhóm Biểu mẫu: `tests/web/test_login.py`.
- Lớp Page Object điều khiển form: `pages/login_page.py`.
- Tập dữ liệu ảnh minh chứng: `evidence/web/`.
- Sẵn sàng bàn giao mã nguồn cho Chu Bách Trúc Mai để tiến hành review chéo trong Tuần 3 (theo đúng kế hoạch tại trang 15 của đề cương).

---

## 3. PHÂN TÍCH KỸ THUẬT VÀ PHÁT HIỆN
1. **Kiến trúc xác thực SSO & OAuth2 Authorization Code Flow**:
   - Cổng thông tin `main.hau.edu.vn` chuyển tiếp sang SSO với tham số dùng một lần (PKCE). Bộ kiểm thử đã cấu hình truy cập từ URL gốc để mỗi lần thực thi đều được cấp phát phiên hợp lệ, triệt tiêu lỗi token hết hạn.
2. **Cơ chế Validation của biểu mẫu**:
   - Biểu mẫu áp dụng validation cả client-side lẫn server-side.
   - Khung thông báo lỗi hiển thị trong `.alert-danger`. Mã kiểm thử đã bắt chính xác các câu thông báo tiếng Việt theo đúng ngữ cảnh thao tác.
3. **Tình trạng phân quyền tài khoản thử nghiệm**:
   - Tài khoản `035187013852` đăng nhập thành công nhưng chỉ được phân quyền vào phân hệ *"Văn bản điều hành"*. Module trọng tâm của đề tài (*"Quản lý nhân sự"*) đang bị khóa (`app-disabled`).
   - Đã báo cáo Nhóm trưởng Trần Văn Thịnh để đưa vào biên bản làm việc xin cấp tài khoản có thẩm quyền Quản trị nhân sự trong các giai đoạn sau.

---

## 4. KẾ HOẠCH CHO TUẦN 3
- Phối hợp với Chu Bách Trúc Mai thực hiện review chéo bộ mã kiểm thử (Huy review script tra cứu của Mai, Mai review script biểu mẫu của Huy).
- Chạy lặp kiểm thử đo độ ổn định script (Loop Rate, Execution Stability) trên nhiều khung giờ.
- Chuẩn bị mở rộng kiểm thử các biểu mẫu nghiệp vụ quản lý hồ sơ cán bộ khi được cấp quyền.

---

**XÁC NHẬN CỦA NHÓM TRƯỞNG**  
*(Ký và ghi rõ họ tên)*  
**Trần Văn Thịnh**  

**NGƯỜI LÀM BÁO CÁO**  
*(Ký và ghi rõ họ tên)*  
**Nguyễn Quang Huy**  
