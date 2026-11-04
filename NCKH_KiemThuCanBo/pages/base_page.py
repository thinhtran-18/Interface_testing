from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Giúp script chạy ổn định và hạn chế tối đa lỗi do tải trang chậm.
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_url(self, url):
        """Mở một đường dẫn URL bất kỳ"""
        self.driver.get(url)

    def find_element_with_wait(self, locator):
        """Chờ và tìm kiếm phần tử xuất hiện trên giao diện"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click_element(self, locator):
        """Chờ phần tử cho phép click và thực hiện thao tác click"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def send_keys_to_element(self, locator, text):
        """Chờ phần tử hiển thị, xóa nội dung cũ và nhập văn bản mới"""
        element = self.find_element_with_wait(locator)
        element.clear()
        element.send_keys(text)
        return element

    def get_page_title(self):
        """Lấy tiêu đề trang hiện tại"""
        return self.driver.title

    def get_current_url(self):
        """Lấy đường dẫn URL hiện tại của trình duyệt"""
        return self.driver.current_url