# Lab 19: Tạo một Vagrantfile để dựng lên một môi trường ảo hóa với Ubuntu và cài đặt Docker trong máy ảo này

* Cài đặt Vagrant và virtualbox
* Chạy lệnh 'vagrant init' để tạo Vagrantfile
* Update Vagrantfile
```
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64" # Sử dụng Ubuntu 22.04

  config.vm.network "private_network", type: "dhcp",
    virtualbox__intnet: "mynetwork"
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
  end
  
  config.vm.provision "shell", inline: <<~SHELL
  # Cập nhật danh sách package
  sudo apt-get update -y
  sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg

  # Thêm khóa GPG mới của Docker
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

  # Thêm repository Docker vào danh sách nguồn APT
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  # Cập nhật danh sách package sau khi thêm repository
  sudo apt-get update -y

  # Cài đặt Docker
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io

  # Thêm user vagrant vào nhóm docker để có thể chạy docker mà không cần sudo
  sudo usermod -aG docker vagrant
SHELL

end
```
* Chạy lệnh khởi tạo và ssh vào kiểm tra docker đã cài đặt
>vagrant up  
>vagrant ssh  
>docker --version

![image](https://github.com/user-attachments/assets/b5974fc9-c90d-48d2-a4a8-295c7e2e123f)

![image](https://github.com/user-attachments/assets/9359a478-9a70-42f6-972a-ca63097c2559)
