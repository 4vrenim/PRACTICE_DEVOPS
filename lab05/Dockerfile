# Chọn image nền Python 3.9
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép requirements.txt vào container
COPY requirements.txt /app/

# Cài đặt các thư viện cần thiết từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng vào container
COPY . /app/

# Mở port 5000
EXPOSE 5000

# Chạy ứng dụng Flask khi container khởi động
CMD ["python", "app.py"]
