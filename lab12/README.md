# Lab 12: Cấu hình Terraform Remote State để lưu trữ trạng thái trên S3 bucket
## Thay thế với Azure Blob Storage
* Tạo Azure Storage Account để lưu trạng thái
```
# Đặt các biến thông tin
RESOURCE_GROUP_NAME="terraform-state-rg"
STORAGE_ACCOUNT_NAME="tfstate$(openssl rand -hex 4)"  # Tạo tên ngẫu nhiên để tránh trùng
CONTAINER_NAME="tfstate"

# Tạo Resource Group
az group create --name $RESOURCE_GROUP_NAME --location eastasia

# Tạo Storage Account (phải là unique name)
az storage account create --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP_NAME --location eastasia --sku Standard_LRS --encryption-services blob

# Lấy Storage Account Key
ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query '[0].value' --output tsv)

# Tạo Blob Container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
```
* Cấu hình Terraform để sử dụng Remote State
  * cập nhật backend trong main.tf của Terraform
    ```
    terraform {
      backend "azurerm" {
      resource_group_name   = "terraform-state-rg"    # Resource Group chứa Storage Account
      storage_account_name  = "your-storage-account-name"  # Thay bằng STORAGE_ACCOUNT_NAME đã tạo
      container_name        = "tfstate"              # Tên Blob Container
      key                  = "terraform.tfstate"     # Định danh file state trong container
      }
    }
    ```
* Khởi tạo Terraform với Remote State
>terraform init

* Kiểm tra trạng thái lưu trên Azure
>az storage blob list --container-name tfstate --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY --output table

![image](https://github.com/user-attachments/assets/1e59550e-87c8-4273-acfc-3716b9da5d7c)

![image](https://github.com/user-attachments/assets/f6d11992-22fd-4877-9acb-32522b0714aa)

