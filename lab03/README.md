# Bài Lab 3: Viết một script Bash để kiểm tra trạng thái của các dịch vụ hệ thống (như nginx, mysql) và gửi email cảnh báo nếu bất kỳ dịch vụ nào bị dừng
* Cài đặt yêu cầu gửi email (Ubuntu)
>sudo apt-get install mailutils

* Tạo script check_services.sh
```
#!/bin/bash

# Định nghĩa danh sách các dịch vụ cần kiểm tra
SERVICES=("nginx" "mysql")

# Định nghĩa email người nhận
EMAIL="your_email@example.com"

# Kiểm tra trạng thái của mỗi dịch vụ
for SERVICE in "${SERVICES[@]}"; do
    # Kiểm tra trạng thái dịch vụ
    systemctl is-active --quiet "$SERVICE"
    
    # Nếu dịch vụ không hoạt động, gửi email cảnh báo
    if [ $? -ne 0 ]; then
        echo "$SERVICE service is down! Please check the system." | mail -s "$SERVICE is DOWN!" "$EMAIL"
        echo "Cảnh báo đã được gửi cho $SERVICE."
    else
        echo "$SERVICE service is running."
    fi
done
```
* Thiết lập cron job để chạy script tự động
  1. Mở crontab bằng lệnh:
  >crontab -e
  2. Thêm dòng sau để chạy script mỗi 10 phút
  >*/10 * * * * /path/to/check_services.sh

