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
