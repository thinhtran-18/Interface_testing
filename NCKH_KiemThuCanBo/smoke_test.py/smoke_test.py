#test môi trường, ko liên quan đến nội dung NC 
from selenium import webdriver
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt Chrome
driver = webdriver.Chrome()

try:
    # Mở trang web công khai dùng để thử môi trường
    driver.get("https://example.com/")
    
    # Đọc tiêu đề trang
    title = driver.title
    print("Tieu de trang:", title)
    
    # Đọc nội dung đoạn văn bản đầu tiên trên trang (thay vì h1)
    paragraph = driver.find_element(By.TAG_NAME, "p")
    print("Noi dung Paragraph:", paragraph.text)
    
    print("KET QUA: PASS")

finally:
    # Đóng trình duyệt sau khi thử nghiệm
    driver.quit()