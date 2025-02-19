# Lab 18: Cấu hình Horizontal Pod Autoscaler (HPA) cho ứng dụng trên Kubernetes để tự động mở rộng số lượng Pod dựa trên tải công việc
* Cài đặt Metrics Server để thu thập dữ liệu CPU/Memory
>kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

* Kiểm tra xem Metrics Server đã chạy chưa
>kubectl get deployment metrics-server -n kube-system

![image](https://github.com/user-attachments/assets/5a9ed59c-e382-40cb-aecc-449e3c26799b)

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
        averageUtilization: 50  # Mở rộng khi CPU vượt 50%
```

* Áp dụng và kiểm tra
>kubectl apply -f hpa.yaml  
>kubectl get hpa

