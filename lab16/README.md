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
* Khởi động Minikube và tạo cluster
>minikube start

![image](https://github.com/user-attachments/assets/7f9a18d2-1fb7-48c7-ad72-c7b42bdce651)

* Kiểm tra cluster
>kubectl get nodes

![image](https://github.com/user-attachments/assets/fb39bcae-7603-48d9-9f31-0a7f73655922)
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

