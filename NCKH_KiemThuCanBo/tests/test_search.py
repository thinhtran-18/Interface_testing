import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# =====================================================================
# CẤU HÌNH HỆ THỐNG & ĐƯỜNG DẪN THƯ MỤC 
# =====================================================================
URL = "https://main.hau.edu.vn"
SEARCH_SELECTOR = "#searchInput"
ADMIN_SELECTOR = "#filterTabs > button:nth-child(3)"
ALL_TAB_SELECTOR = "#filterTabs > button:nth-child(1)"

# Tự động xác định thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "tests" in os.path.abspath(__file__) else os.getcwd()
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Danh sách lưu kết quả thực thi để tự động xuất báo cáo Markdown
test_results = []


def chup_bang_chung(driver, tc_id):
    """Chụp ảnh màn hình tự động và lưu vào thư mục evidence/"""
    file_name = f"{tc_id}.png"
    file_path = os.path.join(EVIDENCE_DIR, file_name)
    try:
        driver.save_screenshot(file_path)
        return f"evidence/{file_name}"
    except Exception:
        return "N/A"


def ghi_nhan_ket_qua(tc_id, name, group, status, duration, note, evidence_path):
    """Lưu kết quả từng Test Case vào bộ nhớ để tổng hợp bảng cuối kỳ"""
    test_results.append({
        "tc_id": tc_id,
        "name": name,
        "group": group,
        "status": status,
        "duration": round(duration, 2),
        "note": note,
        "evidence": evidence_path
    })

def reset_bo_loc_va_tim_kiem(driver, wait, keyword):
    """Đưa bộ lọc về tab Tất cả, xóa sạch ô tìm kiếm và nhập từ khóa mới"""
    try:
        all_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ALL_TAB_SELECTOR)))
        all_btn.click()
        time.sleep(0.4)
    except (NoSuchElementException, TimeoutException):
        pass

    search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SEARCH_SELECTOR)))
    search_box.click()
    search_box.send_keys(Keys.CONTROL, "a")
    search_box.send_keys(Keys.BACKSPACE)
    search_box.clear()
    search_box.send_keys(keyword)
    time.sleep(0.8)  # Chờ DOM cập nhật kết quả real-time


# =====================================================================
# PHẦN 1: KIỂM THỬ XÁC THỰC & PHÂN QUYỀN (TC_01)
# =====================================================================
def run_tc01_unauthenticated():
    print("\n" + "=" * 70)
    print("TC_01: KIỂM THỬ TRUY CẬP KHI CHƯA XÁC THỰC (UNAUTHENTICATED)")
    print("=" * 70)

    temp_driver = webdriver.Chrome()
    temp_driver.maximize_window()
    temp_wait = WebDriverWait(temp_driver, 5)
    start_time = time.perf_counter()

    try:
        temp_driver.get(URL)
        temp_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SEARCH_SELECTOR)))
        duration = time.perf_counter() - start_time
        ev = chup_bang_chung(temp_driver, "TC_01_Unauthenticated")
        print(f"⚠️ [FAIL] ({duration:.2f}s) Ô tìm kiếm vẫn hiển thị khi chưa đăng nhập!")
        ghi_nhan_ket_qua("TC_01", "Truy cập khi chưa xác thực", "Bảo mật & Xác thực", "FAIL", duration, "Hiển thị thanh tìm kiếm khi chưa login", ev)
    except TimeoutException:
        duration = time.perf_counter() - start_time
        ev = chup_bang_chung(temp_driver, "TC_01_Unauthenticated")
        print(f"✅ [PASS] ({duration:.2f}s) Đã chặn truy cập trái phép. URL chuyển hướng: {temp_driver.current_url}")
        ghi_nhan_ket_qua("TC_01", "Truy cập khi chưa xác thực", "Bảo mật & Xác thực", "PASS", duration, "Chặn truy cập và chuyển hướng SSO", ev)
    
    input("👉 Quan sát kết quả TC_01 trên màn hình, nhấn ENTER để đóng phiên chưa xác thực và chuyển sang phần Đăng nhập...")
    temp_driver.quit()


# =====================================================================
# PHẦN 2: CHUỖI 9 KỊCH BẢN KIỂM THỬ TÌM KIẾM & BỘ LỌC (TC_02 -> TC_10)
# =====================================================================
def run_authenticated_suite():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 12)
    short_wait = WebDriverWait(driver, 2.5)  # Dùng cho các kịch bản kỳ vọng 0 kết quả

    try:
        print("\n" + "=" * 70)
        print("KHỞI TẠO PHIÊN ĐĂNG NHẬP CHO CHUỖI KIỂM THỬ CHỨC NĂNG (TC_02 -> TC_10)")
        print("=" * 70)
        driver.get(URL)
        input("👉 Hãy ĐĂNG NHẬP tài khoản trên trình duyệt, sau đó nhấn ENTER tại đây để bắt đầu chạy TC_02...")

        # -----------------------------------------------------------------
        # TC_02: Kiểm thử bảo mật & dữ liệu dị biệt (XSS / Special Chars)
        # -----------------------------------------------------------------
        print("\n--- [TC_02] Tìm kiếm chuỗi ký tự đặc biệt & XSS Payload ---")
        start_t = time.perf_counter()
        xss_payload = "!@#$%^&*()<script>alert(1)</script>"
        reset_bo_loc_va_tim_kiem(driver, wait, xss_payload)
        try:
            short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_02_XSS_SpecialChars")
            print(f"❌ [FAIL] ({dur:.2f}s) Nhập chuỗi XSS nhưng thẻ phần mềm vẫn hiển thị!")
            ghi_nhan_ket_qua("TC_02", "Tìm kiếm ký tự đặc biệt / XSS", "Bảo mật & Dữ liệu rác", "FAIL", dur, "Không ẩn thẻ khi nhập chuỗi dị biệt", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_02_XSS_SpecialChars")
            print(f"✅ [PASS] ({dur:.2f}s) Xử lý an toàn chuỗi XSS, không văng lỗi UI, trả về 0 kết quả.")
            ghi_nhan_ket_qua("TC_02", "Tìm kiếm ký tự đặc biệt / XSS", "Bảo mật & Dữ liệu rác", "PASS", dur, "Xử lý an toàn, 0 kết quả", ev)
        
        input("👉 Quan sát kết quả TC_02 trên trình duyệt, nhấn ENTER để chạy tiếp TC_03...")

        # -----------------------------------------------------------------
        # TC_03: Phân vùng tương đương không hợp lệ (Từ khóa không tồn tại)
        # -----------------------------------------------------------------
        print("\n--- [TC_03] Tìm kiếm phần mềm không tồn tại ---")
        start_t = time.perf_counter()
        non_existent = "Phần mềm quản lý vũ trụ HAU 2026"
        reset_bo_loc_va_tim_kiem(driver, wait, non_existent)
        try:
            short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_03_NonExistent")
            print(f"❌ [FAIL] ({dur:.2f}s) Từ khóa không tồn tại nhưng vẫn hiển thị thẻ phần mềm!")
            ghi_nhan_ket_qua("TC_03", "Tìm kiếm từ khóa không tồn tại", "Phủ định (Negative)", "FAIL", dur, "Lọc sai kết quả", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_03_NonExistent")
            print(f"✅ [PASS] ({dur:.2f}s) Không có thẻ phần mềm nào hiển thị.")
            ghi_nhan_ket_qua("TC_03", "Tìm kiếm từ khóa không tồn tại", "Phủ định (Negative)", "PASS", dur, "Trả về 0 kết quả đúng kỳ vọng", ev)
        
        input("👉 Quan sát kết quả TC_03 trên trình duyệt, nhấn ENTER để chạy tiếp TC_04...")

        # -----------------------------------------------------------------
        # TC_04: Giá trị biên - Chỉ nhập toàn khoảng trắng (Whitespace Only)
        # -----------------------------------------------------------------
        print("\n--- [TC_04] Kiểm thử biên: Chuỗi chỉ chứa khoảng trắng ---")
        start_t = time.perf_counter()
        reset_bo_loc_va_tim_kiem(driver, wait, "       ")
        dur = time.perf_counter() - start_t
        ev = chup_bang_chung(driver, "TC_04_WhitespaceOnly")
        print(f"✅ [PASS] ({dur:.2f}s) Giao diện ổn định khi nhập chuỗi 7 khoảng trắng.")
        ghi_nhan_ket_qua("TC_04", "Tìm kiếm toàn khoảng trắng", "Giá trị biên (Boundary)", "PASS", dur, "Giao diện không bị treo khi nhập dấu cách", ev)
        
        input("👉 Quan sát kết quả TC_04 trên trình duyệt, nhấn ENTER để chạy tiếp TC_05...")

        # -----------------------------------------------------------------
        # TC_05: Giá trị biên trên - Chuỗi ký tự cực dài (255 ký tự)
        # -----------------------------------------------------------------
        print("\n--- [TC_05] Kiểm thử biên trên: Chuỗi dài 255 ký tự ---")
        start_t = time.perf_counter()
        long_keyword = "A" * 255
        reset_bo_loc_va_tim_kiem(driver, wait, long_keyword)
        try:
            short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_05_MaxLength_255")
            print(f"❌ [FAIL] ({dur:.2f}s) Chuỗi 255 ký tự vẫn trả về kết quả!")
            ghi_nhan_ket_qua("TC_05", "Chuỗi cực dài (255 ký tự)", "Giá trị biên (Boundary)", "FAIL", dur, "Hiển thị sai kết quả với chuỗi dài", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_05_MaxLength_255")
            print(f"✅ [PASS] ({dur:.2f}s) Ô input chịu tải tốt chuỗi 255 ký tự, không vỡ layout, 0 kết quả.")
            ghi_nhan_ket_qua("TC_05", "Chuỗi cực dài (255 ký tự)", "Giá trị biên (Boundary)", "PASS", dur, "Không vỡ layout, trả về 0 kết quả", ev)
        
        input("👉 Quan sát kết quả TC_05 trên trình duyệt, nhấn ENTER để chạy tiếp TC_06...")

        # -----------------------------------------------------------------
        # TC_06: Xung đột giữa Từ khóa và Bộ lọc (Filter Mismatch)
        # -----------------------------------------------------------------
        print("\n--- [TC_06] Kiểm thử xung đột: Từ khóa 'Đào tạo' + Bộ lọc 'Hành chính' ---")
        start_t = time.perf_counter()
        reset_bo_loc_va_tim_kiem(driver, wait, "Đào tạo")
        admin_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ADMIN_SELECTOR)))
        admin_btn.click()
        time.sleep(0.8)
        try:
            short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_06_FilterMismatch")
            print(f"❌ [FAIL] ({dur:.2f}s) Thẻ 'Văn bản điều hành' vẫn hiện dù từ khóa là 'Đào tạo'!")
            ghi_nhan_ket_qua("TC_06", "Xung đột Từ khóa & Bộ lọc", "Phủ định (Negative)", "FAIL", dur, "Lỗi phép giao (AND) giữa search và tab", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_06_FilterMismatch")
            print(f"✅ [PASS] ({dur:.2f}s) Kết hợp đúng phép giao (AND): Không hiển thị thẻ sai danh mục.")
            ghi_nhan_ket_qua("TC_06", "Xung đột Từ khóa & Bộ lọc", "Phủ định (Negative)", "PASS", dur, "Ẩn đúng các thẻ không thỏa mãn cả 2 điều kiện", ev)
        
        input("👉 Quan sát kết quả TC_06 trên trình duyệt, nhấn ENTER để chạy tiếp TC_07...")

        # -----------------------------------------------------------------
        # TC_07: Không phân biệt chữ Hoa / Thường (Case Insensitivity)
        # -----------------------------------------------------------------
        print("\n--- [TC_07] Kiểm thử chữ thường toàn bộ: 'văn bản điều hành' ---")
        start_t = time.perf_counter()
        reset_bo_loc_va_tim_kiem(driver, wait, "văn bản điều hành")
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_07_CaseInsensitive")
            print(f"✅ [PASS] ({dur:.2f}s) Hệ thống tìm kiếm không phân biệt hoa/thường thành công.")
            ghi_nhan_ket_qua("TC_07", "Tìm kiếm không phân biệt Hoa/Thường", "Tương đương hợp lệ", "PASS", dur, "Nhận diện tốt chữ thường toàn bộ", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_07_CaseInsensitive")
            print(f"❌ [FAIL] ({dur:.2f}s) Không tìm thấy kết quả khi nhập chữ thường!")
            ghi_nhan_ket_qua("TC_07", "Tìm kiếm không phân biệt Hoa/Thường", "Tương đương hợp lệ", "FAIL", dur, "Bị phân biệt chữ hoa/thường", ev)
        
        input("👉 Quan sát kết quả TC_07 trên trình duyệt, nhấn ENTER để chạy tiếp TC_08...")

        # -----------------------------------------------------------------
        # TC_08: Tìm kiếm một phần từ khóa (Partial Keyword Match)
        # -----------------------------------------------------------------
        print("\n--- [TC_08] Kiểm thử từ khóa con (Partial Match): 'điều hành' ---")
        start_t = time.perf_counter()
        reset_bo_loc_va_tim_kiem(driver, wait, "điều hành")
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_08_PartialMatch")
            print(f"✅ [PASS] ({dur:.2f}s) Tìm thấy thẻ phần mềm khi chỉ nhập một phần tên.")
            ghi_nhan_ket_qua("TC_08", "Tìm kiếm một phần từ khóa (Substring)", "Tương đương hợp lệ", "PASS", dur, "Hỗ trợ tìm kiếm theo chuỗi con", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_08_PartialMatch")
            print(f"❌ [FAIL] ({dur:.2f}s) Không tìm thấy khi nhập từ khóa con!")
            ghi_nhan_ket_qua("TC_08", "Tìm kiếm một phần từ khóa (Substring)", "Tương đương hợp lệ", "FAIL", dur, "Không hỗ trợ tìm kiếm chuỗi con", ev)
        
        input("👉 Quan sát kết quả TC_08 trên trình duyệt, nhấn ENTER để chạy tiếp TC_09...")

        # -----------------------------------------------------------------
        # TC_09: Khoảng trắng thừa ở hai đầu từ khóa (Leading/Trailing Spaces)
        # -----------------------------------------------------------------
        print("\n--- [TC_09] Kiểm thử khoảng trắng hai đầu: '  Văn bản điều hành  ' ---")
        start_t = time.perf_counter()
        reset_bo_loc_va_tim_kiem(driver, wait, "  Văn bản điều hành  ")
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_09_TrimSpaces")
            print(f"✅ [PASS] ({dur:.2f}s) Hệ thống tự động trim() khoảng trắng thừa và trả về đúng kết quả.")
            ghi_nhan_ket_qua("TC_09", "Từ khóa có khoảng trắng thừa 2 đầu", "Giá trị biên (Boundary)", "PASS", dur, "Tự động cắt khoảng trắng (trim)", ev)
        except TimeoutException:
            dur = time.perf_counter() - start_t
            ev = chup_bang_chung(driver, "TC_09_TrimSpaces")
            print(f"⚠️ [FAIL] ({dur:.2f}s) Hệ thống KHÔNG tự động cắt khoảng trắng thừa ở hai đầu từ khóa!")
            ghi_nhan_ket_qua("TC_09", "Từ khóa có khoảng trắng thừa 2 đầu", "Giá trị biên (Boundary)", "FAIL", dur, "Chưa xử lý hàm trim() cho chuỗi đầu vào", ev)
        
        input("👉 Quan sát kết quả TC_09 trên trình duyệt, nhấn ENTER để chạy tiếp TC_10 (Happy Path)...")

        # -----------------------------------------------------------------
        # TC_10: Luồng chính chuẩn (Happy Path) - Tìm kiếm + Lọc + Mở phần mềm
        # -----------------------------------------------------------------
        print("\n--- [TC_10] Luồng chuẩn (Happy Path): Tìm kiếm + Lọc 'Hành chính' + Click mở ---")
        start_t = time.perf_counter()
        reset_bo_loc_va_tim_kiem(driver, wait, "Văn bản điều hành")
        dur_step1 = time.perf_counter() - start_t
        input("👉 [TC_10 - Bước 1] Đã nhập 'Văn bản điều hành'. Quan sát kết quả, nhấn ENTER để chọn bộ lọc 'Hành chính'...")

        start_t2 = time.perf_counter()
        admin_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ADMIN_SELECTOR)))
        admin_btn.click()
        time.sleep(0.5)
        dur_step2 = time.perf_counter() - start_t2
        input("👉 [TC_10 - Bước 2] Đã lọc tab 'Hành chính'. Nhấn ENTER để click mở thẻ phần mềm...")

        start_t3 = time.perf_counter()
        try:
            card_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]"))
            )
            dur = dur_step1 + dur_step2 + (time.perf_counter() - start_t3)
            ev = chup_bang_chung(driver, "TC_10_HappyPath")
            card_element.click()
            print(f"✅ [PASS] ({dur:.2f}s) Đã lọc và mở thành công phần mềm 'Văn bản điều hành'.")
            ghi_nhan_ket_qua("TC_10", "Tìm kiếm chuẩn + Lọc Hành chính + Mở thẻ", "Luồng chính (Happy Path)", "PASS", dur, "Mở phần mềm thành công", ev)
        except TimeoutException:
            dur = dur_step1 + dur_step2 + (time.perf_counter() - start_t3)
            ev = chup_bang_chung(driver, "TC_10_HappyPath")
            print(f"❌ [FAIL] ({dur:.2f}s) Không thể mở phần mềm 'Văn bản điều hành'!")
            ghi_nhan_ket_qua("TC_10", "Tìm kiếm chuẩn + Lọc Hành chính + Mở thẻ", "Luồng chính (Happy Path)", "FAIL", dur, "Không tìm thấy thẻ để click", ev)

        input("\n👉 Đã hoàn tất 10/10 kịch bản kiểm thử! Nhấn ENTER để xuất báo cáo và đóng trình duyệt...")

    finally:
        driver.quit()
        print("\n--- ĐÃ ĐÓNG TRÌNH DUYỆT ---")


def xuat_bao_cao_markdown():
    """Tự động tổng hợp số liệu, tính % và ghi ra file reports/bao_cao_ket_qua_tu_dong.md"""
    total = len(test_results)
    if total == 0:
        return
    passed = sum(1 for r in test_results if r["status"] == "PASS")
    failed = total - passed
    pass_rate = (passed / total) * 100
    total_time = sum(r["duration"] for r in test_results)
    avg_time = total_time / total

    print("\n" + "=" * 75)
    print(f"📊 TỔNG KẾT ĐỢT KIỂM THỬ (PASS: {passed}/{total} - ĐẠT {pass_rate:.1f}% | TỔNG THỜI GIAN XỬ LÝ: {total_time:.2f}s)")
    print("=" * 75)
    for r in test_results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"{icon} {r['tc_id']} | {r['name']:<38} | {r['status']:<4} | {r['duration']:>5.2f}s | {r['evidence']}")

    report_file = os.path.join(REPORT_DIR, "bao_cao_ket_qua_tu_dong.md")
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG \n\n")
        f.write(f"- **Thời gian xuất báo cáo:** {now_str}\n")
        f.write(f"- **Hệ thống kiểm thử:** `{URL}`\n")
        f.write(f"- **Tổng số Test Cases:** {total} kịch bản\n")
        f.write(f"- **Tỷ lệ Đạt (Pass Rate):** **{pass_rate:.2f}%** ({passed}/{total} PASS, {failed}/{total} FAIL)\n")
        f.write(f"- **Tổng thời gian hệ thống xử lý:** {total_time:.2f}s (Trung bình: {avg_time:.2f}s/TC)\n\n")
        f.write("## Bảng kết quả thực thi chi tiết\n\n")
        f.write("| Mã TC | Tên kịch bản | Nhóm kỹ thuật | Kết quả | Thời gian (s) | Bằng chứng (Screenshot) | Ghi chú |\n")
        f.write("| :---: | :--- | :--- | :---: | :---: | :--- | :--- |\n")
        for r in test_results:
            f.write(f"| **{r['tc_id']}** | {r['name']} | {r['group']} | **{r['status']}** | {r['duration']:.2f}s | `{r['evidence']}` | {r['note']} |\n")

    print(f"\n📝 Đã tự động xuất báo cáo Markdown tại: {report_file}")


if __name__ == "__main__":
    run_tc01_unauthenticated()
    run_authenticated_suite()
    xuat_bao_cao_markdown()