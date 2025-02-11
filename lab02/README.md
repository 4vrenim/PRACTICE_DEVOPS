# Bài Lab 2: Thiết lập cron job để thực hiện script sao lưu dữ liệu mỗi ngày vào lúc 2 giờ sáng.
* Mở crontab để chỉnh sửa
>crontab -e

* Thêm dòng sau vào cuối tệp để cron job chạy mỗi ngày vào lúc 2 giờ sáng
>0 2 * * * /path/to/your/backup.sh
