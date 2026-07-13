"""Download real product-style photos and attach them to Products."""
import os
import urllib.request

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerse.settings')
import django
django.setup()

from django.core.files import File
from store.models import Product

# Free Unsplash images (direct CDN URLs) matched to product type
PRODUCT_IMAGES = {
    'SleepyCat': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80',  # mattress/bed
    'Royaloak': 'https://images.unsplash.com/photo-1595428774223-ef526ba924d9?w=800&q=80',  # wood furniture/cabinet
    'Curio': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80',  # hanging/living room
    'Nilkamal': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',  # cabinet/sofa furniture
    'Women Anarkali': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&q=80',  # ethnic wear
    'Floral Yoke': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80',  # purple dress
    'Floral Printed': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&q=80',  # floral dress
    'Kalamkari': 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=800&q=80',  # skirt/fashion
    'Denim Jacket': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800&q=80',  # denim jacket
    'Striped Casual': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&q=80',  # striped shirt
    'Poco': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80',  # smartphone
    'TCL': 'https://images.unsplash.com/photo-1593359677879-a4b92e8b6170?w=800&q=80',  # TV
    'Portronics': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',  # keyboard
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

os.makedirs('media/products', exist_ok=True)


def download(url, filepath):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp, open(filepath, 'wb') as out:
        out.write(resp.read())


def main():
    products = list(Product.objects.all())
    updated = 0

    for product in products:
        matched_key = None
        matched_url = None
        for key, url in PRODUCT_IMAGES.items():
            if key.lower() in product.name.lower():
                matched_key = key
                matched_url = url
                break

        if not matched_url:
            print(f'Skip (no match): {product.name[:50]}')
            continue

        filename = f'product_{product.id}_{matched_key.replace(" ", "_").lower()}.jpg'
        filepath = os.path.join('media', 'products', filename)

        try:
            print(f'Downloading for: {product.name[:50]}...')
            download(matched_url, filepath)
            with open(filepath, 'rb') as f:
                product.image.save(filename, File(f), save=True)
            updated += 1
            print(f'  OK -> {filename}')
        except Exception as e:
            print(f'  FAILED: {e}')

    print(f'\nDone. Updated {updated}/{len(products)} products.')


if __name__ == '__main__':
    main()
