# Lab 24: Tạo một ứng dụng Python Flask đơn giản với REST API và viết unit tests cho các endpoint

* Cài đặt Python và pip
```
sudo apt update -y
sudo apt install -y python3 python3-venv python3-pip
```
* Cài đặt Flask
>pip install flask


* Khởi động server dưới nền
>nohup python3 server.py > server.log 2>&1 &

* Thêm sản phẩm
```
curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "Laptop Dell", "price": 1200, "quantity": 10}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "MacBook Pro", "price": 2000, "quantity": 5}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "iPhone 15", "price": 999, "quantity": 15}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "Samsung Galaxy S23", "price": 850, "quantity": 20}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "Sony Headphones", "price": 150, "quantity": 30}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "Logitech Mouse", "price": 50, "quantity": 100}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "Mechanical Keyboard", "price": 120, "quantity": 50}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "Gaming Chair", "price": 300, "quantity": 25}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "External SSD 1TB", "price": 180, "quantity": 40}'

curl -X POST "http://192.168.56.10:5000/products" -H "Content-Type: application/json" -d '{"name": "4K Monitor", "price": 500, "quantity": 12}'
```

* Lấy danh sách sản phẩm
>curl -X GET "http://192.168.56.10:5000/products"

![image](https://github.com/user-attachments/assets/39db54d2-668b-481f-a954-8794d7043c84)

![image](https://github.com/user-attachments/assets/f3e5e3e1-bc12-4646-83a5-ae1c34bea083)

* Chạy test
>python3 test_server.py


![image](https://github.com/user-attachments/assets/cd052161-1c04-4e2b-9745-2393ba2704dc)


