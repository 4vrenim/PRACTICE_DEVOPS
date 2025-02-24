# Lab 15: Sử dụng GitHub Actions để thiết lập một workflow CI/CD cho dự án Python, bao gồm bước kiểm tra mã nguồn với pytest
* Cấu trúc project
```
simple-python-project/
├── .github/
│   └── workflows/
│       └── python-ci.yml
├── app.py
├── test_app.py
├── requirements.txt
└── README.md
```

* Description
```
# Simple Python Project

This is a simple Python project that adds two numbers and includes a test suite using `pytest`.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
```

* Sau khi push lên Github action sẽ tự chạy
![image](https://github.com/user-attachments/assets/d048464a-81e6-4905-a40f-5c6c3c5a4f7e)
