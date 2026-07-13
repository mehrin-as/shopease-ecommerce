# ShopEase

A full-stack e-commerce website built with **Python** and **Django**.

ShopEase lets users browse products by category, search items, manage a shopping cart, place orders, and register/login. Admins can manage products, categories, and orders through Django Admin.

---

## Features

- Browse products with **category filter** and **search**
- Product detail pages with description and images
- User **registration** and **login**
- Shopping **cart** (quantity + / −, remove items)
- **Checkout** and order confirmation
- Django **Admin** panel to add/edit products and upload photos
- Categories: Electronics, Women's fashion, Men's fashion, Home and Kitchen, Furniture

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.13+ | Language |
| Django 5.2 | Backend framework |
| SQLite | Database |
| Bootstrap 5 | Frontend styling |
| Pillow | Image handling |

---

## Project Structure

```
ecommerse/
├── manage.py
├── requirements.txt
├── seed_db.py              # Seed categories & products
├── add_product_photos.py   # Optional: download sample photos
├── ecommerse/              # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── store/                  # Main app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── templates/store/
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/shopease.git
cd shopease
```

*(Replace `YOUR_USERNAME` and repo name with yours after you push.)*

### 2. Create a virtual environment (recommended)

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Seed sample data

```bash
python seed_db.py
```

This creates:
- 5 categories
- Sample products
- Admin user: **admin** / **adminpass**

### 6. (Optional) Add product photos

```bash
python add_product_photos.py
```

Or upload images yourself via Admin → Products.

### 7. Start the server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

---

## Important URLs

| Page | URL |
|------|-----|
| Home / Products | http://127.0.0.1:8000/ |
| Login | http://127.0.0.1:8000/login/ |
| Register | http://127.0.0.1:8000/register/ |
| Cart | http://127.0.0.1:8000/cart/ |
| Checkout | http://127.0.0.1:8000/checkout/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## Admin Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `adminpass` |

Use Admin → **Products** to edit names, prices, and upload photos.

---

## How to Use

1. **Register** a new customer account (or use Admin).
2. Browse products and use **Filter** by category or search.
3. Open a product → **Add to Cart** (login required).
4. Update quantities on the cart page, then **Proceed to Checkout**.
5. Click **Place Order** to confirm.

---

## Requirements

See `requirements.txt`:

```
Django>=5.2,<6.0
Pillow>=10.0
```

---

## Notes for Internship / Demo

- This project is for **local development** (`DEBUG = True`).
- Do not commit real production secrets.
- Change the admin password if you deploy publicly.
- SQLite database (`db.sqlite3`) is local and not pushed to GitHub.

---

## Author

Built as an internship project — **ShopEase** e-commerce website using Django.
