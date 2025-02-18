# Lab 10: Viết file Terraform để tạo một VPC, Subnet, và Internet Gateway trên AWS
## Thay thế với Azure Virtual Network (VNet), Subnet, và NAT Gateway

* Tạo file cấu hình main.tf bao gồm các thành phần bên dưới
* Cấu hình Provider cho Azure
```
provider "azurerm" {
  features {}

  subscription_id = "your-subscription-id"  # Thay bằng Subscription ID thực tế của bạn
}
```
* Sử dụng Resource Group sẵn có
```
# Nhập Resource Group có sẵn
data "azurerm_resource_group" "existing_rg" {
  name = "MyExistingResourceGroup"  # Thay bằng tên Resource Group của bạn
}
```
* Sử dụng VNET sẵn có
```
# Nhập Virtual Network (VNet) có sẵn
data "azurerm_virtual_network" "existing_vnet" {
  name                = "MyExistingVNet"  # Thay bằng tên VNet của bạn
  resource_group_name = data.azurerm_resource_group.existing_rg.name
}
```
* Tạo Subnet
```
# Tạo Subnet trong VNet có sẵn
resource "azurerm_subnet" "subnet" {
  name                 = "MySubnet"
  resource_group_name  = data.azurerm_resource_group.existing_rg.name
  virtual_network_name = data.azurerm_virtual_network.existing_vnet.name
  address_prefixes     = ["10.0.2.0/24"]  # Chỉnh sửa địa chỉ nếu cần
}
```
* Tạo NAT Gateway và liên kết với một Public IP
```
# Tạo Public IP cho NAT Gateway
resource "azurerm_public_ip" "nat_ip" {
  name                = "MyNATPublicIP"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Tạo NAT Gateway
resource "azurerm_nat_gateway" "nat_gw" {
  name                = "MyNATGateway"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  sku_name            = "Standard"
}

# Gán Public IP vào NAT Gateway
resource "azurerm_nat_gateway_public_ip_association" "nat_gw_ip" {
  nat_gateway_id       = azurerm_nat_gateway.nat_gw.id
  public_ip_address_id = azurerm_public_ip.nat_ip.id
}
```
* Liên kết NAT Gateway với Subnet
```
# Gán NAT Gateway cho Subnet đã tạo
resource "azurerm_subnet_nat_gateway_association" "subnet_nat" {
  subnet_id      = azurerm_subnet.subnet.id
  nat_gateway_id = azurerm_nat_gateway.nat_gw.id
}
```
-----
* Khởi tạo Terraform
>terraform init

![image](https://github.com/user-attachments/assets/a928c48d-5e42-44c8-8591-729c98bfd7f2)

* Kiểm tra cấu hình trước khi chạy
>terraform plan

![image](https://github.com/user-attachments/assets/01a65fb0-07c8-4d78-943b-b123af05a804)

* Triển khai tài nguyên lên Azure
>terraform apply -auto-approve

![image](https://github.com/user-attachments/assets/6b318198-24fc-4f94-b2fe-4bb3aff77171)

* Kiểm tra trên portal
![image](https://github.com/user-attachments/assets/5a0c0425-cf50-48dd-aadc-610fd53c7404)

* Xóa tài nguyên khi không cần thiết
>terraform destroy -auto-approve







