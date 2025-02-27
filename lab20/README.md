# Lab 20: Sử dụng Vagrant để dựng lên một multi-machine environment với một máy ảo chạy ứng dụng web và một máy ảo khác chạy cơ sở dữ liệu

* Cập nhật file Vagrantfile
```
Vagrant.configure("2") do |config|
  
  # Cấu hình cho máy ảo chạy ứng dụng web (Web server)
  config.vm.define "web" do |web|
    
    # Sử dụng box Ubuntu 18.04 (bionic64)
    web.vm.box = "ubuntu/bionic64"
    
    # Đặt hostname cho máy ảo này là "webserver"
    web.vm.hostname = "webserver"
    
    # Cấu hình mạng nội bộ với địa chỉ IP tĩnh 192.168.56.10
    web.vm.network "private_network", ip: "192.168.56.10"

    # Provisioning (cài đặt phần mềm) cho máy ảo "web"
    web.vm.provision "shell", inline: <<-SHELL
      # Cập nhật danh sách gói phần mềm
      apt-get update
      
      # Cài đặt Nginx
      apt-get install -y nginx
      
      # Khởi động dịch vụ Nginx
      systemctl start nginx
      
      # Đảm bảo Nginx tự khởi động khi máy ảo khởi động lại
      systemctl enable nginx
    SHELL
  end

  # Cấu hình cho máy ảo chạy cơ sở dữ liệu (Database server)
  config.vm.define "db" do |db|
    
    # Sử dụng box Ubuntu 18.04 (bionic64)
    db.vm.box = "ubuntu/bionic64"
    
    # Đặt hostname cho máy ảo này là "dbserver"
    db.vm.hostname = "dbserver"
    
    # Cấu hình mạng nội bộ với địa chỉ IP tĩnh 192.168.56.11
    db.vm.network "private_network", ip: "192.168.56.11"

    # Provisioning (cài đặt phần mềm) cho máy ảo "db"
    db.vm.provision "shell", inline: <<-SHELL
      # Cập nhật danh sách gói phần mềm
      apt-get update
      
      # Cài đặt MySQL server
      apt-get install -y mysql-server
      
      # Khởi động dịch vụ MySQL
      systemctl start mysql
      
      # Đảm bảo MySQL tự khởi động khi máy ảo khởi động lại
      systemctl enable mysql

      # Cài đặt cơ sở dữ liệu và người dùng MySQL
      mysql -e "CREATE DATABASE mydb;"
      mysql -e "CREATE USER 'user'@'%' IDENTIFIED BY 'password';"
      mysql -e "GRANT ALL PRIVILEGES ON mydb.* TO 'user'@'%';"
      mysql -e "FLUSH PRIVILEGES;"
    SHELL
  end

end
```
* Khởi tạo vm
>vagrant up

* SSH vào server web, ping server db và truy cập MySQL server
![image](https://github.com/user-attachments/assets/401cf86c-df7f-4d16-b6ae-0156e7dbb03f)

* Truy cập web bằng trình duyệt
![image](https://github.com/user-attachments/assets/3fc3fc0e-ce7d-4441-868d-1f8eebed3745)

* Dừng và xóa các vm
>vagrant halt  
>vagrant destroy -f


