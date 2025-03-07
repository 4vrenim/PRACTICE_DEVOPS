import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Danh sách các dịch vụ cần kiểm tra
SERVICES = ["nginx", "mysql", "docker"]

# Cấu hình email
SMTP_SERVER = "smtp.gmail.com"  # Thay đổi nếu dùng dịch vụ khác
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Dùng App Password nếu dùng Gmail
EMAIL_RECEIVER = "receiver_email@example.com"

def check_service_status(service):
    """Kiểm tra trạng thái dịch vụ."""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "active"
    except Exception as e:
        return False

def send_email_alert(failed_services):
    """Gửi email cảnh báo nếu có dịch vụ bị dừng."""
    subject = "CẢNH BÁO: Dịch vụ hệ thống bị dừng!"
    body = f"Các dịch vụ sau đang bị dừng:\n\n" + "\n".join(failed_services)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Email cảnh báo đã được gửi.")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

def main():
    failed_services = [service for service in SERVICES if not check_service_status(service)]
    if failed_services:
        print(f"Dịch vụ bị dừng: {', '.join(failed_services)}")
        send_email_alert(failed_services)
    else:
        print("Tất cả dịch vụ đều đang chạy bình thường.")

if __name__ == "__main__":
    main()
