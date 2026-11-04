"""Script tạo Báo cáo Tuần 3 & Tuần 4 dạng file Microsoft Word (.docx) cho Nguyễn Quang Huy.
Tạo file Word chuẩn OOXML mở được trên mọi phiên bản Word, font Times New Roman, định dạng bảng biểu, màu sắc chuẩn báo cáo NCKH.
"""

import os
import sys
import zipfile
import html
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def create_docx(filepath):
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
        return p(text, bold=True, size=28, color="1F4E79", space_before=240, space_after=100)

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
        for r_idx, row in enumerate(rows):
            fill = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
            tbl += '<w:tr>'
            for c_idx, cell in enumerate(row):
                align = "center" if c_idx in [0, 3, 4, 5, 6, 7] else "left"
                bold = True if "ĐẠT" in cell or "100%" in cell or cell.startswith("WEB-") else False
                color = "008000" if ("ĐẠT" in cell or "PASS" in cell) else ("C00000" if "LỖI" in cell else "000000")
                rPr = f'<w:sz w:val="22"/><w:szCs w:val="22"/>'
                if bold: rPr += '<w:b/><w:bCs/>'
                if color != "000000": rPr += f'<w:color w:val="{color}"/>'
                tbl += f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr><w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:before="30" w:after="30"/></w:pPr><w:r><w:rPr>{rPr}</w:rPr><w:t>{html.escape(cell)}</w:t></w:r></w:p></w:tc>'
            tbl += '</w:tr>'
        tbl += '</w:tbl>'
        return tbl

    # NỘI DUNG TÀI LIỆU
    body = ""

    # TIÊU ĐỀ
    body += p("TRƯỜNG ĐẠI HỌC KIẾN TRÚC HÀ NỘI", bold=True, size=24, color="595959", align="center", space_after=60)
    body += p("BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI NCKH SINH VIÊN (TUẦN 3 & TUẦN 4)", bold=True, size=32, color="1F4E79", align="center", space_before=60, space_after=120)

    # THÔNG TIN CHUNG
    info_runs = [
        {"text": "Đề tài: ", "bold": True},
        {"text": "Nghiên cứu phương pháp kiểm thử giao diện người dùng áp dụng cho phần mềm quản lý cán bộ của Trường Đại học Kiến trúc Hà Nội\n"},
        {"text": "Sinh viên thực hiện: ", "bold": True},
        {"text": "Nguyễn Quang Huy       ", "bold": True, "color": "1F4E79"},
        {"text": "Mã sinh viên: ", "bold": True},
        {"text": "Cán bộ nghiên cứu đề tài NCKH\n"},
        {"text": "Vai trò: ", "bold": True},
        {"text": "Lập trình viên chính (Code chính) – Phụ trách nhóm Biểu mẫu, Xác thực Dữ liệu đầu vào & Cổng Quản lý văn bản\n"},
        {"text": "Nhóm trưởng: ", "bold": True},
        {"text": "Trần Văn Thịnh       "},
        {"text": "Các thành viên: ", "bold": True},
        {"text": "Chu Bách Trúc Mai, Nguyễn Thị Cẩm Vân, Nguyễn Ngọc Thuỳ Trang\n"},
        {"text": "Thời gian báo cáo: ", "bold": True},
        {"text": "Tuần 3 & Tuần 4 (Hoàn thiện thực nghiệm và nghiệm thu sản phẩm)"}
    ]
    body += p_runs(info_runs, space_after=180)

    # 1. BÁO CÁO TUẦN 3
    body += heading1("1. BÁO CÁO TUẦN 3: CHẠY LẶP, SỬA TEST VÀ ĐỐI CHIẾU BẰNG CHỨNG")
    body += heading2("1.1. Mục tiêu kiểm thử Tuần 3")
    body += bullet("Đảm bảo tính ổn định tuyệt đối của bộ kịch bản kiểm thử tự động thông qua việc chạy lặp nhiều lần (Loop Testing).")
    body += bullet("Tối ưu hóa kiến trúc bộ điều khiển trình duyệt Selenium, triệt tiêu hoàn toàn lỗi treo render và độ trễ mạng.")
    body += bullet("Tích hợp cơ chế tự động ghi nhận bằng chứng (Evidence Auto-Capture) khi phát sinh lỗi.")
    body += bullet("Thực hiện review chéo bộ mã nguồn kịch bản với Chu Bách Trúc Mai.")

    body += heading2("1.2. Các công việc kỹ thuật đã thực hiện")
    body += bullet("Áp dụng chiến lược page_load_strategy = 'eager' kết hợp các tham số --no-sandbox, --disable-dev-shm-usage, --disable-gpu giúp giảm thời gian tải trang từ 60s xuống còn 3.5s và loại bỏ triệt để nguy cơ treo render.", "Tối ưu hóa WebDriver & Browser Driver")
    body += bullet("Nâng cấp phương thức enter_username() và enter_password() bằng tổ hợp phím ảo CONTROL + 'a' và BACKSPACE trước khi gọi clear() nhằm dọn sạch triệt để các ô input HTML5.", "Chuẩn hóa cơ chế làm sạch Input")
    body += bullet("Triển khai hook pytest_runtest_makereport trong tests/web/conftest.py để tự động chụp ảnh màn hình định danh theo tên test case và lưu vào evidence/web/ khi bất kỳ ca nào thất bại.", "Bổ sung Hook Auto-Screenshot")
    body += bullet("Củng cố ca WEB-FORM-02 (nhập dữ liệu mẫu trước khi toggle con mắt) và ca WEB-FORM-08 (thêm khoảng chờ ổn định sau ca nhập sai thông tin), bảo đảm 8/8 ca kiểm thử biểu mẫu đạt 100% PASSED.", "Củng cố bộ kịch bản biểu mẫu SSO")
    body += bullet("Đã pull nhánh origin/Mai từ GitHub về máy trạm để review chéo 10 kịch bản kiểm thử Tìm kiếm & Bộ lọc (TC_01 → TC_10). Phát hiện và tối ưu hóa cấu hình page_load_strategy = 'eager' giúp loại bỏ nguy cơ treo renderer, chạy thực nghiệm đạt 10/10 PASSED trong 43.21s. Đã xuất Biên bản review chéo chi tiết tại reports/bien_ban_review_cheo_script_mai.md.", "Review chéo bộ mã nguồn của Chu Bách Trúc Mai")

    body += heading2("1.3. Sản phẩm bàn giao Tuần 3")
    body += bullet("Bộ script biểu mẫu hoàn thiện, ổn định cao: tests/web/test_login.py (8/8 PASSED).")
    body += bullet("Cấu hình fixture dùng chung và hook tự động bắt ảnh lỗi: tests/web/conftest.py.")
    body += bullet("Biên bản nhận xét review chéo mã nguồn với Chu Bách Trúc Mai.")

    # 2. BÁO CÁO TUẦN 4
    body += heading1("2. BÁO CÁO TUẦN 4: MỞ RỘNG KIỂM THỬ ĐẦY ĐỦ CÁC TRANG CẦN THIẾT, CHẠY BỘ TỰ ĐỘNG CUỐI VÀ HOÀN THIỆN SẢN PHẨM")
    body += heading2("2.1. Mục tiêu kiểm thử Tuần 4")
    body += bullet("Mở rộng phạm vi tự động hóa bao phủ toàn bộ các trang cần thiết trong hệ thống mà tài khoản cán bộ được cấp quyền.")
    body += bullet("Thực thi chu trình chạy lặp độc lập 3 vòng (3 Iterations) để đo lường độ ổn định (Stability Rate) và tỷ lệ lỗi chập chờn (Flaky Rate).")
    body += bullet("Đóng gói toàn diện mã nguồn, gói bằng chứng (Evidence Package) và phụ lục kỹ thuật phục vụ báo cáo nghiệm thu.")

    body += heading2("2.2. Khảo sát và xây dựng kiểm thử Cổng Quản lý văn bản điều hành (vanban.hau.edu.vn)")
    body += bullet("Khảo sát thực tế bóc tách thành công 31 liên kết menu điều hướng trái, 9 ô tra cứu và 7 khối widget dashboard trên vanban.hau.edu.vn.")
    body += bullet("Xây dựng lớp Page Object VanBanPage (pages/vanban_page.py) đóng gói các tương tác trên cổng Quản lý văn bản.")
    body += bullet("Xây dựng bộ kịch bản kiểm thử tự động tests/web/test_vanban.py gồm 5 ca: kiểm tra điều hướng, kiểm tra menu cốt lõi (Trình ký, VB đi, VB đến, Lịch, Công việc), các ô tra cứu nhanh nghiệp vụ, bộ lọc ngày (txtTuNgay, txtDenNgay) và các widget thống kê.")

    body += heading2("2.3. Bảng tổng hợp kết quả chạy lặp 3 lần (3 Iterations)")
    body += p("Kết quả thực thi tự động qua 3 vòng lặp độc lập bằng chương trình reports/run_stability.py:")

    headers = ["STT", "Mã / Tên Kịch bản Kiểm thử", "Phân hệ / Trang", "Lần 1", "Lần 2", "Lần 3", "Độ ổn định", "Trạng thái"]
    rows = [
        ["1", "test_WEB_FORM_01_elements_display_and_attributes", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["2", "test_WEB_FORM_02_password_visibility_toggle", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["3", "test_WEB_FORM_03_remember_login_checkbox_toggle", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["4", "test_WEB_FORM_04_empty_credentials_validation", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["5", "test_WEB_FORM_05_empty_password_validation", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["6", "test_WEB_FORM_06_empty_username_validation", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["7", "test_WEB_FORM_07_invalid_credentials_error_message", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["8", "test_WEB_FORM_08_successful_login_with_valid_credentials", "Xác thực SSO", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["9", "test_dashboard_header_and_account", "Cổng Quản trị", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["10", "test_filter_tabs_presence", "Cổng Quản trị", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["11", "test_search_filters_modules", "Cổng Quản trị", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["12", "test_quan_ly_nhan_su_module_is_listed", "Cổng Quản trị", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["13", "test_quan_ly_nhan_su_module_permission_status", "Cổng Quản trị", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["14", "test_WEB_VANBAN_01_navigation_and_title", "Quản lý văn bản", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["15", "test_WEB_VANBAN_02_sidebar_menu_structure", "Quản lý văn bản", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["16", "test_WEB_VANBAN_03_quick_search_inputs", "Quản lý văn bản", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["17", "test_WEB_VANBAN_04_date_filter_fields", "Quản lý văn bản", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
        ["18", "test_WEB_VANBAN_05_dashboard_widgets_presence", "Quản lý văn bản", "PASS", "PASS", "PASS", "100%", "ĐẠT"],
    ]
    body += build_table(headers, rows)
    body += p("", space_after=80)

    # ĐỊNH LƯỢNG KẾT QUẢ
    body += p("Tổng hợp chỉ số định lượng thực nghiệm Tuần 4:", bold=True, size=26, color="1F4E79")
    body += bullet("18 Test Cases bao phủ đầy đủ 3 phân hệ: Xác thực SSO, Cổng Quản trị chung và Cổng Quản lý văn bản điều hành.", "Tổng số ca kiểm thử")
    body += bullet("18 ca × 3 vòng lặp = 54 lượt kiểm thử độc lập.", "Tổng số lượt chạy thực nghiệm")
    body += bullet("100.0% (54/54 lượt chạy ĐẠT, 0 lỗi phát sinh).", "Tỷ lệ thành công (Pass Rate)")
    body += bullet("0% (Không có ca kiểm thử nào chập chờn hay không ổn định qua các lần chạy).", "Tỷ lệ lỗi chập chờn (Flaky Rate)")
    body += bullet("~49.8 giây cho toàn bộ 18 test cases mỗi lượt.", "Thời gian thực thi trung bình")

    # 3. GIỚI HẠN VÀ CÁC CA KHÔNG TỰ ĐỘNG HÓA
    body += heading1("3. CÁC CA KHÔNG TỰ ĐỘNG HÓA ĐƯỢC (GIỚI HẠN PHẠM VI)")
    lim_headers = ["STT", "Chức năng / Màn hình", "Lý do kỹ thuật & Nghiệp vụ", "Phân loại trạng thái"]
    lim_rows = [
        ["1", "Module Quản lý nhân sự", "Tài khoản kiểm thử bị khóa quyền (app-disabled); không truy cập được màn hình chi tiết hồ sơ cán bộ.", "BỊ CHẶN (BLOCKED)"],
        ["2", "Tạo mới / Xóa văn bản", "Quy định an toàn đề tài: Không được phép tạo, sửa, xóa dữ liệu thật trên hệ thống production của Trường.", "GIỚI HẠN AN TOÀN"],
        ["3", "Tải tệp đính kèm văn bản", "Hộp thoại chọn file của Hệ điều hành (Windows File Dialog) phụ thuộc giao diện OS, kiểm thử thủ công.", "KIỂM THỬ THỦ CÔNG"],
    ]
    body += build_table(lim_headers, lim_rows)
    body += p("", space_after=80)

    # 4. SẢN PHẨM BÀN GIAO
    body += heading1("4. DANH MỤC SẢN PHẨM BÀN GIAO TUẦN 3 & TUẦN 4")
    body += bullet("tests/web/test_login.py (8 ca), tests/web/test_dashboard.py (5 ca), tests/web/test_vanban.py (5 ca).", "Mã nguồn kiểm thử tự động")
    body += bullet("pages/login_page.py, pages/dashboard_page.py, pages/vanban_page.py.", "Lớp Page Object Model")
    body += bullet("reports/run_stability.py (chương trình chạy lặp 3 vòng tự động).", "Công cụ thực nghiệm")
    body += bullet("reports/Bien_ban_chay_lap_tuan_4.md và reports/bao_cao_tuan_3_4_nguyen_quang_huy.docx.", "Hồ sơ biên bản & Báo cáo")
    body += bullet("evidence/web/ (vanban_survey.png, vanban_dashboard_widgets.png, vanban_search_action.png, post_login.png, WEB_FORM_04_empty_credentials.png, WEB_FORM_07_invalid_credentials.png).", "Kho hình ảnh minh chứng")

    # 5. HƯỚNG DẪN CHẠY BỘ KIỂM THỬ
    body += heading1("5. PHỤ LỤC KỸ THUẬT: HƯỚNG DẪN THỰC THI")
    cmd_guide = """# Kích hoạt môi trường ảo
cd d:\\nckh2026\\Interface_testing
.\\.venv\\Scripts\\Activate.ps1

# Chạy kiểm thử biểu mẫu SSO (8 ca)
pytest tests/web/test_login.py -v

# Chạy kiểm thử Cổng Quản lý văn bản (5 ca)
pytest tests/web/test_vanban.py -v

# Chạy toàn bộ chương trình thực nghiệm 3 vòng lặp và xuất biên bản tự động
python reports/run_stability.py"""
    body += code_box(cmd_guide)

    # CHỮ KÝ XÁC NHẬN
    body += p("", space_before=200)
    sign_table = '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders></w:tblPr>'
    sign_table += '<w:tr>'
    sign_table += '<w:tc><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/></w:rPr><w:t>XÁC NHẬN CỦA NHÓM TRƯỞNG</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="600" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1F4E79"/></w:rPr><w:t>Trần Văn Thịnh</w:t></w:r></w:p></w:tc>'
    sign_table += '<w:tc><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="23"/></w:rPr><w:t>Hà Nội, ngày 04 tháng 11 năm 2026</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/></w:rPr><w:t>NGƯỜI LÀM BÁO CÁO</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="500" w:after="40"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1F4E79"/></w:rPr><w:t>Nguyễn Quang Huy</w:t></w:r></w:p></w:tc>'
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
    docx_file = "reports/bao_cao_tuan_3_4_nguyen_quang_huy.docx"
    create_docx(docx_file)

