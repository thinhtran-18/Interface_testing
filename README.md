# Kiểm thử giao diện phần mềm quản lý cán bộ

Kho mã dùng chung cho đề tài nghiên cứu khoa học sinh viên về kiểm thử giao diện người dùng của phần mềm quản lý cán bộ Trường Đại học Kiến trúc Hà Nội.

## Phạm vi

- Kiểm thử hộp đen bằng tay trên phiên bản Web và ứng dụng di động.
- Dùng Selenium để tự động hóa một số kịch bản phù hợp trên Web.
- Không dùng Selenium để kiểm thử ứng dụng di động. Kết quả di động được ghi theo biểu mẫu kiểm thử thủ công trong `tests/mobile/manual/`.
- Chỉ kiểm thử trên môi trường và tài khoản đã được cho phép. Chỉ dùng dữ liệu giả hoặc đã ẩn danh.

## Cấu trúc

```text
Interface_testing/
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── README.md
├── pytest.ini
├── requirements.txt
├── docs/                         # Phạm vi, quy ước, mẫu biểu
├── pages/                        # Page Object cho giao diện Web
├── test_data/                    # Chỉ dữ liệu giả/đã ẩn danh
├── tests/
│   ├── web/                      # Selenium + pytest
│   └── mobile/
│       ├── manual/               # Test case thủ công ứng dụng di động
│       └── devices/              # Cấu hình thiết bị/hệ điều hành
├── evidence/
│   ├── web/                      # Bằng chứng đã rà soát và ẩn danh
│   └── mobile/                   # Bằng chứng đã rà soát và ẩn danh
└── reports/                      # Hướng dẫn tổng hợp; không commit báo cáo chạy tạm
```

## Cài đặt trên Windows PowerShell

Yêu cầu Python và Chrome đã được cài trên máy. Mở PowerShell tại thư mục repo:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Mở `.env` và điền `APP_BASE_URL` bằng địa chỉ môi trường thử đã được cấp quyền. Không ghi tài khoản/mật khẩu vào file này nếu không cần thiết; tuyệt đối không commit `.env`.

Chạy ca Web:

```powershell
pytest -q
```

Test tự động có thể cần Selenium tải driver tương thích lần chạy đầu, nên máy cần được phép truy cập mạng. Selenium Manager đi kèm Selenium hiện đại và thường tự quản lý driver; nếu môi trường nhóm chặn tải xuống, ghi lỗi môi trường và thống nhất cách cài với người phụ trách IT.

## Cài đặt trên macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
pytest -q
```

## Kết quả kiểm thử

Test Selenium ghi kết quả vào terminal. Khi bổ sung lưu ảnh/log, lưu trong `test-results/` hoặc `logs/`; các thư mục này được Git bỏ qua. Bằng chứng đưa vào báo cáo nghiên cứu phải được rà soát, ẩn danh và đặt trong `evidence/web/` hoặc `evidence/mobile/`, kèm mã test case và ngày chạy.

## Thành viên

- Trần Văn Thịnh: điều phối, cấu trúc khung tự động hóa và tích hợp.
- Nguyễn Quang Huy: Selenium cho biểu mẫu, dữ liệu và thông báo Web.
- Chu Bách Trúc Mai: Selenium cho tra cứu, hiển thị và điều hướng Web.
- Nguyễn Thị Cẩm Vân: ma trận, test case và kết quả kiểm thử thủ công Web.
- Nguyễn Ngọc Thuỳ Trang: test case và kết quả kiểm thử thủ công ứng dụng di động.

Quy trình nhánh và cách cộng tác xem `CONTRIBUTING.md`.
