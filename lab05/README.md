# Bài Lab 5: Thiết lập Docker Compose để chạy ứng dụng web với một cơ sở dữ liệu PostgreSQL.

Cập nhật requirements.txt cài đặt thêm thư viện psycopg2 để Flask có thể kết nối với PostgreSQL

Cập nhật app.py để kết nối với cơ sở dữ liệu PostgreSQL

Tạo file init_db.sql. File này sẽ được chép vào thư mục /docker-entrypoint-initdb.d/ trong container PostgreSQL. PostgreSQL sẽ tự động chạy các câu lệnh SQL trong file này khi container lần đầu tiên được khởi động, tạo cơ sở dữ liệu và bảng greetings

Tạo file docker-compose.yml để thiết lập ứng dụng Flask và PostgreSQL

Build và khởi động các container
>docker-compose up --build

![image](https://github.com/user-attachments/assets/f5fac486-474a-4944-a528-51a1fec58af0)

![image](https://github.com/user-attachments/assets/b5991085-19b8-4386-94f1-afee5d0b27bc)
