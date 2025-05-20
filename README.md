CSE702025-LT8-Nhóm-9

Hệ Thống Điểm Danh Bằng Nhận Diện Khuôn Mặt

Tổng Quan Dự Án

Dự án phát triển một hệ thống điểm danh tự động tiên tiến tại Đại học Phenikaa, ứng dụng công nghệ nhận diện khuôn mặt hiện đại. Hệ thống tích hợp các thuật toán SCRFD để phát hiện khuôn mặt và ArcFace để nhận diện danh tính, mang lại độ chính xác cao trong môi trường lớp học thực tế. Giải pháp này khắc phục các hạn chế của phương pháp điểm danh truyền thống như tốn thời gian, dễ sai sót và nguy cơ gian lận.



Tính Năng Chính





Phát Hiện Khuôn Mặt: Sử dụng SCRFD để phát hiện khuôn mặt nhanh chóng và chính xác, kể cả trong điều kiện ánh sáng phức tạp.



Nhận Diện Khuôn Mặt: Ứng dụng ArcFace để xác minh danh tính đáng tin cậy, đảm bảo tính minh bạch.



Xử Lý Thời Gian Thực: Hỗ trợ điểm danh tức thì, tiết kiệm thời gian và tăng hiệu quả quản lý.



Giới Thiệu Sinh Viên







Thông tin



Chi tiết





Họ và Tên



Nguyễn Minh Dương





Mã Số Sinh Viên



23010441





Lớp



KTPM-LT8





Email



23010441@st.phenikaa-uni.edu.vn





Vai Trò



Người thực hiện chính, chịu trách nhiệm thiết kế, triển khai và đánh giá hệ thống.





Chuyên Ngành



Công nghệ Thông tin, chuyên sâu về Thị Giác Máy Tính.



Liên Hệ

Mọi thắc mắc hoặc đóng góp ý kiến, vui lòng liên hệ:
📧 Email: 23010441@st.phenikaa-uni.edu.vn
👤 Người liên hệ: Nguyễn Minh Dương

## Lợi ích khi tích hợp Kafka vào hệ thống

*(Đã loại bỏ Kafka, phần này chỉ giữ lại nếu bạn muốn tham khảo về tích hợp Kafka trong tương lai)*

## Khi đã có Kafka, có cần giữ lại SQLite không?

*(Đã loại bỏ Kafka, hệ thống hiện tại chỉ sử dụng SQLite để lưu trữ dữ liệu điểm danh, người dùng, sinh viên...)*

## Hướng dẫn chạy Kafka trên local để hệ thống hoạt động

*(Đã loại bỏ Kafka, không cần thực hiện các bước này nếu không sử dụng Kafka trong hệ thống của bạn)*

---

**Tóm lại:**  
- Luôn phải chạy Zookeeper và Kafka server trước khi chạy app.
- Đảm bảo `localhost:9092` đang mở và không bị firewall chặn.
- Khi Kafka đã chạy, app sẽ gửi event thành công, không còn báo lỗi "No Kafka broker available".

### Lưu ý khi gửi email thông báo điểm danh

1. **Đảm bảo trường email của sinh viên đã được lưu trong database**
   - Khi đăng ký hoặc nhập dữ liệu sinh viên, cần có cột `email` hợp lệ cho từng sinh viên.
   - Nếu thiếu email, hệ thống sẽ không gửi được thông báo cho sinh viên đó.

2. **Nếu dùng Gmail để gửi email tự động**
   - Không dùng mật khẩu Gmail thông thường, mà phải bật tính năng "App Password" (Mật khẩu ứng dụng) trong phần bảo mật tài khoản Google.
   - Hướng dẫn:  
     - Truy cập https://myaccount.google.com/security  
     - Bật xác thực 2 bước (2-Step Verification).
     - Tạo "App Password" cho ứng dụng (chọn loại app là "Mail", thiết bị là "Other").
     - Sử dụng app password này trong code thay cho mật khẩu Gmail.

3. **Nếu gửi nhiều email (nhiều sinh viên/lớp lớn)**
   - Nên xử lý gửi email theo kiểu bất đồng bộ (asynchronous) hoặc dùng queue (ví dụ: Celery, RabbitMQ, Redis Queue) để tránh gửi quá nhanh dẫn đến bị Google hoặc nhà cung cấp email chặn/tạm khóa tài khoản.
   - Có thể thêm delay nhỏ giữa các lần gửi hoặc gom nhóm gửi theo batch.
   - Nếu gửi số lượng lớn, nên dùng dịch vụ email chuyên nghiệp như SendGrid, Amazon SES, Mailgun...

4. **Kiểm tra thư mục Spam**
   - Email gửi tự động có thể bị vào Spam, nên hướng dẫn sinh viên kiểm tra cả thư mục Spam/Junk.

5. **Bảo mật thông tin**
   - Không lưu trữ app password hoặc thông tin nhạy cảm trong code public hoặc repo công khai.

## Kiểm tra dữ liệu trong database SQLite

Bạn có thể kiểm tra dữ liệu trong file SQLite (`system.db`) bằng các cách sau:

### 1. Dùng lệnh sqlite3 trên terminal/cmd

- Mở terminal/cmd, chuyển đến thư mục chứa file `system.db`:
  ```
  cd database
  sqlite3 system.db
  ```
- Sau đó, trong giao diện sqlite3:
  ```
  .tables
  SELECT * FROM users;
  SELECT * FROM attendance;
  SELECT name, seq FROM sqlite_sequence;
  .schema users
  .schema attendance
  .exit
  ```

### 2. Dùng DB Browser for SQLite (giao diện đồ họa)

- Tải và cài đặt [DB Browser for SQLite](https://sqlitebrowser.org/).
- Mở file `system.db` để xem, sửa, truy vấn dữ liệu trực quan.

### 3. Dùng Python với db_queries.py

Bạn có thể viết một đoạn script nhỏ để kiểm tra dữ liệu, ví dụ:

````python
# filepath: check_db.py
from database.db_queries import fetch_users

users = fetch_users()
for user in users:
    print(user)
````

Hoặc tự viết truy vấn SQL với sqlite3:

````python
# filepath: check_db.py
import sqlite3

conn = sqlite3.connect('database/system.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)
conn.close()
````

---

**Tóm lại:**  
- Có thể kiểm tra database bằng lệnh sqlite3, phần mềm DB Browser, hoặc code Python sử dụng db_queries.py.
- Nên dùng DB Browser for SQLite để xem dữ liệu trực quan, dễ thao tác.

### Giải thích về bảng `sqlite_sequence` trong SQLite

- `sqlite_sequence` là bảng hệ thống (system table) do SQLite tự động tạo ra khi bạn sử dụng cột `AUTOINCREMENT` trong các bảng (ví dụ: `id INTEGER PRIMARY KEY AUTOINCREMENT`).
- Bảng này lưu trữ tên bảng (`name`) và giá trị tự tăng hiện tại (`seq`) cho mỗi bảng có sử dụng AUTOINCREMENT.
- Khi bạn thêm bản ghi mới vào bảng có AUTOINCREMENT, SQLite sẽ tăng giá trị `seq` trong `sqlite_sequence` để đảm bảo mỗi giá trị là duy nhất và không bị lặp lại, kể cả khi bạn xóa bản ghi.

**Ví dụ:**  
- Nếu bạn có bảng `users` với `id INTEGER PRIMARY KEY AUTOINCREMENT`, thì dòng tương ứng trong `sqlite_sequence` sẽ cho biết giá trị id lớn nhất đã được sử dụng cho bảng `users`.
- Khi bạn thêm bản ghi mới, id sẽ tăng tiếp từ giá trị này.

**Truy vấn:**  
```sql
SELECT name, seq FROM sqlite_sequence;
```
- Kết quả sẽ cho bạn biết giá trị tự tăng hiện tại của từng bảng.

**Tóm lại:**  
- Bạn không cần thao tác trực tiếp với `sqlite_sequence` trong ứng dụng bình thường.
- Đây là bảng hệ thống giúp SQLite quản lý giá trị tự tăng cho các bảng có AUTOINCREMENT.