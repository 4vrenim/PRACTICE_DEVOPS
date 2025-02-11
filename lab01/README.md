# Bài Lab 1: Viết một script Bash để tự động hóa việc sao lưu dữ liệu từ một thư mục cụ thể tới một thư mục khác và nén các tập tin đã sao lưu.
```
#!/bin/bash

# Định nghĩa thư mục nguồn và thư mục đích
SOURCE_DIR="/path/to/source_directory"
BACKUP_DIR="/path/to/backup_directory"

# Tạo tên tệp sao lưu với ngày giờ
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# Sao lưu và nén dữ liệu
tar -czf "$BACKUP_FILE" -C "$SOURCE_DIR" .

echo "Sao lưu thành công! Tệp sao lưu lưu tại: $BACKUP_FILE"
```
