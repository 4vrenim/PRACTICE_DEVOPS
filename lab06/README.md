# Lab 6: Tạo một Docker Swarm cluster với ít nhất 3 nodes và triển khai ứng dụng web đã xây dựng

* Khởi tạo Docker Swarm Cluster
Trên Node 1 (Manager Node)
>docker swarm init --advertise-addr <MANAGER_IP>

![image](https://github.com/user-attachments/assets/8f1dfa2c-29a6-487a-b0bd-f5fed7e30231)

* Trên Node 2 và Node 3 (Worker Nodes) sử dụng command từ Manager Node để join
![image](https://github.com/user-attachments/assets/f66ff787-cc5e-45cf-8a9f-fbcf94cc4c9d)

* Kiểm tra trạng thái của Swarm
>docker node ls

![image](https://github.com/user-attachments/assets/1b8c3106-1714-4b78-96fe-1dc41950081c)

* Tạo Docker Compose cho Swarm và triển khai ứng dụng lên Docker Swarm
>docker stack deploy -c docker-compose.yml flask-app

* Kiểm tra trạng thái của dịch vụ
>docker stack services flask-app

![image](https://github.com/user-attachments/assets/2c683317-dae3-4729-8ee0-5ba11fc8269a)

* Có thể truy cập web từ Node 2 và 3

![image](https://github.com/user-attachments/assets/0e21555a-0169-4695-b33e-03de8be6d99c)

![image](https://github.com/user-attachments/assets/2ac500b5-15e4-4e65-b430-901b43c147b1)
