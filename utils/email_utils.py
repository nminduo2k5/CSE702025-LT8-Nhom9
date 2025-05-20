import smtplib
from email.mime.text import MIMEText

def send_attendance_email(to_email, student_name, datetime_str):
    subject = "Thông báo điểm danh"
    body = f"Chào {student_name},\nBạn đã được điểm danh vào lúc {datetime_str}."
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "your_email@gmail.com"  # Thay bằng email gửi đi
    msg["To"] = to_email

    # Cấu hình SMTP (ví dụ dùng Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your_email@gmail.com"    # Thay bằng email gửi đi
    smtp_pass = "your_app_password"       # Thay bằng app password (không phải mật khẩu thường)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_email], msg.as_string())
        server.quit()
        print(f"Đã gửi email điểm danh cho {to_email}")
    except Exception as e:
        print(f"Lỗi gửi email cho {to_email}: {e}")
