"""Script tạo báo cáo Tuần 1 & Tuần 2 cho Nguyễn Quang Huy.
Xuất ra cả 2 định dạng:
1. Markdown: reports/bao_cao_tuan_1_2_nguyen_quang_huy.md
2. Microsoft Word (.docx): reports/bao_cao_tuan_1_2_nguyen_quang_huy.docx
Không phụ thuộc vào thư viện ngoài, tạo file Word chuẩn OOXML mở được trên mọi phiên bản Word.
"""

import os
import sys
import zipfile
import html

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_markdown(filepath):
    md_content = """# BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI NCKH SINH VIÊN (TUẦN 1 & TUẦN 2)

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
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Đã tạo file Markdown: {filepath}")


def create_docx(filepath):
    # Tạo cấu trúc file OOXML Word chuẩn
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="26"/>
        <w:szCs w:val="26"/>
        <w:lang w:val="vi-VN"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:line="276" w:lineRule="auto" w:after="120"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

    # Helper XML builders
    def p(text="", bold=False, italic=False, size=26, color="000000", align="both", space_before=0, space_after=120):
        jc = f'<w:jc w:val="{align}"/>' if align else ''
        spacing = f'<w:spacing w:before="{space_before}" w:after="{space_after}"/>'
        rPr = '<w:rPr>'
        if bold: rPr += '<w:b/><w:bCs/>'
        if italic: rPr += '<w:i/><w:iCs/>'
        if size: rPr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        if color: rPr += f'<w:color w:val="{color}"/>'
        rPr += '</w:rPr>'
        
        escaped_text = html.escape(text)
        return f'<w:p><w:pPr>{jc}{spacing}</w:pPr><w:r>{rPr}<w:t xml:space="preserve">{escaped_text}</w:t></w:r></w:p>'

    def p_runs(runs, align="both", space_before=0, space_after=120):
        jc = f'<w:jc w:val="{align}"/>' if align else ''
        spacing = f'<w:spacing w:before="{space_before}" w:after="{space_after}"/>'
        body = f'<w:p><w:pPr>{jc}{spacing}</w:pPr>'
        for r in runs:
            text = html.escape(r.get("text", ""))
            rPr = '<w:rPr>'
            if r.get("bold"): rPr += '<w:b/><w:bCs/>'
            if r.get("italic"): rPr += '<w:i/><w:iCs/>'
            size = r.get("size", 26)
            rPr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
            if r.get("color"): rPr += f'<w:color w:val="{r["color"]}"/>'
            if r.get("font"): rPr += f'<w:rFonts w:ascii="{r["font"]}" w:hAnsi="{r["font"]}"/>'
            rPr += '</w:rPr>'
            body += f'<w:r>{rPr}<w:t xml:space="preserve">{text}</w:t></w:r>'
        body += '</w:p>'
        return body

    def heading1(text):
        return p(text, bold=True, size=30, color="1F4E79", space_before=240, space_after=100)

    def heading2(text):
        return p(text, bold=True, size=26, color="203864", space_before=180, space_after=80)

    def bullet(text, bold_prefix=""):
        runs = []
        if bold_prefix:
            runs.append({"text": "• " + bold_prefix + ": ", "bold": True, "size": 26, "color": "111111"})
            runs.append({"text": text, "bold": False, "size": 26, "color": "111111"})
        else:
            runs.append({"text": "• " + text, "bold": False, "size": 26, "color": "111111"})
        return p_runs(runs, align="both", space_before=0, space_after=60)

    def code_box(code_text):
        lines = code_text.strip().split("\n")
        res = '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders><w:top w:val="single" w:sz="6" w:color="CCCCCC"/><w:left w:val="single" w:sz="6" w:color="1F4E79"/><w:bottom w:val="single" w:sz="6" w:color="CCCCCC"/><w:right w:val="single" w:sz="6" w:color="CCCCCC"/></w:tblBorders><w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:left w:w="180" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:right w:w="180" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tr><w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="F5F6F8"/></w:tcPr>'
        for line in lines:
            escaped = html.escape(line)
            res += f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:color w:val="2A2A2A"/></w:rPr><w:t xml:space="preserve">{escaped}</w:t></w:r></w:p>'
        res += '</w:tc></w:tr></w:tbl>'
        return res

    def build_table(headers, rows):
        tbl = '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>'
        tbl += '<w:top w:val="single" w:sz="8" w:space="0" w:color="7F7F7F"/>'
        tbl += '<w:left w:val="single" w:sz="8" w:space="0" w:color="7F7F7F"/>'
        tbl += '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="7F7F7F"/>'
        tbl += '<w:right w:val="single" w:sz="8" w:space="0" w:color="7F7F7F"/>'
        tbl += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D0D0"/>'
        tbl += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="D0D0D0"/>'
        tbl += '</w:tblBorders><w:tblCellMar><w:top w:w="100" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        
        # Header row
        tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
        for h in headers:
            tbl += f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/></w:tcPr><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="40" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/><w:sz w:val="23"/><w:szCs w:val="23"/><w:color w:val="FFFFFF"/></w:rPr><w:t>{html.escape(h)}</w:t></w:r></w:p></w:tc>'
        tbl += '</w:tr>'

        # Data rows
        for row in rows:
            tbl += '<w:tr>'
            for idx, cell in enumerate(row):
                align = "center" if idx in [0, 2, 5] else "both"
                color = "008000" if cell == "PASSED" else "111111"
                bold = (cell == "PASSED") or (idx == 0)
                tbl += f'<w:tc><w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:before="30" w:after="30"/></w:pPr><w:r><w:rPr>'
                if bold: tbl += '<w:b/><w:bCs/>'
                tbl += f'<w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="{color}"/></w:rPr><w:t>{html.escape(cell)}</w:t></w:r></w:p></w:tc>'
            tbl += '</w:tr>'
        tbl += '</w:tbl>'
        return tbl

    # Assemble Document XML Body
    body = ""

    # Header trường
    body += p("BỘ GIÁO DỤC VÀ ĐÀO TẠO - TRƯỜNG ĐẠI HỌC KIẾN TRÚC HÀ NỘI", bold=True, size=24, align="center", space_after=40)
    body += p("ĐỀ TÀI NGHIÊN CỨU KHOA HỌC SINH VIÊN NĂM 2026", italic=True, size=22, align="center", space_after=200)

    # Tiêu đề báo cáo
    body += p("BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI NCKH", bold=True, size=34, color="1F4E79", align="center", space_before=100, space_after=40)
    body += p("GIAI ĐOẠN: TUẦN 1 & TUẦN 2", bold=True, size=28, color="203864", align="center", space_after=200)

    # Khung thông tin
    info_runs = [
        {"text": "Đề tài: ", "bold": True},
        {"text": "Nghiên cứu phương pháp kiểm thử giao diện người dùng áp dụng cho phần mềm quản lý cán bộ của Trường Đại học Kiến trúc Hà Nội\n"},
        {"text": "Họ và tên sinh viên thực hiện: ", "bold": True},
        {"text": "Nguyễn Quang Huy\n", "bold": True, "color": "1F4E79"},
        {"text": "Vai trò trong nhóm: ", "bold": True},
        {"text": "Lập trình viên chính (Code chính) – Phụ trách Kiểm thử nhóm Biểu mẫu (Form Testing) & Xác thực Dữ liệu đầu vào\n"},
        {"text": "Nhóm trưởng: ", "bold": True},
        {"text": "Trần Văn Thịnh | "},
        {"text": "Thành viên nhóm: ", "bold": True},
        {"text": "Chu Bách Trúc Mai, Nguyễn Thị Cẩm Vân, Nguyễn Ngọc Thuỳ Trang\n"},
        {"text": "Thời gian báo cáo: ", "bold": True},
        {"text": "Từ Tuần 1 đến hết Tuần 2"}
    ]
    # Bọc info box
    body += '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders><w:top w:val="single" w:sz="6" w:color="B8CCE4"/><w:left w:val="single" w:sz="24" w:color="1F4E79"/><w:bottom w:val="single" w:sz="6" w:color="B8CCE4"/><w:right w:val="single" w:sz="6" w:color="B8CCE4"/></w:tblBorders><w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tr><w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="F2F5F9"/></w:tcPr>'
    body += p_runs(info_runs, align="both", space_after=40)
    body += '</w:tc></w:tr></w:tbl>'

    # 1. BÁO CÁO TUẦN 1
    body += heading1("1. BÁO CÁO TUẦN 1: KHẢO SÁT VÀ KHÓA THIẾT KẾ")
    body += heading2("1.1. Mục tiêu")
    body += p("Khảo sát luồng giao diện Web thực tế, phân tích cấu trúc biểu mẫu xác thực người dùng tập trung (SSO) và chuẩn bị nền tảng kỹ thuật kiểm thử tự động theo đề cương phân công.")
    
    body += heading2("1.2. Các công việc đã thực hiện")
    body += bullet("Truy cập và khảo sát cơ chế điều hướng tự động giữa Cổng quản trị chung (main.hau.edu.vn) và Cổng xác thực SSO (sso.hau.edu.vn). Nhận diện kiến trúc OAuth2 / OpenID Connect sử dụng mã xác thực một lần (code_challenge & state), ghi nhận giải pháp khởi động phiên test từ URL gốc để tránh token hết hạn.", "Khảo sát hệ thống SSO HAU")
    body += bullet("Sử dụng Chrome DevTools khảo sát chính xác bộ chọn phần tử (Selectors): ô tài khoản #Username (placeholder: 'Nhập tên đăng nhập'), ô mật khẩu #Password (type='password'), checkbox #RememberLogin, nút con mắt a.toggle-password, nút bấm submit button.btn-login và khung cảnh báo lỗi .alert-danger.", "Bóc tách cấu trúc DOM biểu mẫu")
    body += bullet("Áp dụng kỹ thuật phân lớp tương đương và phân tích giá trị biên: xác định tập dữ liệu hợp lệ (tài khoản cán bộ 035187013852 / 123@123), tập dữ liệu biên (bỏ trống cả hai trường, chỉ nhập user, chỉ nhập pass) và tập dữ liệu không hợp lệ (sai tài khoản hoặc mật khẩu).", "Phân loại dữ liệu đầu vào & Thiết kế ca kiểm thử")
    body += bullet("Thống nhất cấu trúc kho mã Selenium/Pytest theo mô hình Page Object Model (POM) do Nhóm trưởng Trần Văn Thịnh khởi tạo; bàn giao danh mục luồng biểu mẫu cho Nguyễn Thị Cẩm Vân lập ma trận test case.", "Phối hợp công việc nhóm")

    body += heading2("1.3. Sản phẩm bàn giao Tuần 1")
    body += bullet("Sơ đồ luồng đăng nhập và điều hướng xác thực Web.")
    body += bullet("Danh mục 8 ca kiểm thử biểu mẫu dự kiến (mã WEB-FORM-01 đến WEB-FORM-08) có đầy đủ tiền điều kiện, dữ liệu thử và kết quả kỳ vọng.")

    # 2. BÁO CÁO TUẦN 2
    body += heading1("2. BÁO CÁO TUẦN 2: VIẾT CODE, KIỂM THỬ VÀ GHI NHẬN KẾT QUẢ")
    body += heading2("2.1. Mục tiêu")
    body += p("Chuyển đổi thiết kế thành mã nguồn kiểm thử tự động Selenium/Pytest, hoàn thiện Page Object cho biểu mẫu, thực thi kiểm thử vòng một và thu thập hình ảnh minh chứng.")

    body += heading2("2.2. Các công việc đã thực hiện")
    body += bullet("Đóng gói toàn bộ thao tác form vào lớp LoginPage (pages/login_page.py): nhập tài khoản, nhập mật khẩu, click đăng nhập, toggle con mắt hiển thị/ẩn mật khẩu, toggle checkbox ghi nhớ và hàm trích xuất câu thông báo lỗi từ .alert-danger. Tích hợp cơ chế chờ tường minh WebDriverWait chống lỗi tải trang.", "Xây dựng Page Object LoginPage")
    body += bullet("Hỗ trợ kiểm tra điều hướng sau đăng nhập thành công vào Cổng quản trị main.hau.edu.vn và trích xuất mã tài khoản hiển thị trên header.", "Xây dựng Page Object DashboardPage")
    body += bullet("Hiện thực hóa đầy đủ 8 kịch bản kiểm thử tự động trong file tests/web/test_login.py.", "Lập trình bộ kiểm thử tự động Biểu mẫu")

    # Bảng Test Cases
    body += heading2("2.3. Bảng ma trận kịch bản kiểm thử đã thực hiện (Test Matrix)")
    headers = ["Mã test", "Tên kịch bản kiểm thử", "Loại kiểm thử", "Dữ liệu đầu vào", "Kết quả kỳ vọng", "Trạng thái"]
    rows = [
        ["WEB-FORM-01", "Kiểm tra hiển thị & thuộc tính phần tử biểu mẫu", "Giao diện/DOM", "Truy cập cổng SSO HAU", "Input hiển thị đúng placeholder, type='password', nút Đăng nhập", "PASSED"],
        ["WEB-FORM-02", "Kiểm tra nút con mắt ẩn/hiện mật khẩu", "Tương tác UI", "Nhập pass, click toggle", "Thuộc tính type chuyển đổi chính xác 'password' <-> 'text'", "PASSED"],
        ["WEB-FORM-03", "Kiểm tra checkbox 'Nhớ thông tin đăng nhập'", "Tương tác UI", "Click checkbox Remember", "Trạng thái is_selected() chuyển đổi linh hoạt khi click", "PASSED"],
        ["WEB-FORM-04", "Kiểm tra validation khi gửi biểu mẫu rỗng (Biên)", "Kiểm thử biên", "User = '', Pass = ''", "Cảnh báo đỏ: 'Vui lòng nhập tên đăng nhập' và 'Vui lòng nhập mật khẩu'", "PASSED"],
        ["WEB-FORM-05", "Kiểm tra validation khi bỏ trống mật khẩu", "Kiểm thử biên", "User = '035187013852', Pass = ''", "Cảnh báo đỏ: 'Vui lòng nhập mật khẩu'; không báo lỗi tài khoản", "PASSED"],
        ["WEB-FORM-06", "Kiểm tra validation khi bỏ trống tên đăng nhập", "Kiểm thử biên", "User = '', Pass = '123@123'", "Cảnh báo đỏ: 'Vui lòng nhập tên đăng nhập'; không báo lỗi mật khẩu", "PASSED"],
        ["WEB-FORM-07", "Kiểm tra thông báo khi nhập sai tài khoản/pass", "Bảo mật/Tiêu cực", "User sai, Pass sai", "Cảnh báo: 'Tên đăng nhập hoặc mật khẩu không đúng.'", "PASSED"],
        ["WEB-FORM-08", "Kiểm tra đăng nhập thành công với tài khoản hợp lệ", "Chức năng/Tích hợp", "Tài khoản chuẩn trong .env", "Hệ thống xác thực thành công, điều hướng về cổng chính, header hiển thị usercode", "PASSED"]
    ]
    body += build_table(headers, rows)

    body += heading2("2.4. Kết quả thực thi kiểm thử tự động (Execution Logs)")
    body += p("Kết quả thực thi nhóm Biểu mẫu của Nguyễn Quang Huy (test_login.py) đạt 8/8 PASSED:", bold=True)
    body += code_box("""============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.1.1
rootdir: D:\\nckh2026\\Interface_testing
configfile: pytest.ini
collected 8 items

tests/web/test_login.py::test_WEB_FORM_01_elements_display_and_attributes PASSED [ 12%]
tests/web/test_login.py::test_WEB_FORM_02_password_visibility_toggle PASSED   [ 25%]
tests/web/test_login.py::test_WEB_FORM_03_remember_login_checkbox_toggle PASSED [ 37%]
tests/web/test_login.py::test_WEB_FORM_04_empty_credentials_validation PASSED   [ 50%]
tests/web/test_login.py::test_WEB_FORM_05_empty_password_validation PASSED     [ 62%]
tests/web/test_login.py::test_WEB_FORM_06_empty_username_validation PASSED     [ 75%]
tests/web/test_login.py::test_WEB_FORM_07_invalid_credentials_error_message PASSED [ 87%]
tests/web/test_login.py::test_WEB_FORM_08_successful_login_with_valid_credentials PASSED [100%]

============================= 8 passed in 17.16s ==============================""")

    body += p("Kết quả thực thi toàn diện kết hợp cả nhóm đạt 14/14 PASSED (100%):", bold=True, space_before=120)
    body += code_box("""tests/web/test_dashboard.py::test_dashboard_header_and_account PASSED          [  7%]
tests/web/test_dashboard.py::test_filter_tabs_presence PASSED                  [ 14%]
tests/web/test_dashboard.py::test_search_filters_modules PASSED                [ 21%]
tests/web/test_dashboard.py::test_quan_ly_nhan_su_module_is_listed PASSED       [ 28%]
tests/web/test_dashboard.py::test_quan_ly_nhan_su_module_permission_status PASSED [ 35%]
tests/web/test_login.py::test_WEB_FORM_01_elements_display_and_attributes PASSED [ 42%]
tests/web/test_login.py::test_WEB_FORM_02_password_visibility_toggle PASSED   [ 50%]
tests/web/test_login.py::test_WEB_FORM_03_remember_login_checkbox_toggle PASSED [ 57%]
tests/web/test_login.py::test_WEB_FORM_04_empty_credentials_validation PASSED   [ 64%]
tests/web/test_login.py::test_WEB_FORM_05_empty_password_validation PASSED     [ 71%]
tests/web/test_login.py::test_WEB_FORM_06_empty_username_validation PASSED     [ 78%]
tests/web/test_login.py::test_WEB_FORM_07_invalid_credentials_error_message PASSED [ 85%]
tests/web/test_login.py::test_WEB_FORM_08_successful_login_with_valid_credentials PASSED [ 92%]
tests/web/test_smoke.py::test_authorized_application_opens PASSED              [100%]
============================= 14 passed in 59.13s ==============================""")

    body += heading2("2.5. Minh chứng kiểm thử thực tế (Evidence)")
    body += p("Toàn bộ hình ảnh kiểm thử tự động đã được lưu trữ tại thư mục evidence/web/ gồm:")
    body += bullet("evidence/web/post_login.png : Ảnh chụp Cổng quản trị sau đăng nhập thành công với mã định danh (035187013852).")
    body += bullet("evidence/web/WEB_FORM_04_empty_credentials.png : Ảnh chụp cảnh báo đỏ khi gửi biểu mẫu rỗng.")
    body += bullet("evidence/web/WEB_FORM_07_invalid_credentials.png : Ảnh chụp thông báo lỗi khi nhập sai mật khẩu.")
    body += bullet("evidence/web/search_nhan_su.png : Ảnh lọc tìm kiếm module Quản lý nhân sự.")
    body += bullet("evidence/web/user_dropdown.png : Ảnh menu tài khoản người dùng góc phải trên.")

    body += heading2("2.6. Sản phẩm bàn giao Tuần 2")
    body += bullet("Bộ script kiểm thử tự động: tests/web/test_login.py.")
    body += bullet("Page Object điều khiển biểu mẫu: pages/login_page.py.")
    body += bullet("Kho ảnh minh chứng thực tế: evidence/web/.")
    body += bullet("Sẵn sàng bàn giao cho Chu Bách Trúc Mai tiến hành review chéo script trong Tuần 3 (theo đúng kế hoạch ghi chú tại Trang 15 đề cương).")

    # 3. PHÂN TÍCH KỸ THUẬT
    body += heading1("3. PHÂN TÍCH KỸ THUẬT VÀ PHÁT HIỆN")
    body += bullet("Cổng main.hau.edu.vn chuyển tiếp sang SSO với tham số dùng một lần (PKCE). Kịch bản tự động đã xử lý luồng bắt đầu từ trang chủ để trình duyệt tự động cấp phát URL xác thực mới mỗi lần chạy mà không bị lỗi token hết hạn.", "Kiến trúc SSO & OAuth2 Authorization")
    body += bullet("Biểu mẫu áp dụng validation cả client-side lẫn server-side. Khung thông báo lỗi hiển thị trong .alert-danger. Mã kiểm thử đã bắt chính xác các câu thông báo tiếng Việt theo đúng ngữ cảnh thao tác.", "Cơ chế hiển thị Validation")
    body += bullet("Tài khoản thực nghiệm 035187013852 đăng nhập thành công nhưng chỉ được phân quyền vào phân hệ Văn bản điều hành. Module trọng tâm của đề tài (Quản lý nhân sự) đang bị khóa (class app-card app-disabled). Đã báo cáo Nhóm trưởng Trần Văn Thịnh để đưa vào biên bản làm việc xin cấp tài khoản có thẩm quyền Quản trị nhân sự trong các giai đoạn sau.", "Tình trạng phân quyền tài khoản thử nghiệm")

    # 4. KẾ HOẠCH TUẦN 3
    body += heading1("4. KẾ HOẠCH CHO TUẦN 3")
    body += bullet("Phối hợp với Chu Bách Trúc Mai thực hiện review chéo bộ mã kiểm thử (Huy review script tra cứu của Mai, Mai review script biểu mẫu của Huy).")
    body += bullet("Chạy lặp kiểm thử đo độ ổn định script (Loop Rate, Execution Stability) trên nhiều khung giờ khác nhau.")
    body += bullet("Chuẩn bị mở rộng kiểm thử các biểu mẫu nghiệp vụ quản lý hồ sơ cán bộ khi được cấp quyền.")

    # Phần chữ ký xác nhận
    body += p("", space_before=200)
    sign_table = '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders></w:tblPr>'
    sign_table += '<w:tr>'
    sign_table += '<w:tc><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/></w:rPr><w:t>XÁC NHẬN CỦA NHÓM TRƯỞNG</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="600" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1F4E79"/></w:rPr><w:t>Trần Văn Thịnh</w:t></w:r></w:p></w:tc>'
    sign_table += '<w:tc><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="23"/></w:rPr><w:t>Hà Nội, ngày 26 tháng 10 năm 2026</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/></w:rPr><w:t>NGƯỜI LÀM BÁO CÁO</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="500" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1F4E79"/></w:rPr><w:t>Nguyễn Quang Huy</w:t></w:r></w:p></w:tc>'
    sign_table += '</w:tr></w:tbl>'
    body += sign_table

    doc_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles_xml)
        z.writestr("word/document.xml", doc_xml.encode("utf-8"))

    print(f"Đã tạo file Word chuẩn: {filepath}")

if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    md_file = "reports/bao_cao_tuan_1_2_nguyen_quang_huy.md"
    docx_file = "reports/bao_cao_tuan_1_2_nguyen_quang_huy.docx"
    generate_markdown(md_file)
    create_docx(docx_file)
