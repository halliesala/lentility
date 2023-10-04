from app import app, bcrypt
import models as m
from faker import Faker
from random import randint, choice
from datetime import datetime

fake = Faker()

# ----- PRODUCT ATTRIBUTES ----- #
LENTIL_TYPES = ['Red Lentils', 'Green Lentils', 'Brown Lentils', 'Black Lentils', 'Pidgeon Peas', 'Chickpeas', 'Green Split Peas', 'Yellow Split Peas']
QUANTITIES_LB = [1, 10, 100]
MANUFACTURERS = ['Lentilmania', "Barb's Best Beans", "The Puy Tool", "lTero", "Planterson", "Hearty Soups International", "Lentsply Sproutona", "House Brand"]


class SeedDB:

    @classmethod
    def seed_manufacturers(cls):
        m.Manufacturer.query.delete()
        for mfct in MANUFACTURERS:
            m.db.session.add(m.Manufacturer(name=mfct))
            m.db.session.commit()
    
    @classmethod
    def seed_canonical_products(cls):
        # Clear existing products #
        m.CanonicalProduct.query.delete()

        
        # Helper functions for generating products #
        def sku(manufacturer):
            return manufacturer[:3].upper() + ''.join([str(randint(0,9)) for i in range(7)])
        def product_name(lentil_type, quantity, manufacturer):
            return f"{lentil_type} - {quantity} lb"
        def description(lentil_type, quantity, manufacturer):
            return f"{lentil_type} from {manufacturer}. {quantity} lb bag."
        
        for l in LENTIL_TYPES:
            for q in QUANTITIES_LB:
                for mfct in MANUFACTURERS:
                    cp = m.CanonicalProduct(
                        manufacturer_id = m.Manufacturer.query.filter_by(name=mfct).first().id,
                        manufacturer_sku = sku(mfct),
                        name = product_name(l, q, mfct),
                        description = description(l, q, mfct),
                        quantity = q,
                        image_link = None,
                        price_preset = q  * len(l) * len(mfct) * 0.01,
                    )
                    # Not every manufacturer has every product
                    if (choice([True, False])):
                        m.db.session.add(cp)
                        m.db.session.commit()
        m.db.session.commit()

    @classmethod
    def seed_vendor_products(cls):

        # Each supplier has a same-named house brand and carries all canonical_products from that brand 
        # housebrand1 and housebrand2 both carry the housebrand manufacturer
        HOUSE_BRAND_MANUFACTURERS = {
                'heartysoupsinternational': 'Hearty Soups International',
                'planterson': 'Planterson',
                'lentsplysproutona': 'Lentsply Sproutona',
                'housebrand1': 'House Brand',
                'housebrand2': 'House Brand',
            }
        hb_mfcts = m.Manufacturer.query.filter(m.Manufacturer.name.in_(HOUSE_BRAND_MANUFACTURERS.values())).all()
        hb_mfct_ids = [m.id for m in hb_mfcts]

        # Suppliers also carry a random selection of products from 'name brands' like 'Lentilmania', "Barb's Best Beans", "The Puy Tool", and "lTero".
        name_brand_products = (m.CanonicalProduct.query.filter(~m.CanonicalProduct.manufacturer_id.in_(hb_mfct_ids)).all())

        for v in m.VENDORS:

            # Clear products table for vendor #
            print("Clearing products for {v}...")
            m.vendor_classes[v.capitalize() + 'Product'].query.delete()

            print(f"Seeding products for {v}...")
            
            house_brand_manufacturer = m.Manufacturer.query.filter_by(name=HOUSE_BRAND_MANUFACTURERS[v]).first()
            house_brand_products = m.CanonicalProduct.query.filter_by(manufacturer_id=house_brand_manufacturer.id).all()
            other_products = [p for p in name_brand_products if choice([True, False])]

            print(f"Adding {len(house_brand_products)} house brand and {len(other_products)} other products...")
            
            for cp in house_brand_products + other_products:
                class_name = f"{v.capitalize()}Product"

                # Manufacturer of the canonical product
                manufacturer = m.Manufacturer.query.filter_by(id=cp.manufacturer_id).first()

                vp = m.vendor_classes[class_name](
                    name = cp.name,
                    manufacturer_name = manufacturer.name,
                    manufacturer_sku = cp.manufacturer_sku,
                    stock = randint(0, 100),
                    image_link = cp.image_link,
                    price_preset = cp.price_preset * len(v) * 0.1 if v not in ('housebrand1','housebrand2') else cp.price_preset,
                )
                m.db.session.add(vp)

            m.db.session.commit()
            

if __name__ == '__main__':
    with app.app_context():
        SeedDB.seed_manufacturers()
        SeedDB.seed_canonical_products()
        SeedDB.seed_vendor_products()
