import os
import django
from django.core.files.base import ContentFile
from io import BytesIO

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerse.settings')
django.setup()

from store.models import Category, Product
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_image(filename, text, color):
    img = Image.new('RGB', (400, 300), color=color)
    draw = ImageDraw.Draw(img)
    # Simple draw text
    draw.text((20, 140), text, fill=(255, 255, 255))
    
    # Save to media/products/
    os.makedirs('media/products', exist_ok=True)
    filepath = os.path.join('media', 'products', filename)
    img.save(filepath, 'PNG')
    return f'products/{filename}'

def seed():
    print("Clearing old data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print("Seeding Categories...")
    cats = {
        1: Category.objects.create(id=1, name="Electronics"),
        2: Category.objects.create(id=2, name="Women's fashion"),
        3: Category.objects.create(id=3, name="Men's fashion"),
        4: Category.objects.create(id=4, name="Home and Kitchen"),
        5: Category.objects.create(id=5, name="Furniture"),
    }
    
    print("Generating images and seeding products...")
    
    products_data = [
        # Furniture
        {
            "name": "SleepyCat Ultima CoolTEC Fabric 8 Inch Thickness King Size Mattress 78x72x8 Inches",
            "category": cats[5],
            "price": 25600.00,
            "stock": 5,
            "online_exclusive": False,
            "description": "Ultima CoolTEC Mattress by SleepyCat ensures high comfort and cooling for a deeply restorative rest. 8-inch thickness, engineered support, king size 78x72x8 inches, breathable memory foam.",
            "img_name": "sleepycat_mattress.png",
            "color": "#3f51b5",
            "text": "SleepyCat Mattress"
        },
        {
            "name": "Royaloak Brown Textured Shoe Rack 2 Door",
            "category": cats[5],
            "price": 4500.00,
            "stock": 8,
            "online_exclusive": True,
            "description": "Modern 2-door brown textured shoe rack by Royaloak. Durable, spacious, and compact with styled patterns suitable for entrances and home spaces. Online exclusive item.",
            "img_name": "royaloak_shoe_rack.png",
            "color": "#795548",
            "text": "Royaloak Shoe Rack"
        },
        {
            "name": "Curio Centre Round Cotton Home Swing",
            "category": cats[5],
            "price": 7546.00,
            "stock": 3,
            "online_exclusive": False,
            "description": "About this item Can be used as a cradle, a swing to hang outside, rest under the sunset, relax poolside, lounge on the deck. Made of cotton, Capacity: 120 Kgs, Dimension: 67cm x 42cm x 145cm (Height of chair, without rope is 45cm) Can be used at home, bedroom, sunroom, kid's room, living room, garden, yard, patio, deck, and garden. Portable & relocates anywhere, Sets-up in seconds, Lightweight and easy to store and carry. Easy to hang from ceiling, tree, or any sturdy overhang that can support your weight.",
            "img_name": "curio_swing.png",
            "color": "#9e9e9e",
            "text": "Curio swing"
        },
        {
            "name": "Nilkamal Freedom Big FMM Plastic Cabinet",
            "category": cats[5],
            "price": 7890.00,
            "stock": 6,
            "online_exclusive": False,
            "description": "Nilkamal Freedom Big FMM Plastic Cabinet offers spacious storage with durable plastic construction. Ideal for home organization, multipurpose storage for clothes, books, and household items.",
            "img_name": "nilkamal_cabinet.png",
            "color": "#607d8b",
            "text": "Nilkamal Cabinet"
        },
        # Women's fashion
        {
            "name": "Women Anarkali Kurta",
            "category": cats[2],
            "price": 999.00,
            "stock": 10,
            "online_exclusive": False,
            "description": "Traditional cotton Anarkali Kurta for women. Highlights beautiful patterns, elegant flair, and classic round neck styling. Suitable for casual wear as well as formal ceremonies.",
            "img_name": "women_anarkali_kurta.png",
            "color": "#e91e63",
            "text": "Women Anarkali Kurta"
        },
        {
            "name": "Floral Yoke Design Thread Work Anarkali Kurta With Palazzos & Dupatta",
            "category": cats[2],
            "price": 1097.00,
            "stock": 4,
            "online_exclusive": False,
            "description": "Beautiful floral yoke design thread work Anarkali Kurta complete set with matching palazzos and a lightweight dupatta. Elevates ethnic elegance with custom prints.",
            "img_name": "floral_anarkali_set.png",
            "color": "#9c27b0",
            "text": "Floral Anarkali set"
        },
        {
            "name": "Floral Printed Flared Sleeve Cotton Fit & Flare Dress",
            "category": cats[2],
            "price": 999.00,
            "stock": 6,
            "online_exclusive": False,
            "description": "Delightful floral printed fit & flare dress for women. Features short flared sleeves, premium cotton fabric, and comfortable styling suited for summer outings.",
            "img_name": "floral_flare_dress.png",
            "color": "#ff4081",
            "text": "Floral Flare Dress"
        },
        {
            "name": "Black & Maroon Kalamkari Hand Block Print Ethnic Sustainable Maxi Pure Cotton Skirt with Gathers",
            "category": cats[2],
            "price": 474.00,
            "stock": 7,
            "online_exclusive": False,
            "description": "Artisanal Kalamkari hand block print maxi skirt. Cotton fabric with gathers. Traditional border in deep maroon contrast on premium black base. Sustainable and stylish.",
            "img_name": "kalamkari_skirt.png",
            "color": "#212121",
            "text": "Kalamkari Skirt"
        },
        # Men's fashion
        {
            "name": "Washed Cotton Denim Jacket",
            "category": cats[3],
            "price": 1396.00,
            "stock": 8,
            "online_exclusive": False,
            "description": "Washed cotton denim jacket for men. Features classic collar, dual chest pockets, button closures, and premium comfort build. An excellent layer for casual streetwear.",
            "img_name": "washed_denim_jacket.png",
            "color": "#3f51b5",
            "text": "Washed Denim Jacket"
        },
        {
            "name": "Men Cotton Striped Casual Shirt",
            "category": cats[3],
            "price": 743.00,
            "stock": 12,
            "online_exclusive": False,
            "description": "Striped casual shirt for men. Crafted from lightweight, breathable cotton. Vertical stripes design styled with standard collar and full-button closure.",
            "img_name": "striped_casual_shirt.png",
            "color": "#2196f3",
            "text": "Striped Casual Shirt"
        },
        # Electronics
        {
            "name": "Black Poco m6 5g 6-128gb",
            "category": cats[1],
            "price": 20000.00,
            "stock": 10,
            "online_exclusive": False,
            "description": "Black Poco M6 5G mobile. Comes with 6GB RAM and 128GB internal storage. Smooth performance, vibrant display, fast charging support, and sleek design.",
            "img_name": "poco_m6.png",
            "color": "#4caf50",
            "text": "Poco M6 5G Mobile"
        },
        {
            "name": "TCL 139 cm (55 inches) 4K Ultra HD Smart QLED Google TV 55C61B (Black)",
            "category": cats[1],
            "price": 40560.00,
            "stock": 4,
            "online_exclusive": False,
            "description": "TCL 4K QLED Android Smart TV. High resolution, Dolby Audio integration, immersive display panel, hands-free voice controls, and smart hub functionalities.",
            "img_name": "tcl_tv.png",
            "color": "#607d8b",
            "text": "TCL 55-inch 4K QLED TV"
        },
        {
            "name": "Portronics Key11 Combo Rechargeable Wireless Keyboard and Mouse Set, Bluetooth 5.3&2.4GHz Wireless,",
            "category": cats[1],
            "price": 1699.00,
            "stock": 15,
            "online_exclusive": False,
            "description": "Portronics Key11 combo rechargeable set containing high-precision wireless keyboard and mouse. Bluetooth 5.3 + 2.4GHz dual mode connectivity, silent keypress.",
            "img_name": "portronics_combo.png",
            "color": "#9e9e9e",
            "text": "Portronics Keyboard & Mouse"
        }
    ]
    
    for info in products_data:
        img_path = create_placeholder_image(info["img_name"], info["text"], info["color"])
        Product.objects.create(
            name=info["name"],
            category=info["category"],
            price=info["price"],
            stock=info["stock"],
            online_exclusive=info["online_exclusive"],
            description=info["description"],
            image=img_path
        )
        print(f"Created Product: {info['name']}")

    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@shopease.com', 'adminpass')
        print("Created Superuser 'admin' with password 'adminpass'")
        
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
