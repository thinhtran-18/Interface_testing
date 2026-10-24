# Quy ước cộng tác

## Quyền truy cập GitHub

Repo thuộc tài khoản cá nhân nên chủ repo cần mời từng thành viên làm collaborator và cấp quyền **Write** để họ đọc, tạo nhánh, đẩy nhánh và mở Pull Request. Người được mời phải chấp nhận lời mời trước khi quyền có hiệu lực. Không chia sẻ mật khẩu hoặc Personal Access Token của chủ repo.

## Quy trình đề xuất

Mọi người làm trên nhánh riêng và gửi Pull Request vào `main`; chỉ chủ repo hoặc người được thống nhất mới gộp PR. Điều này giữ `main` ở trạng thái dùng được và giảm việc ghi đè thay đổi của nhau.

### Lấy repo lần đầu

Sau khi được mời và đã chấp nhận lời mời, mỗi thành viên clone repo một lần:

```bash
git clone https://github.com/thinhtran-18/Interface_testing-.git
cd Interface_testing-
```

Trên Windows có thể chạy các lệnh trên trong PowerShell hoặc Git Bash. GitHub sẽ yêu cầu đăng nhập qua trình duyệt/Git Credential Manager khi cần; không dùng mật khẩu tài khoản trong lệnh Git.

1. Lấy mã mới nhất:

   ```bash
   git switch main
   git pull origin main
   ```

2. Tạo nhánh có tên ngắn, ví dụ:

   ```bash
   git switch -c feat/web-login-smoke
   git switch -c test/mobile-search-cases
   git switch -c docs/test-case-template
   ```

3. Chỉ thêm các file thuộc phần việc của mình. Kiểm tra trước khi commit:

   ```bash
   git status
   git diff --check
   git diff
   ```

4. Commit và đẩy nhánh:

   ```bash
   git add <duong-dan-file>
   git commit -m "test: add web login cases"
   git push -u origin <ten-nhanh>
   ```

5. Tạo Pull Request trên GitHub, mô tả thay đổi, mã test case liên quan, cách kiểm tra và ảnh bằng chứng đã ẩn danh. Nhờ ít nhất một thành viên review trước khi gộp.

6. Sau khi PR được gộp, cập nhật bản mới:

   ```bash
   git switch main
   git pull origin main
   ```

## Quy ước nội dung

- Không push thẳng lên `main` trong công việc thường ngày.
- Không commit mật khẩu, token, file `.env`, dữ liệu cán bộ thật, ảnh chứa thông tin định danh hoặc kết quả chạy tạm.
- Mỗi test case phải có mã, tiền điều kiện, dữ liệu thử, bước thực hiện và kết quả mong đợi.
- Mỗi báo lỗi phải có bước tái hiện, kết quả mong đợi/thực tế, môi trường và bằng chứng đã ẩn danh.
- Người sửa một test cần giữ mã test case ổn định hoặc ghi rõ mã cũ/mới trong PR.
