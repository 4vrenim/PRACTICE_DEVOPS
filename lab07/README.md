# Bài Lab 7: Sử dụng AWS CLI để tạo một EC2 instance với cấu hình định trước
## Sử dụng Azure thay thế
* Đăng nhập vào Azure
>az login

![image](https://github.com/user-attachments/assets/dc5a0ff6-a53b-4af6-8b13-bef57f263c34)

* Nếu có nhiều subscription, hãy chọn một bằng lệnh
>az account list --output table  
>az account set --subscription "SUBSCRIPTION_ID"

* Tạo nhóm tài nguyên nếu chưa có
>az group create --name MyResourceGroup --location eastus

* Tạo VM
```
az vm create \
  --resource-group MyResourceGroup \
  --name MyVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B1s
```
![image](https://github.com/user-attachments/assets/3e95caa1-9acb-4c79-9d56-907fcbfb120d)
