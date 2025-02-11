# Bài Lab 8: Thiết lập Auto Scaling Group trên AWS để tự động mở rộng hoặc thu hẹp số lượng EC2 instances dựa trên tải công việc.
## Thay thế với Azure và Virtual Machine Scale Set (VMSS)

* Tạo một nhóm VM Scale Set
```
az vmss create \
  --resource-group MyResourceGroup \
  --name MyScaleSet \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --instance-count 2 \
  --vm-sku Standard_B1s \
  --upgrade-policy-mode automatic \
  --load-balancer ""
```
![image](https://github.com/user-attachments/assets/bc3a611b-408a-494a-ac4b-9f7246d0ad6c)
![image](https://github.com/user-attachments/assets/a8cc7de9-1473-4990-83df-a17e086df0ff)

* Cấu hình Autoscale dựa trên CPU Usage
```
az monitor autoscale create \
  --resource-group MyResourceGroup \
  --name MyAutoscaleRule \
  --resource MyScaleSet \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --min-count 2 \
  --max-count 5 \
  --count 2
```
![image](https://github.com/user-attachments/assets/53d8f96b-0084-4fe8-90ef-773708bbb284)

* Thêm quy tắc mở rộng khi CPU > 50% sau 1 phút
```
az monitor autoscale rule create \
  --resource-group MyResourceGroup \
  --autoscale-name MyAutoscaleRule \
  --condition "Percentage CPU > 50 avg 1m" \
  --scale out 1
```
* Thêm quy tắc giảm tải khi CPU < 30% sau 2 phút
```
az monitor autoscale rule create \
  --resource-group MyResourceGroup \
  --autoscale-name MyAutoscaleRule \
  --condition "Percentage CPU < 30 avg 2m" \
  --scale in 1
```
![image](https://github.com/user-attachments/assets/56f5d857-f6ec-4a00-b6c0-266d254a2e7a)

* Kiểm tra cấu hình Autoscale
>az monitor autoscale show --resource-group MyResourceGroup --name MyAutoscaleRule

## TEST
* Kiểm tra trạng thái VM Scale Set
>az vmss list-instances --resource-group MyResourceGroup --name MyScaleSet --output table

![image](https://github.com/user-attachments/assets/b67d8912-f021-427d-b770-e522c1be9c0d)
![image](https://github.com/user-attachments/assets/66ced30c-e959-4e54-bf38-293242e86466)

* Kết nối SSH và tạo tải CPU cao trên một VM
>sudo apt update && sudo apt install -y stress  
>stress --cpu 4 --timeout 600

* Kiểm tra số lượng VM sau 1 phút
![image](https://github.com/user-attachments/assets/8db4c181-5cbe-4fdc-8afb-a4284eaf1989)
![image](https://github.com/user-attachments/assets/a8c4417d-18bc-4baf-9ccd-c780c5407e3a)




