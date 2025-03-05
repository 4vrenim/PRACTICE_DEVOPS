# Lab 23: Viết một script Python để tự động hóa việc triển khai một ứng dụng web lên một server từ repository Git
## Prerequisite:
* Git Repo chứa app.py, requirements.txt.
* Host cài đặt python, fabric. Host chứa file fabfile.py
* Deploy server cài đặt python, git
## Deploy
* Run on host
`fab deploy`

* Accest http://<deploy_server_ip>:5000/greet/<yourname>
![image](https://github.com/user-attachments/assets/3a4c7652-ba34-4f84-bf9b-507c5b579ebe)
