-- Kiểm tra và tạo cơ sở dữ liệu nếu chưa tồn tại
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'flaskdb') THEN
      CREATE DATABASE flaskdb;
   END IF;
END
$$;

-- Kết nối vào cơ sở dữ liệu flaskdb
\c flaskdb;

-- Kiểm tra và tạo bảng nếu chưa tồn tại
CREATE TABLE IF NOT EXISTS greetings (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL
);

-- Chèn dữ liệu nếu bảng rỗng
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM greetings) THEN
      INSERT INTO greetings (message) VALUES ('Hello, World!');
   END IF;
END
$$;

