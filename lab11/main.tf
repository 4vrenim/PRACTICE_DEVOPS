provider "azurerm" {
  features {}

  subscription_id = "your-subscription-id"  # Thay bằng Subscription ID thực tế của bạn
}

# 1. Tạo Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "TerraGroup"
  location = "East Asia"
}

# 2. Tạo Virtual Network và Subnet
resource "azurerm_virtual_network" "vnet" {
  name                = "myVNet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "mySubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# 3. Tạo Public IP cho Load Balancer
resource "azurerm_public_ip" "lb_pip" {
  name                = "myPublicIP"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# 4. Tạo Load Balancer
resource "azurerm_lb" "lb" {
  name                = "myLoadBalancer"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "PublicIP"
    public_ip_address_id = azurerm_public_ip.lb_pip.id
  }
}


# Load Balancer Backend Pool
resource "azurerm_lb_backend_address_pool" "lb_backend" {
  name            = "backendPool"
  loadbalancer_id = azurerm_lb.lb.id
}

# Load Balancer Rule
resource "azurerm_lb_rule" "lb_rule" {
  name                           = "http-rule"
  loadbalancer_id                = azurerm_lb.lb.id
  frontend_ip_configuration_name = "PublicIP"
  backend_address_pool_ids       = azurerm_lb_backend_address_pool.lb_backend.id
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  enable_floating_ip             = false
  idle_timeout_in_minutes        = 5
  load_distribution              = "Default"
}

# Tạo Virtual Machine Scale Set (VMSS)
resource "azurerm_monitor_autoscale_setting" "autoscale" {
  name                = "autoscale-vmss"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  target_resource_id  = azurerm_linux_virtual_machine_scale_set.vmss.id

  profile {
    name = "default"

    capacity {
      default = 2
      minimum = 1
      maximum = 5
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_namespace   = "Microsoft.Compute/virtualMachineScaleSets"
        time_grain         = "PT1M"
        statistic          = "Average"
        operator           = "GreaterThan"
        threshold          = 75
        time_aggregation   = "Average"
        time_window        = "PT5M"
      }

      scale_action {
        direction  = "Increase"
        type       = "ChangeCount"
        value      = 1
        cooldown   = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_namespace   = "Microsoft.Compute/virtualMachineScaleSets"
        time_grain         = "PT1M"
        statistic          = "Average"
        operator           = "LessThan"
        threshold          = 25
        time_aggregation   = "Average"
        time_window        = "PT5M"
      }

      scale_action {
        direction  = "Decrease"
        type       = "ChangeCount"
        value      = 1
        cooldown   = "PT5M"
      }
    }
  }
}
