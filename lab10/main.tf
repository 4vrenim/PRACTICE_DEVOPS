provider "azurerm" {
  features {}

  subscription_id = "your-subscription-id"  # Thay bằng Subscription ID thực tế của bạn
}

# 1️⃣ Nhập Resource Group có sẵn
data "azurerm_resource_group" "existing_rg" {
  name = "MyExistingResourceGroup"  # Thay bằng tên Resource Group của bạn
}

# 2️⃣ Nhập Virtual Network (VNet) có sẵn
data "azurerm_virtual_network" "existing_vnet" {
  name                = "MyExistingVNet"  # Thay bằng tên VNet của bạn
  resource_group_name = data.azurerm_resource_group.existing_rg.name
}

# 3️⃣ Tạo Subnet trong VNet có sẵn
resource "azurerm_subnet" "subnet" {
  name                 = "MySubnet"
  resource_group_name  = data.azurerm_resource_group.existing_rg.name
  virtual_network_name = data.azurerm_virtual_network.existing_vnet.name
  address_prefixes     = ["10.0.2.0/24"]  # Chỉnh sửa địa chỉ nếu cần
}

# 4️⃣ Tạo Public IP cho NAT Gateway
resource "azurerm_public_ip" "nat_ip" {
  name                = "MyNATPublicIP"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# 5️⃣ Tạo NAT Gateway
resource "azurerm_nat_gateway" "nat_gw" {
  name                = "MyNATGateway"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  sku_name            = "Standard"
}

# 6️⃣ Gán Public IP vào NAT Gateway
resource "azurerm_nat_gateway_public_ip_association" "nat_gw_ip" {
  nat_gateway_id       = azurerm_nat_gateway.nat_gw.id
  public_ip_address_id = azurerm_public_ip.nat_ip.id
}

# 7️⃣ Gán NAT Gateway cho Subnet đã tạo
resource "azurerm_subnet_nat_gateway_association" "subnet_nat" {
  subnet_id      = azurerm_subnet.subnet.id
  nat_gateway_id = azurerm_nat_gateway.nat_gw.id
}
