# Lab 21: Cài đặt Prometheus trên Docker và cấu hình để thu thập metrics từ một ứng dụng web
## Sử dụng Vagrant tạo VM cài đặt sẵn Docker để chạy các services: Prometheus, Nginx, Nginx Exporter. Ngixn Exporter là thành phần tạo metric.
* Tạo các file Vagrantfile, nginx-status.conf, index.html, compose.yml trong cùng thư mục và chạy `vagrant up`
* Nginx web server: http://192.168.56.10:80
* Prometheus dashboard: http://192.168.56.10:9090
* Dùng query "nginx_connections_accepted" để kiểm tra lượng kết nối

![image](https://github.com/user-attachments/assets/b6d9b0f3-743e-425a-8e6b-5ce1a6866f70)

![image](https://github.com/user-attachments/assets/79eb04ee-5100-449d-9469-22b3d137d12e)




