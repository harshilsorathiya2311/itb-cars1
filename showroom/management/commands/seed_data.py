#!/usr/bin/env python
"""
Seed script to populate database with sample data and car images.
Run: python manage.py seed_data
"""

import io
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from showroom.models import Brand, Car


CAR_IMAGES = {
    'Toyota Camry': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&q=80',
    'Toyota RAV4': 'https://images.unsplash.com/photo-1581540222194-0def2dda95b8?w=800&q=80',
    'Honda Civic': 'https://images.unsplash.com/photo-1597404294360-feeeda04612e?w=800&q=80',
    'Honda CR-V': 'https://images.unsplash.com/photo-1583267746897-2cf415887172?w=800&q=80',
    'BMW 3 Series': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80',
    'BMW X5': 'https://images.unsplash.com/photo-1556189250-72ba954cfc2b?w=800&q=80',
    'Mercedes-Benz C-Class': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
    'Mercedes-Benz E-Class': 'https://unsplash.com/photos/JIKSp3GlVbk/download?force=true&w=800',
    'Tesla Model 3': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80',
    'Tesla Model Y': 'https://images.unsplash.com/photo-1536700503339-1e4b06520771?w=800&q=80',
    'Ford Mustang': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&q=80',
    'Ford Explorer': 'https://unsplash.com/photos/r6623jRyhDM/download?force=true&w=800',
    'Audi A4': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800&q=80',
    'Audi Q5': 'https://unsplash.com/photos/bNEcJppCTI8/download?force=true&w=800',
    'Hyundai Tucson': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
    'Hyundai Elantra': 'https://unsplash.com/photos/BUGj8EPg9A8/download?force=true&w=800',
    'Kia K5': 'https://unsplash.com/photos/pXo8Z5dgwxg/download?force=true&w=800',
    'Kia Telluride': 'https://unsplash.com/photos/tzpA1l2_UQ8/download?force=true&w=800',
    'Nissan Altima': 'https://unsplash.com/photos/grXozDsWupA/download?force=true&w=800',
    'Nissan Rogue': 'https://unsplash.com/photos/uNoAsK9kJZU/download?force=true&w=800',
    'Mahindra Thar': 'https://images.unsplash.com/photo-1688803676728-66fbb959ae26?w=800&q=80',
}


class Command(BaseCommand):
    help = 'Populate database with sample data and car images'

    def download_image(self, url, car_name):
        """Download image from URL and return as ContentFile."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img_content = ContentFile(response.content, name=f'{car_name.replace(" ", "_").lower()}.jpg')
                return img_content
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  Failed to download image for {car_name}: {e}'))
        return None

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))

        brands_data = [
            {'name': 'Toyota'},
            {'name': 'Honda'},
            {'name': 'BMW'},
            {'name': 'Mercedes-Benz'},
            {'name': 'Audi'},
            {'name': 'Ford'},
            {'name': 'Tesla'},
            {'name': 'Hyundai'},
            {'name': 'Kia'},
            {'name': 'Nissan', 'showroom_location': '1234 Nissan Boulevard, Suite 200', 'showroom_city': 'Los Angeles', 'showroom_phone': '+1 (800) 123-NISSAN'},
            {'name': 'Mahindra'},
        ]

        brands = []
        for data in brands_data:
            name = data['name']
            defaults = {k: v for k, v in data.items() if k != 'name'}
            brand, created = Brand.objects.get_or_create(name=name, defaults=defaults)
            if not created:
                for attr, value in defaults.items():
                    setattr(brand, attr, value)
                brand.save()
            brands.append(brand)
            if created:
                self.stdout.write(f'  Created brand: {name}')

        cars_data = [
            {'brand': 'Toyota', 'name': 'Camry', 'price': '28000.00', 'title': 'Reliable Midsize Sedan', 'description': 'The Toyota Camry offers a perfect blend of comfort, efficiency, and reliability. Features include advanced safety systems, spacious interior, and excellent fuel economy.'},
            {'brand': 'Toyota', 'name': 'RAV4', 'price': '32000.00', 'title': 'Popular Compact SUV', 'description': 'The RAV4 is Toyotas best-selling SUV with rugged styling, available hybrid powertrain, and plenty of cargo space for adventures.'},
            {'brand': 'Honda', 'name': 'Civic', 'price': '25000.00', 'title': 'Sporty Compact Car', 'description': 'The Honda Civic delivers an engaging driving experience with premium features, efficient engines, and a refined interior.'},
            {'brand': 'Honda', 'name': 'CR-V', 'price': '30000.00', 'title': 'Versatile Family SUV', 'description': 'The CR-V offers class-leading cargo space, comfortable seating, and available hybrid powertrain for maximum efficiency.'},
            {'brand': 'BMW', 'name': '3 Series', 'price': '45000.00', 'title': 'Luxury Sports Sedan', 'description': 'The BMW 3 Series sets the standard for luxury sports sedans with precise handling, powerful engines, and cutting-edge technology.'},
            {'brand': 'BMW', 'name': 'X5', 'price': '65000.00', 'title': 'Premium Luxury SUV', 'description': 'The BMW X5 combines athletic performance with luxurious comfort, advanced driver assistance, and versatile cargo space.'},
            {'brand': 'Mercedes-Benz', 'name': 'C-Class', 'price': '48000.00', 'title': 'Elegant Luxury Sedan', 'description': 'The Mercedes C-Class offers a sophisticated interior, smooth ride quality, and the latest MBUX infotainment system.'},
            {'brand': 'Mercedes-Benz', 'name': 'E-Class', 'price': '62000.00', 'title': 'Executive Luxury Sedan', 'description': 'The Mercedes E-Class combines cutting-edge technology with handcrafted luxury, delivering an unparalleled executive driving experience.'},
            {'brand': 'Tesla', 'name': 'Model 3', 'price': '42000.00', 'title': 'Electric Performance Sedan', 'description': 'The Tesla Model 3 delivers instant acceleration, long range, and industry-leading autopilot technology in a sleek package.'},
            {'brand': 'Tesla', 'name': 'Model Y', 'price': '50000.00', 'title': 'Electric SUV', 'description': 'The Model Y combines the versatility of an SUV with Teslas electric technology, offering spacious interior and impressive range.'},
            {'brand': 'Ford', 'name': 'Mustang', 'price': '35000.00', 'title': 'Iconic American Muscle', 'description': 'The Ford Mustang continues its legacy with powerful V8 options, modern technology, and unmistakable American styling.'},
            {'brand': 'Ford', 'name': 'Explorer', 'price': '41000.00', 'title': 'Adventure-Ready SUV', 'description': 'The Ford Explorer offers three-row seating, available 4WD, and smart technology for families who love adventure.'},
            {'brand': 'Audi', 'name': 'A4', 'price': '43000.00', 'title': 'Refined Luxury Sedan', 'description': "Audi's A4 features Quattro all-wheel drive, premium interior materials, and advanced virtual cockpit display."},
            {'brand': 'Audi', 'name': 'Q5', 'price': '48000.00', 'title': 'Luxury Compact SUV', 'description': 'The Audi Q5 blends sophisticated styling with powerful performance, featuring Quattro AWD and a premium cabin with advanced MMI technology.'},
            {'brand': 'Hyundai', 'name': 'Tucson', 'price': '28000.00', 'title': 'Stylish Compact SUV', 'description': 'The Hyundai Tucson stands out with bold design, generous warranty, and a well-equipped interior at a competitive price.'},
            {'brand': 'Hyundai', 'name': 'Elantra', 'price': '22000.00', 'title': 'Value-Packed Sedan', 'description': 'The Hyundai Elantra impresses with its dramatic design, impressive fuel economy, and class-leading warranty coverage.'},
            {'brand': 'Kia', 'name': 'K5', 'price': '29500.00', 'title': 'Sporty Midsize Sedan', 'description': 'The Kia K5 turns heads with its sleek fastback design, available all-wheel drive, and a refined interior that punches above its class.'},
            {'brand': 'Kia', 'name': 'Telluride', 'price': '36000.00', 'title': 'Award-Winning SUV', 'description': 'The Kia Telluride offers three-row seating, bold styling, and exceptional value with a premium interior that rivals luxury SUVs.'},
            {'brand': 'Nissan', 'name': 'Altima', 'price': '26000.00', 'title': 'Confident Sedan', 'description': 'The Nissan Altima features available all-wheel drive, ProPILOT Assist, and a spacious interior with Zero Gravity seats for ultimate comfort.'},
            {'brand': 'Nissan', 'name': 'Rogue', 'price': '29000.00', 'title': 'Versatile Compact SUV', 'description': 'The Nissan Rogue delivers a refined ride, smart storage solutions, and class-leading safety features for modern families.'},
            {'brand': 'Mahindra', 'name': 'Thar', 'price': '32000.00', 'title': 'Iconic Off-Road SUV', 'description': 'The Mahindra Thar is a legendary off-road SUV with rugged design, 4x4 capability, and modern amenities for adventure seekers.'},
        ]

        image_count = 0
        for car_data in cars_data:
            brand = Brand.objects.get(name=car_data['brand'])
            car_key = f"{car_data['brand']} {car_data['name']}"
            car, created = Car.objects.get_or_create(
                brand=brand,
                name=car_data['name'],
                defaults={
                    'price': car_data['price'],
                    'title': car_data['title'],
                    'description': car_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  Created car: {car}')

            if not car.image:
                image_url = CAR_IMAGES.get(car_key)
                if image_url:
                    img_file = self.download_image(image_url, car_key)
                    if img_file:
                        car.image.save(f'{car_key.replace(" ", "_").lower()}.jpg', img_file, save=True)
                        image_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  Added image for: {car}'))

        self.stdout.write(self.style.SUCCESS(f'\nSeeding complete!'))
        self.stdout.write(self.style.SUCCESS(f'  Images added: {image_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Total brands: {Brand.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  Total cars: {Car.objects.count()}'))
