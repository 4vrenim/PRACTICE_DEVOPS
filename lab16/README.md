# Lab 16: Cài đặt một Kubernetes cluster sử dụng Minikube và triển khai một ứng dụng web đơn giản lên cluster.
* Cài Minikube
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
* Cài Kubectl
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```
* Khởi động Minikube và tạo cluster 3 node
>minikube start --nodes 3 -p minikube-demo --driver=docker

![image](https://github.com/user-attachments/assets/b3fed113-bbae-40ab-9606-b04e3afa9754)

* Kiểm tra cluster
>kubectl get nodes

![image](https://github.com/user-attachments/assets/76b24fd7-3958-4d00-b631-6a488bc420fe)
---
## Triển khai Ứng dụng Web đơn giản
Sử dụng một ứng dụng Flask nhỏ chạy trong Docker
* Dockerfile
```
FROM python:3.9
WORKDIR /app
COPY app.py .
RUN pip install flask
CMD ["python", "app.py"]
```
* app.py
```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Kubernetes from Minikube!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
* Build Docker image
```
eval $(minikube docker-env)  # Sử dụng Docker của Minikube
docker build -t my-flask-app .
```
* Tạo pod
>kubectl run "example pod" --image=my-flask-app --image-pull-policy Never

* Kiểm tra pod
>kubectl get pod "example pod" -o wide

![image](https://github.com/user-attachments/assets/f0f10839-50f8-4635-a391-8ccbb05a3052)

