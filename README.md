
# 🛍️ **Drobe — Single-Seller Clothing Store (Django)**

A modern single-seller clothing store built with **Django**, featuring product management, cart functionality, user accounts, and a clean modular structure.

---

## **Features**

### 👨‍💼 Seller (Admin)

* Add new clothing products
* Edit and delete products
* Manage product images
* Manage categories/brands
* View and fulfill customer orders
* Offer discounts 

### 🛒 Users

* Browse products by category/brand
* Add items to cart
* Update or remove cart items
* Create an account / log in
* Proceed to checkout 
* Responsive pages 


## 🔧 **Installation & Setup**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/helviz/drobe.git
cd drobe
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 5️⃣ Create Superuser (Seller Account)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

Visit: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---


