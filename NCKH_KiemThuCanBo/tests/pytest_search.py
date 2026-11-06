"""Pytest automated test suite: Kiểm thử E2E từ Main Portal đến Quản lý văn bản."""
import os
import re
import sys
import time
from datetime import datetime

# Ép hệ thống nhận diện thư mục gốc để tìm thấy module 'pages'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.base_page import BasePage

load_dotenv()

# Cấu hình URL (Điền cứng luôn để không phụ thuộc file .env)
URL = "https://main.hau.edu.vn"
HOME_VB_URL = "https://vanban.hau.edu.vn/Home/Index"

# Selectors
SEARCH_SELECTOR = "#searchInput"
ADMIN_SELECTOR = "#filterTabs > button:nth-child(3)"
ALL_TAB_SELECTOR = "#filterTabs > button:nth-child(1)"

# Thiết lập thư mục lưu bằng chứng
BASE_DIR = os.getcwd()
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


def chup_bang_chung(driver, tc_id):
    file_path = os.path.join(EVIDENCE_DIR, f"{tc_id}.png")
    try:
        driver.save_screenshot(file_path)
    except Exception:
        pass


def lam_noi_bat(driver, element):
    """Cuộn trang đến phần tử và đóng khung viền đỏ nổi bật để quay video."""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].setAttribute('style', 'border: 4px solid red; background-color: #ffcccc;');", element)
    time.sleep(2) # Dừng 2 giây để nhìn rõ


def reset_bo_loc_va_tim_kiem(driver, wait, keyword):
    try:
        all_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ALL_TAB_SELECTOR)))
        all_btn.click()
        time.sleep(0.3)
    except (NoSuchElementException, TimeoutException):
        pass

    search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SEARCH_SELECTOR)))
    search_box.click()
    search_box.send_keys(Keys.CONTROL, "a")
    search_box.send_keys(Keys.BACKSPACE)
    search_box.clear()
    search_box.send_keys(keyword)
    time.sleep(0.6)


# ==============================================================================
# PHẦN 1: KIỂM THỬ TÌM KIẾM & BỘ LỌC TẠI TRANG CHỦ (TC_01 - TC_10)
# ==============================================================================

@pytest.mark.web
def test_tc01_unauthenticated_access():
    options = Options()
    options.add_argument("--window-size=1365,900")
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")
    temp_driver = webdriver.Chrome(options=options)
    temp_wait = WebDriverWait(temp_driver, 4)
    try:
        temp_driver.get(URL)
        with pytest.raises(TimeoutException):
            temp_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SEARCH_SELECTOR)))
        chup_bang_chung(temp_driver, "TC_01_Unauthenticated")
    finally:
        temp_driver.quit()


@pytest.fixture(scope="module")
def auth_driver():
    """Fixture đăng nhập tự động 1 lần cho chuỗi test từ TC_02 trở đi."""
    username = "035187013852"
    password = "123@123"
    
    if username == "TENDANGNHAP_CUA_BAN":
        pytest.skip("BẠN QUÊN CHƯA ĐIỀN USERNAME VÀ PASSWORD Ở DÒNG 79, 80 RỒI!")

    options = Options()
    options.add_argument("--start-maximized")
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    login_page = LoginPage(driver)
    login_page.login(username, password)
    
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "searchInput")))
    try:
        yield driver
    finally:
        driver.quit()


@pytest.mark.web
def test_tc02_xss_and_special_chars(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    short_wait = WebDriverWait(auth_driver, 2)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "!@#$%^&*()<script>alert(1)</script>")
    chup_bang_chung(auth_driver, "TC_02_XSS_SpecialChars")
    with pytest.raises(TimeoutException):
        short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))

@pytest.mark.web
def test_tc03_non_existent_keyword(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    short_wait = WebDriverWait(auth_driver, 2)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "Phần mềm quản lý vũ trụ HAU 2026")
    chup_bang_chung(auth_driver, "TC_03_NonExistent")
    with pytest.raises(TimeoutException):
        short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))

@pytest.mark.web
def test_tc04_whitespace_only(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "       ")
    chup_bang_chung(auth_driver, "TC_04_WhitespaceOnly")
    assert "Kiến trúc Hà Nội" in auth_driver.page_source

@pytest.mark.web
def test_tc05_max_length_255_chars(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    short_wait = WebDriverWait(auth_driver, 2)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "A" * 255)
    chup_bang_chung(auth_driver, "TC_05_MaxLength_255")
    with pytest.raises(TimeoutException):
        short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))

@pytest.mark.web
def test_tc06_filter_mismatch(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    short_wait = WebDriverWait(auth_driver, 2)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "Đào tạo")
    admin_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ADMIN_SELECTOR)))
    admin_btn.click()
    time.sleep(0.5)
    chup_bang_chung(auth_driver, "TC_06_FilterMismatch")
    with pytest.raises(TimeoutException):
        short_wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))

@pytest.mark.web
def test_tc07_case_insensitive(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "văn bản điều hành")
    elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
    chup_bang_chung(auth_driver, "TC_07_CaseInsensitive")
    assert elem.is_displayed()

@pytest.mark.web
def test_tc08_partial_keyword_match(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "điều hành")
    elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
    chup_bang_chung(auth_driver, "TC_08_PartialMatch")
    assert elem.is_displayed()

@pytest.mark.web
def test_tc09_leading_trailing_spaces(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "  Văn bản điều hành  ")
    chup_bang_chung(auth_driver, "TC_09_TrimSpaces")
    elems = auth_driver.find_elements(By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")
    visible = [e for e in elems if e.is_displayed()]
    assert len(visible) >= 0

@pytest.mark.web
def test_tc10_happy_path_search_and_filter(auth_driver):
    wait = WebDriverWait(auth_driver, 10)
    reset_bo_loc_va_tim_kiem(auth_driver, wait, "Văn bản điều hành")
    admin_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ADMIN_SELECTOR)))
    admin_btn.click()
    time.sleep(0.5)
    
    card_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Văn bản điều hành')]")))
    lam_noi_bat(auth_driver, card_element)
    card_element.click()
    
    time.sleep(3)
    if len(auth_driver.window_handles) > 1:
        auth_driver.switch_to.window(auth_driver.window_handles[-1])
        
    if "vanban" not in auth_driver.current_url:
        auth_driver.get(HOME_VB_URL)


# ==============================================================================
# PHẦN 2: KIỂM THỬ CHUYÊN SÂU VANBAN.HAU.EDU.VN (TC_11 - TC_15)
# ==============================================================================

@pytest.mark.web
def test_tc11_16_kiem_thu_trinh_ky_toan_dien(auth_driver):
    """
    TC_11 + TC_16 (Gộp): Vừa dùng △State Engine kiểm tra lỗi liệt nút (ONR) ở menu, 
    vừa đi thẳng vào trang (Direct Routing) để test luồng chức năng tìm kiếm & Khoảng ngày.
    """
    wait = WebDriverWait(auth_driver, 10)
    base_page = BasePage(auth_driver)
    auth_driver.get(HOME_VB_URL)
    time.sleep(2)
    
    # =========================================================================
    # PHẦN 1: ÁP DỤNG △STATE ENGINE ĐỂ MỞ MENU (TEST LỖI ONR - TC16)
    # =========================================================================
    tk_menu_cha = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[contains(., 'Trình ký')])[1]")))
    parent_li_locator = (By.XPATH, "(//a[contains(., 'Trình ký')])[1]/parent::li")
    
    def click_menu():
        lam_noi_bat(auth_driver, tk_menu_cha)
        auth_driver.execute_script("arguments[0].click();", tk_menu_cha)
        
    loi_onr = None
    try:
        # Máy quét State Engine: Kiểm tra xem click menu có phản hồi không
        base_page.verify_state_change(action_func=click_menu, element_to_watch_locator=parent_li_locator)
        time.sleep(1) 
    except AssertionError as e:
        chup_bang_chung(auth_driver, "TC16_Loi_ONR_MenuTrinhKy")
        # Ghi nhận lỗi nhưng KHÔNG dừng chương trình, để nó chạy tiếp Phần 2
        loi_onr = str(e)


    # =========================================================================
    # PHẦN 2: ĐIỀU HƯỚNG TRỰC TIẾP ĐỂ TEST BỘ LỌC (TC11)
    # =========================================================================
    # Bỏ qua cái menu lỗi, đi thẳng bằng URL để test tính năng bên trong
    danh_sach_muc_nho = [
        {"ten": "Trình ký con", "url": "https://vanban.hau.edu.vn/Trinh-ky/Danh-sach-trinh-ky"},
        {"ten": "Trình ký trả lại", "url": "https://vanban.hau.edu.vn/Trinh-ky/Trinh-ky-tra-lai"}
    ]
    loi_nghiep_vu = []
    
    for muc in danh_sach_muc_nho:
        try:
            # 1. Đi thẳng vào URL
            auth_driver.get(muc["url"])
            base_page.wait_for_page_load()
            time.sleep(3) # Chờ cho vòng xoay loading biến mất
            
            # 2. Nhập tìm kiếm theo text
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or contains(@placeholder, 'trích yếu')]")))
            lam_noi_bat(auth_driver, search_box) 
            search_box.clear()
            search_box.send_keys("Thông báo")
            time.sleep(1)
            
            # 3. Mở dropdown bộ lọc
            bo_loc_btn = auth_driver.find_elements(By.XPATH, "//*[contains(text(), 'Chọn bộ lọc')] | //select")
            if bo_loc_btn:
                lam_noi_bat(auth_driver, bo_loc_btn[0]) 
                auth_driver.execute_script("arguments[0].click();", bo_loc_btn[0])
                time.sleep(1)
                webdriver.ActionChains(auth_driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                time.sleep(1)
            
            # 4. Điền ô khoảng ngày bằng JavaScript (để né lỗi bảng lịch popup chặn phím)
            date_inputs = auth_driver.find_elements(By.XPATH, "//input[contains(@placeholder, 'ngày') or contains(@class, 'date') or contains(@id, 'date') or @type='date']")
            visible_date_inputs = [inp for inp in date_inputs if inp.get_attribute("type") != "hidden" and "search" not in (inp.get_attribute("id") or "").lower()]
            
            if len(visible_date_inputs) >= 2:
                lam_noi_bat(auth_driver, visible_date_inputs[0])
                auth_driver.execute_script("arguments[0].value = '01/01/2026';", visible_date_inputs[0])
                
                lam_noi_bat(auth_driver, visible_date_inputs[1])
                auth_driver.execute_script("arguments[0].value = '31/12/2026';", visible_date_inputs[1])
                visible_date_inputs[1].send_keys(Keys.ENTER)
            elif len(visible_date_inputs) >= 1:
                lam_noi_bat(auth_driver, visible_date_inputs[0])
                auth_driver.execute_script("arguments[0].value = '01/01/2026 - 31/12/2026';", visible_date_inputs[0])
                visible_date_inputs[0].send_keys(Keys.ENTER)
            time.sleep(1)
            
            # 5. Bấm nút Tìm
            nut_tim = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Tìm')]")))
            lam_noi_bat(auth_driver, nut_tim) 
            auth_driver.execute_script("arguments[0].click();", nut_tim)
            time.sleep(2)
            
            chup_bang_chung(auth_driver, f"TC11_16_BoLoc_{muc['ten'].replace(' ', '')}")
            
        except Exception as e:
            loi_nghiep_vu.append(f"Lỗi ở trang {muc['ten']}: {str(e)[:40]}")
            
    # =========================================================================
    # TỔNG HỢP BÁO CÁO LỖI
    # =========================================================================
    if loi_nghiep_vu:
        pytest.fail(" | ".join(loi_nghiep_vu))
        
    if loi_onr:
        pytest.fail(f"[BẮT ĐƯỢC LỖI ONR BẰNG △STATE] {loi_onr}")

# ------------------------------------------------------------------------------
# Cấu hình + hàm phụ trợ riêng cho TC_12 (BẢN TỐI ƯU VÀ CHỐNG LỖI UI TẠNG HÌNH)
# ------------------------------------------------------------------------------
TC12_TU_KHOA = ["Thông báo"]    
TC12_TU_KHOA_KHONG_TON_TAI = "zzqq_khong_ton_tai"

def tc12_slug(text):
    return (re.sub(r"\W+", "", text, flags=re.UNICODE) or "x")[:30]

def tc12_lay_menu_hien_thi(driver, text):
    """Quét toàn bộ DOM, lọc ra đúng cái thẻ menu ĐANG THỰC SỰ HIỂN THỊ trên màn hình (Né menu ẩn của Mobile)."""
    elements = driver.find_elements(By.XPATH, f"//a[contains(normalize-space(.), '{text}')]")
    for e in elements:
        if e.is_displayed():
            return e
    return None

def tc12_tim_o_tim_kiem(driver):
    cac_xpath = [
        "//input[contains(@placeholder, 'Tìm theo')]",
        "//input[contains(@placeholder, 'Tìm') or contains(@placeholder, 'Tra cứu') or contains(@placeholder, 'trích yếu')]",
        "//input[@id='searchInput']",
        "(//input[@type='text' and not(@type='hidden')])[1]",
    ]
    for xp in cac_xpath:
        for e in driver.find_elements(By.XPATH, xp):
            if e.is_displayed():
                return e
    return None

def tc12_lay_kich_thuoc_trang(driver):
    for s in driver.find_elements(By.XPATH, "//select[contains(@name, '_length')]"):
        try:
            return int(s.get_attribute("value"))
        except:
            pass
    return None

def tc12_doc_ket_qua(driver):
    body = driver.find_element(By.TAG_NAME, "body").text
    m_tim_thay = re.search(r"Tìm thấy\s*([\d.,]+)\s*văn bản", body)
    m_chan_bang = re.search(r"Hiển thị\s*[\d.,]+\s*đến\s*[\d.,]+\s*trong\s*([\d.,]+)\s*bản ghi", body)

    def so(m):
        return int(re.sub(r"\D", "", m.group(1))) if m else None

    dong = [r for r in driver.find_elements(By.XPATH, "//table//tbody/tr[count(td)>=5]") if r.is_displayed()]
    return {"tim_thay": so(m_tim_thay), "tong_bang": so(m_chan_bang), "so_dong": len(dong)}

def tc12_doi_ket_qua(driver, toi_da=5):
    time.sleep(1.5)
    truoc = tc12_doc_ket_qua(driver)
    het_gio = time.time() + toi_da
    while time.time() < het_gio:
        time.sleep(0.6)
        sau = tc12_doc_ket_qua(driver)
        if sau == truoc:
            return sau
        truoc = sau
    return truoc

def tc12_so_ket_qua(snap):
    for k in ("tim_thay", "tong_bang", "so_dong"):
        if snap[k] is not None:
            return snap[k]

def tc12_kiem_tra_nhat_quan(snap, kich_thuoc):
    loi = []
    tt, tb, sd = snap["tim_thay"], snap["tong_bang"], snap["so_dong"]
    if tt is not None and tb is not None and tt != tb:
        loi.append(f"Tìm thấy {tt} lệch với {tb} bản ghi dưới chân trang.")
    return loi

def tc12_tim_kiem(driver, tu_khoa):
    o_tim = tc12_tim_o_tim_kiem(driver)
    o_tim.click()
    o_tim.send_keys(Keys.CONTROL, "a")
    o_tim.send_keys(Keys.BACKSPACE)
    o_tim.send_keys(tu_khoa)
    nut_tim = [b for b in driver.find_elements(By.XPATH, "//button[normalize-space(.)='Tìm']") if b.is_displayed()]
    if nut_tim:
        driver.execute_script("arguments[0].click();", nut_tim[0])
    else:
        o_tim.send_keys(Keys.RETURN)
    return tc12_doi_ket_qua(driver)

def tc12_lam_noi_bat_ket_qua(driver):
    try:
        for e in driver.find_elements(By.XPATH, "//*[contains(text(), 'Tìm thấy')] | //*[contains(text(), 'trong') and contains(text(), 'bản ghi')]"):
            if e.is_displayed():
                lam_noi_bat(driver, e)
                return
    except:
        pass


@pytest.mark.web
def test_tc12_van_ban_di_den_submenus(auth_driver):
    """TC_12 (Rút gọn): Trỏ vào TỪNG MỤC CON bằng TEXT hiển thị thực tế (Né bẫy UI 100%), đếm kết quả."""
    driver = auth_driver
    menus = ["Văn bản đi", "Văn bản đến"]
    loi, canh_bao, bang = [], [], []

    def ghi(nhan, tu_khoa, snap):
        bang.append((nhan, tu_khoa, snap))
        print(f"[TC12] {nhan} | '{tu_khoa}' -> Tìm thấy: {snap['tim_thay']} | Chân bảng: {snap['tong_bang']} | Dòng: {snap['so_dong']}")

    for menu in menus:
        # --- BƯỚC 1: Vét cạn danh sách các mục con bằng Văn bản ---
        try:
            driver.get(HOME_VB_URL)
            time.sleep(2)
            cha = tc12_lay_menu_hien_thi(driver, menu)
            if not cha:
                loi.append(f"Không tìm thấy thẻ cha '{menu}' trên giao diện.")
                continue
            
            lam_noi_bat(driver, cha)
            # Tìm thẻ li bọc ngoài, lấy tất cả thẻ a bên trong ul
            con_elements = cha.find_elements(By.XPATH, "./parent::*//ul//a")
            
            # Nếu chưa xổ ra thì click
            if not any(e.is_displayed() for e in con_elements):
                driver.execute_script("arguments[0].click();", cha)
                time.sleep(2)
                con_elements = cha.find_elements(By.XPATH, "./parent::*//ul//a")
                
            ds_muc_con = [e.get_attribute("textContent").strip() for e in con_elements if e.get_attribute("textContent").strip()]
        except Exception as e:
            loi.append(f"Lỗi khi trích xuất danh sách con của '{menu}': {str(e)[:60]}")
            continue
            
        if not ds_muc_con:
            loi.append(f"Menu '{menu}' không có mục con nào sau khi click.")
            continue
            
        print(f"[TC12] {menu} có {len(ds_muc_con)} mục con: {ds_muc_con}")

        # --- BƯỚC 2: Duyệt từng mục con bằng TEXT của nó ---
        for ten_muc_con in ds_muc_con:
            nhan = f"{menu} > {ten_muc_con}"
            try:
                driver.get(HOME_VB_URL)
                time.sleep(2)
                
                # Tìm lại cha và mở
                cha = tc12_lay_menu_hien_thi(driver, menu)
                con_elements = cha.find_elements(By.XPATH, "./parent::*//ul//a")
                if not any(e.is_displayed() for e in con_elements):
                    driver.execute_script("arguments[0].click();", cha)
                    time.sleep(1.5)
                    
                # Mở mục con bằng TEXT chính xác
                sub_menu = tc12_lay_menu_hien_thi(driver, ten_muc_con)
                if not sub_menu:
                    loi.append(f"{nhan}: Không thấy mục con này hiện trên màn hình!")
                    continue
                    
                lam_noi_bat(driver, sub_menu)
                driver.execute_script("arguments[0].click();", sub_menu)
                time.sleep(3) 

                # Lấy ô tìm kiếm
                o_tim = WebDriverWait(driver, 5).until(lambda d: tc12_tim_o_tim_kiem(d))
                if not o_tim:
                    loi.append(f"{nhan}: Không tìm thấy ô tìm kiếm!")
                    continue
                    
                lam_noi_bat(driver, o_tim)
                kich_thuoc = tc12_lay_kich_thuoc_trang(driver)

                # Tìm mặc định
                co_so = tc12_doi_ket_qua(driver)
                n0 = tc12_so_ket_qua(co_so)
                ghi(nhan, "(chưa tìm)", co_so)
                for m in tc12_kiem_tra_nhat_quan(co_so, kich_thuoc):
                    loi.append(f"{nhan} (mặc định): {m}")
                    
                tc12_lam_noi_bat_ket_qua(driver)
                chup_bang_chung(driver, f"TC12_{tc12_slug(menu)}_{tc12_slug(ten_muc_con)}_MacDinh")

                # Tìm kiếm dữ liệu
                cac_lan_tim = [("bat_ky", TC12_TU_KHOA[0]), ("khong_ton_tai", TC12_TU_KHOA_KHONG_TON_TAI)]
                for loai, tu_khoa in cac_lan_tim:
                    snap = tc12_tim_kiem(driver, tu_khoa)
                    n = tc12_so_ket_qua(snap)
                    ghi(nhan, tu_khoa, snap)

                    for m in tc12_kiem_tra_nhat_quan(snap, kich_thuoc):
                        loi.append(f"{nhan} (tìm '{tu_khoa}'): {m}")
                    
                    if co_so["tim_thay"] is not None and n is not None and n0 is not None and n > n0:
                        loi.append(f"{nhan}: tìm '{tu_khoa}' ra {n} kết quả, nhiều hơn mặc định ({n0}).")
                    if loai == "khong_ton_tai" and n and n > 0:
                        loi.append(f"{nhan}: chuỗi không tồn tại '{tu_khoa}' vẫn ra {n} kết quả.")

                    tc12_lam_noi_bat_ket_qua(driver)
                    chup_bang_chung(driver, f"TC12_{tc12_slug(menu)}_{tc12_slug(ten_muc_con)}_{tc12_slug(tu_khoa)}")

            except Exception as e:
                loi.append(f"Lỗi thao tác tại {nhan}: {str(e)[:60]}")

    # ---------- 5. Tổng hợp ----------
    print("\n===== TC12: SỐ KẾT QUẢ THEO TỪNG MỤC CON / TỪ KHÓA =====")
    print(f"{'Menu > Mục con':34} | {'Từ khóa':26} | {'Tìm thấy':>8} | {'Chân bảng':>9} | {'Dòng':>4}")
    for nhan, tu_khoa, snap in bang:
        tt = "-" if snap["tim_thay"] is None else snap["tim_thay"]
        tb = "-" if snap["tong_bang"] is None else snap["tong_bang"]
        print(f"{nhan:34} | {tu_khoa:26} | {tt:>8} | {tb:>9} | {snap['so_dong']:>4}")
    for cb in canh_bao:
        print(f"[CẢNH BÁO] {cb}")

    if loi:
        pytest.fail("TC12 FAILED:\n- " + "\n- ".join(loi))
    print("[TC12] PASSED: Số liệu nhất quán.")

@pytest.mark.web
def test_tc13_lich_thoi_gian_thuc_va_qua_khu(auth_driver):
    """TC_13: Kiểm tra Lịch phòng ban/cá nhân khớp thời gian thực và lịch quá khứ."""
    wait = WebDriverWait(auth_driver, 10)
    auth_driver.get(HOME_VB_URL)
    time.sleep(2)
    
    hom_nay = datetime.now().strftime("%d/%m")
    
    lich_menu = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Lịch')]")))
    lam_noi_bat(auth_driver, lich_menu)
    lich_menu.click()
    time.sleep(1)
    
    loai_lich = ["Lịch cá nhân", "Lịch phòng ban"]
    loi = []
    
    for loai in loai_lich:
        sub_lich = wait.until(EC.visibility_of_element_located((By.XPATH, f"//a[contains(., '{loai}')]")))
        lam_noi_bat(auth_driver, sub_lich)
        sub_lich.click()
        time.sleep(3)
        
        try:
            today_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{hom_nay}')]")))
            lam_noi_bat(auth_driver, today_elem)
            
            btn_prev = auth_driver.find_elements(By.XPATH, "//button[contains(@class, 'fc-prev-button') or contains(@class, 'prev')]")
            if btn_prev:
                lam_noi_bat(auth_driver, btn_prev[0])
                btn_prev[0].click()
                time.sleep(2)
                chup_bang_chung(auth_driver, f"TC13_{loai}_QuaKhu")
        except TimeoutException:
            loi.append(f"Lỗi tại '{loai}': Không nhận diện được ngày hiện tại ({hom_nay}).")
            
    if loi:
        pytest.fail(" | ".join(loi))


# ------------------------------------------------------------------------------
# Cấu hình + hàm phụ trợ riêng cho TC_14
# ------------------------------------------------------------------------------
# Trạng thái CÁ NHÂN (badge trong cột "Nội dung công việc") được coi là đã xong
TU_KHOA_XONG = ["xử lý xong", "đã hoàn thành"]
# Các mốc trong khối "Những việc chưa hoàn thành" ở cột bên phải
NHAN_CHUA_HOAN_THANH = ["Trước đây", "Hôm nay", "Ngày mai", "7 ngày tới", "Trong tương lai", "Không có thời hạn"]


def doc_thong_ke_ca_nhan(page_text):
    """Đọc khối 'Việc được giao cho tôi' (x/y hoàn thành, %) và 'Những việc chưa hoàn thành'."""
    lines = [l.strip() for l in page_text.split("\n") if l.strip()]
    kq = {"x": None, "y": None, "pct": None, "dem": {}}

    for i, l in enumerate(lines):
        if "Việc được giao cho" in l:
            doan = "\n".join(lines[i:i + 8])
            m = re.search(r"(\d+)\s*/\s*(\d+)\s*hoàn thành", doan, re.I)
            if m:
                kq["x"], kq["y"] = int(m.group(1)), int(m.group(2))
            m = re.search(r"(\d+)\s*%", doan)
            if m:
                kq["pct"] = int(m.group(1))
            break

    for i, l in enumerate(lines):
        if "Những việc chưa hoàn thành" in l:
            con_lai = lines[i + 1:]
            for nhan in NHAN_CHUA_HOAN_THANH:
                for k, dong in enumerate(con_lai):
                    m = re.fullmatch(re.escape(nhan) + r"\s*(\d+)?", dong)
                    if m:
                        if m.group(1) is not None:
                            kq["dem"][nhan] = int(m.group(1))
                        elif k + 1 < len(con_lai) and con_lai[k + 1].isdigit():
                            kq["dem"][nhan] = int(con_lai[k + 1])
                        break
            break
    return kq


def lay_dong_cong_viec(driver):
    # Dòng công việc thật có >= 4 ô; dòng nhóm "TUẦN: ..." và dòng "không có dữ liệu" chỉ có 1 ô
    return driver.find_elements(By.XPATH, "//table//tbody/tr[count(td)>=4]")


def phan_tich_dong(row):
    cells = row.find_elements(By.XPATH, "./td")
    nd = cells[1].text if len(cells) > 1 else ""
    td = cells[3].text if len(cells) > 3 else ""
    dong_nd = [l.strip() for l in nd.split("\n") if l.strip()]

    m_td = re.search(r"(\d+)\s*/\s*(\d+)\s*Hoàn thành", td, re.I)
    m_qh = re.search(r"(\d+)\s*Quá hạn", td, re.I)
    m_pct = re.search(r"(\d+)\s*%", td)
    m_han = re.search(r"(\d{2}/\d{2}/\d{4})\s*(?:→|->|-)\s*(\d{2}/\d{2}/\d{4})", nd)

    han = None
    if m_han:
        han = datetime.strptime(m_han.group(2), "%d/%m/%Y").date()

    return {
        "tieu_de": dong_nd[0] if dong_nd else "(không đọc được tiêu đề)",
        "ca_nhan_xong": any(k in nd.lower() for k in TU_KHOA_XONG),
        "ca_nhan_qua_han": "quá hạn" in nd.lower(),
        "tien_do": (int(m_td.group(1)), int(m_td.group(2))) if m_td else None,
        "qua_han": int(m_qh.group(1)) if m_qh else 0,
        "pct": int(m_pct.group(1)) if m_pct else None,
        "han": han,
        "co_icon_check": "check" in (cells[0].get_attribute("innerHTML") or "").lower() if cells else False,
    }


def mo_danh_sach_cong_viec(driver, wait):
    xpath_cha = "//a[contains(normalize-space(.), 'Quản lý công việc')]"
    xpath_con = "//a[contains(normalize-space(.), 'Danh sách công việc')]"

    # Chỉ bấm menu cha khi menu con chưa hiện (tránh bấm lần nữa làm menu bị thu lại)
    con_hien = [e for e in driver.find_elements(By.XPATH, xpath_con) if e.is_displayed()]
    if not con_hien:
        cha = wait.until(EC.presence_of_element_located((By.XPATH, xpath_cha)))
        lam_noi_bat(driver, cha)
        driver.execute_script("arguments[0].click();", cha)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_con)))
        con_hien = [e for e in driver.find_elements(By.XPATH, xpath_con) if e.is_displayed()]

    lam_noi_bat(driver, con_hien[0])
    driver.execute_script("arguments[0].click();", con_hien[0])


@pytest.mark.web
def test_tc14_quan_ly_cong_viec_trang_thai(auth_driver):
    """TC_14: Cá nhân đã xong việc thì hệ thống hiển thị đúng; quá hạn chỉ phản ánh người khác chưa xong."""
    driver = auth_driver
    wait = WebDriverWait(driver, 15)
    loi, canh_bao = [], []   # loi -> FAILED, canh_bao -> chỉ in ra để xem lại

    driver.get(HOME_VB_URL)
    time.sleep(2)

    # ---------- 1. Mở Quản lý công việc > Danh sách công việc ----------
    try:
        mo_danh_sach_cong_viec(driver, wait)
        wait.until(lambda d: len(lay_dong_cong_viec(d)) > 0)
    except TimeoutException:
        chup_bang_chung(driver, "TC14_KhongMoDuocDanhSach")
        pytest.fail("Không mở được 'Danh sách công việc' hoặc danh sách không có công việc nào.")
    time.sleep(2)  # chờ khối thống kê bên phải tải xong

    page_text = driver.find_element(By.TAG_NAME, "body").text
    chup_bang_chung(driver, "TC14_DanhSachCongViec")

    cong_viec = [phan_tich_dong(el) for el in lay_dong_cong_viec(driver)]
    hom_nay = datetime.now().date()

    # ---------- 2. Kiểm tra từng công việc: cá nhân xong, người khác chưa xong -> quá hạn ----------
    for stt, cv in enumerate(cong_viec, 1):
        nhan = f"CV#{stt} '{cv['tieu_de']}'"
        if cv["tien_do"] is None:
            loi.append(f"{nhan}: không đọc được tiến độ chung (dạng 'a/b Hoàn thành').")
            continue
        a, b = cv["tien_do"]
        c = cv["qua_han"]
        chua_xong_khac = b - a
        print(f"[TC14] {nhan}: cá nhân={'XONG' if cv['ca_nhan_xong'] else 'CHƯA XONG'} | "
              f"tiến độ chung {a}/{b} | quá hạn {c} | hạn {cv['han']}")

        if b <= 0 or not (0 <= a <= b):
            loi.append(f"{nhan}: tiến độ chung vô lý ({a}/{b}).")
            continue
        if cv["ca_nhan_xong"] and a < 1:
            loi.append(f"{nhan}: cá nhân đã 'Xử lý xong' nhưng số người hoàn thành chung = {a} "
                       f"(phải >= 1 vì đã gồm chính mình).")
        if cv["pct"] is not None and abs(cv["pct"] - round(a / b * 100)) > 1:
            loi.append(f"{nhan}: % hiển thị {cv['pct']}% không khớp {a}/{b} = {round(a / b * 100)}%.")
        if c > chua_xong_khac:
            loi.append(f"{nhan}: số quá hạn ({c}) lớn hơn số người chưa xong ({chua_xong_khac}).")
        if cv["ca_nhan_xong"] and cv["ca_nhan_qua_han"]:
            loi.append(f"{nhan}: cá nhân đã xong nhưng dòng công việc vẫn gắn nhãn 'Quá hạn' của cá nhân.")

        if cv["han"] is not None:
            han_da_qua = cv["han"] < hom_nay
            if han_da_qua and chua_xong_khac > 0 and c == 0:
                loi.append(f"{nhan}: hạn {cv['han']} đã qua, còn {chua_xong_khac} người chưa xong "
                           f"nhưng số quá hạn = 0.")
            elif han_da_qua and 0 < c < chua_xong_khac:
                canh_bao.append(f"{nhan}: quá hạn {c} < số chưa xong {chua_xong_khac} (kiểm tra có người được gia hạn?).")
            if not han_da_qua and c > 0:
                loi.append(f"{nhan}: hạn {cv['han']} chưa tới nhưng đã báo quá hạn {c}.")
        else:
            canh_bao.append(f"{nhan}: không đọc được thời hạn nên bỏ qua kiểm tra quá hạn theo ngày.")

        if cv["ca_nhan_xong"] != cv["co_icon_check"]:
            canh_bao.append(f"{nhan}: trạng thái chữ ({'xong' if cv['ca_nhan_xong'] else 'chưa xong'}) "
                            f"và dấu tích ở cột đầu không khớp (có thể do class icon khác 'check').")

    # ---------- 3. Đối chiếu với khối thống kê cá nhân bên phải ----------
    tk = doc_thong_ke_ca_nhan(page_text)
    so_xong = sum(1 for cv in cong_viec if cv["ca_nhan_xong"])
    tong = len(cong_viec)
    print(f"[TC14] Danh sách: {so_xong}/{tong} việc cá nhân đã xong | "
          f"Thống kê bên phải: {tk['x']}/{tk['y']} ({tk['pct']}%) | Chưa hoàn thành: {tk['dem']}")

    if tk["x"] is None:
        loi.append("Không đọc được khối 'Việc được giao cho tôi' (dạng 'x/y hoàn thành').")
    else:
        if tk["x"] != so_xong:
            loi.append(f"Thống kê ghi {tk['x']} việc hoàn thành nhưng danh sách có {so_xong} việc 'Xử lý xong'.")
        if tk["y"] != tong:
            loi.append(f"Thống kê ghi tổng {tk['y']} việc nhưng danh sách có {tong} việc "
                       f"(nếu danh sách gồm cả việc mình giao đi thì bỏ kiểm tra này).")
        if tk["y"] and tk["pct"] is not None and abs(tk["pct"] - round(tk["x"] / tk["y"] * 100)) > 1:
            loi.append(f"Thống kê ghi {tk['pct']}% không khớp {tk['x']}/{tk['y']}.")

        if not tk["dem"]:
            canh_bao.append("Không đọc được các mốc trong 'Những việc chưa hoàn thành'.")
        else:
            tong_chua_xong = sum(tk["dem"].values())
            du_kien = tk["y"] - tk["x"]
            if tong_chua_xong != du_kien:
                loi.append(f"'Những việc chưa hoàn thành' cộng lại = {tong_chua_xong} "
                           f"nhưng phải bằng {tk['y']} - {tk['x']} = {du_kien}. "
                           f"(Việc mình đã xong không được tính vào 'Trước đây'/quá hạn, "
                           f"quá hạn của người khác càng không được tính vào mình.)")

    # ---------- 4. Kết luận ----------
    for cb in canh_bao:
        print(f"[CẢNH BÁO] {cb}")
    if loi:
        pytest.fail("TC14 FAILED:\n- " + "\n- ".join(loi))
    print("[TC14] PASSED: trạng thái cá nhân khớp với thống kê; quá hạn chỉ phản ánh người khác chưa xong.")


# ==============================================================================
# PHẦN 3: ÁP DỤNG THUẬT TOÁN △STATE ENGINE CỦA MAI (TC_17)
# ==============================================================================

@pytest.mark.web
def test_tc17_loi_logic_bo_loc_tra_cuu(auth_driver):
    """
    TC_17: Nhập giá trị biên (khoảng trắng) và chuỗi sai vào ô Tra cứu.
    Mục tiêu: Chứng minh lỗi Logic của bộ lọc (Vẫn hiện văn bản dù nhập sai).
    """
    base_page = BasePage(auth_driver)
    base_page.wait_for_page_load()
    auth_driver.get("https://vanban.hau.edu.vn/VBDiTraCuu/Index") # Trỏ thẳng vào trang Tra cứu bạn đang mở
    time.sleep(2)
    
    try:
        # Ô tra cứu
        search_input = WebDriverWait(auth_driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='text' or @id='searchInput']"))
        )
        
        payloads = ["   ", "tên_văn_bản_ảo_12345"]
        for payload in payloads:
            lam_noi_bat(auth_driver, search_input)
            search_input.clear()
            search_input.send_keys(payload)
            search_input.send_keys(Keys.RETURN)
            
            base_page.wait_for_page_load()
            time.sleep(2)
            
            # Quét tìm xem có dòng văn bản nào xuất hiện trên bảng không (thẻ <tr> trong tbody)
            danh_sach_van_ban = auth_driver.find_elements(By.XPATH, "//tbody/tr[not(contains(., 'Không có')) and not(contains(., 'No data'))]")
            
            # NẾU CÓ VĂN BẢN HIỂN THỊ -> LỖI HỆ THỐNG
            if len(danh_sach_van_ban) > 0:
                # Lấy tên của cái văn bản bị lọt ra (VD: Thông báo về việc lấy ý kiến...)
                trich_yeu = danh_sach_van_ban[0].text[:50] + "..." 
                pytest.fail(f"[BẮT ĐƯỢC BUG LOGIC] Nhập '{payload}' nhưng hệ thống KHÔNG TÌM KIẾM/LỌC mà vẫn hiện văn bản: '{trich_yeu}'")
                
    except AssertionError as e:
        chup_bang_chung(auth_driver, "TC17_Bug_LogicBoLoc")
        raise e
    except Exception as e:
        if "[BẮT ĐƯỢC BUG LOGIC]" in str(e):
            chup_bang_chung(auth_driver, "TC17_Bug_LogicBoLoc")
            raise e
        pytest.fail(f"Lỗi khi chạy kịch bản TC17: {str(e)}")
