# Lab 14: Tạo một Jenkins pipeline để thực hiện các bước xây dựng, kiểm tra và triển khai ứng dụng Docker

* Cài đặt sshpass
* Cài đặt Java
```
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
```
* Cài đặt Jenkin
```
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```
* Chạy Jenkin
```
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```
* Vào http://<IP>:8080 để truy cập
* Tạo 1 pipeline project và vào phần Configure -> Pipeline để tạo script
```
pipeline {
    agent any

    environment {
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'your-dockerhub-name/your-app'
        IMAGE_TAG = 'latest'
        DEPLOY_SERVER = 'IP-Server-trien_khai'
    }
   
    
    stages {
    
        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/4vrenim/practice_jenkin.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    sh 'docker run --rm $IMAGE_NAME:$IMAGE_TAG &'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'ssh-deploy', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS')]) {
                        sh "sshpass -p \"$SSH_PASS\" ssh -o StrictHostKeyChecking=no $SSH_USER@$DEPLOY_SERVER 'docker pull $IMAGE_NAME:$IMAGE_TAG && docker run -d --restart=always -p 5050:5050 $IMAGE_NAME:$IMAGE_TAG'"
                    }
                }
            }
        }
    }
}
```

![image](https://github.com/user-attachments/assets/bda9702b-69a5-4a64-9385-b3db4440cf42)

* Vào Dashboard -> Manage Jenkins -> Credentials tạo 2 credentials : docker-hub-credentials (thông tin truy cập Dockerhub) và ssh-deploy (thông tin user deploy để ssh)
![image](https://github.com/user-attachments/assets/6bcf17f7-3e20-41b8-867d-c6500520646a)

* Chạy Build Now
![image](https://github.com/user-attachments/assets/0d5bebf5-51a0-4ef0-b887-40fe4e32892c)

![image](https://github.com/user-attachments/assets/e2e98663-984f-4c4d-ae87-9d722c4e5b4d)



