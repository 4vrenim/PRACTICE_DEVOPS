# Cấu hình S3 bucket để lưu trữ bản sao lưu của ứng dụng và thiết lập Lifecycle Policy để tự động xóa các bản sao lưu cũ sau 30 ngày
## Thay thế bằng Azure Blob Storage
* Tạo Storage Account
```
az storage account create --name mybackupstorage \
    --resource-group MyResourceGroup \
    --location eastus \
    --sku Standard_LRS \
    --kind StorageV2
```
![image](https://github.com/user-attachments/assets/46241bf5-4009-498e-9724-53b585b9cdf8)

* Tạo Container trong Storage Account
```
az storage container create --name backups \
    --account-name mybackupstorage \
    --public-access off
```
![image](https://github.com/user-attachments/assets/09d4ac5a-833e-483d-9ab2-2989bd9184c7)

* Tạo file lifecycle-policy.json và update Lifecycle Policy để xóa file sau 30 ngày
```
az storage account management-policy create \
    --account-name mybackupstorage \
    --policy @policy.json \
    --resource-group MyResourceGroup
```
* Sao lưu dữ liệu lên Azure Blob Storage
```
az storage blob upload \
    --account-name mybackupstorage \
    --container-name backups \
    --name backup-$(date +%F).sql \
    --file /path/to/backup.sql
```
![image](https://github.com/user-attachments/assets/8fc838d3-5932-47a3-a236-f002dc0c18b9)

* Tự động hóa sao lưu với cron lúc 2h sáng
>crontab -e

>0 2 * * * az storage blob upload --account-name mybackupstorage --container-name backups --name backup-$(date +\%F).sql --file /path/to/backup.sql
  
