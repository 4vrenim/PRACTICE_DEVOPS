# Lab 18: Cấu hình Horizontal Pod Autoscaler (HPA) cho ứng dụng trên Kubernetes để tự động mở rộng số lượng Pod dựa trên tải công việc
* Cài đặt Metrics Server để thu thập dữ liệu CPU/Memory
>minikube addons enable metrics-server

* Kiểm tra xem Metrics Server đã chạy chưa
>kubectl get deployment metrics-server -n kube-system

![image](https://github.com/user-attachments/assets/bcae0a61-2f87-4ee5-ab93-1cb7e820a8cb)

* Cập nhật file deployment.yaml để sử dụng Resource Limits
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: my-flask-app
        ports:
        - containerPort: 5000
        resources:
          requests:
            cpu: "250m"
          limits:
            cpu: "500m"
```

* Áp dụng thay đổi
>kubectl apply -f deployment.yaml

* Tạo hpa.yaml để Tự Động Mở Rộng Pods
```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-deployment
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 30  # Mở rộng khi CPU vượt 30%
```

* Áp dụng và kiểm tra
>kubectl apply -f hpa.yaml  
>kubectl get hpa
---
## Tạo Tải CPU và kiểm tra
* Tạo pod busybox
>kubectl run -i --tty load-generator --image=busybox -- /bin/sh

* Trong terminal BusyBox, chạy vòng lặp request
>while true; do wget -q -O- http://flask-service.default.svc.cluster.local/; done

* Theo dõi HPA xem số lượng pod tăng khi cpu vượt ngưỡng
>kubectl get hpa flask-hpa --watch

![image](https://github.com/user-attachments/assets/9366a073-4ea0-402e-aa81-c947453d47df)
