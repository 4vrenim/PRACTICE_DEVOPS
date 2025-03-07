from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# File lưu danh sách sản phẩm
PRODUCTS_FILE = "products.json"

# Hàm đọc dữ liệu từ file
def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    return []

# Hàm lưu dữ liệu vào file
def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

# Danh sách sản phẩm sẽ được tải từ file khi server khởi động
products = load_products()

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = {"id": len(products) + 1, "name": data["name"]}
    products.append(new_product)
    save_products(products)  # Lưu lại vào file
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
