# Lab 13: Thiết lập một pipeline CI/CD trên GitLab để tự động xây dựng, kiểm tra và triển khai một ứng dụng web
## Triển khai 1 Pipeline deploy web nodejs đơn giản
* Build: Cài module mới hoặc update file index.js
* Test: Truy cập web xem nội dung
* Deploy: Deploy code lên gitlab
---
1. Tạo project lab13 trên gitlab
2. Tạo gitlab runner với tag lab13
3. Install gitlab runner trên vm host
4. Tạo service runner trên vm host với Token lấy từ step 2
5. Clone repository từ gitlab về host
6. Trên vm host tạo file index.js với nội dung
```
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
```
7. Trên vm host install nodejs và thực thi lệnh ' npm init --y'

![image](https://github.com/user-attachments/assets/cb5fb765-e5c2-480d-994d-6b2284bac2b2)

![image](https://github.com/user-attachments/assets/7f6b8de9-8ad2-4999-b16d-ad3504581ea4)

![image](https://github.com/user-attachments/assets/89085d3e-a1c3-45a4-a3a2-919ef2aa625d)

![image](https://github.com/user-attachments/assets/ca1c3496-28c3-481a-b3f1-2afc90363f44)

