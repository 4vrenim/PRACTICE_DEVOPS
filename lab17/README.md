# Lab 17: Viết file YAML để định nghĩa một Deployment và Service cho ứng dụng web trên Kubernetes
* Tạo file deployment.yaml
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
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
```

* Tạo file service.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: NodePort
```

* Deploy Ứng Dụng Lên Kubernetes
```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
