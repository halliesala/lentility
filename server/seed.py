from app import app, bcrypt
import models as m
from faker import Faker
from random import randint, choice, sample
from datetime import datetime, timedelta
from sqlalchemy import func

fake = Faker()

LENTIL_TYPES = ['Red Lentils', 'Green Lentils', 'Brown Lentils', 'Black Lentils', 'Pidgeon Peas', 'Chickpeas', 'Green Split Peas', 'Yellow Split Peas']
QUANTITIES_LB = [1, 10, 100]
MANUFACTURERS = ['Lentilmania', "Barb's Best Beans", "The Puy Tool", "lTero", "Planterson", "Hearty Soups International", "Lentsply Sproutona", "House Brand"]
SUPPLIERS = ['Hearty Soups International', 'Planterson', 'Lentsply Sproutona', 'Lentil City', 'DC Lentil']
HOUSE_BRAND_MANUFACTURERS = {
                'heartysoupsinternational': 'Hearty Soups International',
                'planterson': 'Planterson',
                'lentsplysproutona': 'Lentsply Sproutona',
                'lentilcity': 'House Brand',
                'dclentil': 'House Brand',
            }
ORDER_STATUSES = ['in_cart', 'placed', 'delivered']
DOTS = '...'


class SeedDB:

    # MAIN DB #

    # -- NO DEPENDENCIES -- #
    @classmethod
    def clear_db(cls):
        for table in reversed(m.db.metadata.sorted_tables):
            m.db.session.execute(table.delete())
        m.db.session.commit()

    @classmethod
    def seed_manufacturers(cls):
        m.Manufacturer.query.delete()
        print("Seeding manufacturers...")
        for mfct in MANUFACTURERS:
            m.db.session.add(m.Manufacturer(name=mfct))
            m.db.session.commit()
        print("Done.")
    
    @classmethod
    def seed_practices(cls):
        m.Practice.query.delete()
        print("Seeding practices...")
        for i in range(10):
            p = m.Practice(
                name = fake.company(),
                created_time = fake.date_time_between(start_date='-2y', end_date='-3m'),
            )
            m.db.session.add(p)
        m.db.session.commit()
        print("Done.")

    @classmethod
    def seed_suppliers(cls):
        m.Supplier.query.delete()
        print("Seeding suppliers...")
        for s in SUPPLIERS:
            supplier = m.Supplier(
                name = s,
                house_brand = HOUSE_BRAND_MANUFACTURERS[s.lower().replace(' ', '')],
                preferred = True if s in ['Lentil City', 'DC Lentil'] else False,
            )
            m.db.session.add(supplier)
        m.db.session.commit()
        print("Done.")

    # -- DEPENDENCIES: manufacturers -- #
    @classmethod
    def seed_canonical_products(cls):
        m.CanonicalProduct.query.delete()

        print("Seeding canonical products...")
        # Helper functions for generating products #
        def sku(manufacturer):
            return manufacturer[:3].upper() + ''.join([str(randint(0,9)) for i in range(12)])
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
        print("Done.")

    # -- DEPENDENCIES: canonical_products, suppliers, vendor products -- #
    @classmethod
    def seed_products(cls):
        # Add all products from vendor product tables
        m.Product.query.delete()
        print('Seeding products...')
        for v in m.VENDORS:
            supplier = m.Supplier.query.filter(func.replace(func.lower(m.Supplier.name), ' ', '') == v).first()
            vendor_products = m.vendor_classes[v.capitalize() + 'Product'].query.all()
            for vp in vendor_products:
                # Match manufacturer name and sku to canonical product; if none, skip
                try:
                    manufacturer = m.Manufacturer.query.filter_by(name=vp.manufacturer_name).one()
                    canonical_product = m.CanonicalProduct.query.filter_by(manufacturer_sku=vp.manufacturer_sku, manufacturer_id=manufacturer.id).one()
                except:
                    # No match found
                    continue
                # Create product and add to db
                p = m.Product(
                    name = vp.name,
                    canonical_product_id = canonical_product.id,
                    supplier_id = supplier.id,
                    supplier_sku = vp.sku,
                    image_link = None,
                )
                m.db.session.add(p)
        m.db.session.commit()
        print("Done.")

    # -- DEPENDENCIES: practices -- #
    @classmethod
    def seed_users(cls):
        m.User.query.delete()

        print("Seeding users. This may take a minute... ")
        practices = m.Practice.query.all()
        for p in practices:
            # All users have the same password, 'password'
            # Generate primary user
            first_name = fake.first_name()
            last_name = fake.last_name()
            email_domain = 'lentilmail.com'
            primary_user = m.User(
                email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}",
                password = bcrypt.generate_password_hash('password').decode('utf-8'),
                practice_id = p.id,
                role = 'lentist',
                first_name = first_name,
                last_name = last_name,
                is_primary = True,
            )
            m.db.session.add(primary_user)
            # Generate 0-2 secondary users
            for _ in range(randint(0, 2)):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email_domain = 'lentilmail.com'
                u = m.User(
                    email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}",
                    password = bcrypt.generate_password_hash('password').decode('utf-8'),
                    practice_id = p.id,
                    role = choice(['lentist', 'lentil_assistant']),
                    first_name = first_name,
                    last_name = last_name,
                    is_primary = False,
                )
                m.db.session.add(u)
        m.db.session.commit()
        print("Done.")

    @classmethod
    def seed_addresses(cls):
        m.Address.query.delete()

        print("Seeding addresses...")

        practices = m.Practice.query.all()
        for p in practices:
            addresses = []
            # Seed 1-3 addresses
            for _ in range(randint(1, 3)):
                us_state = choice(["NY", "CA", "NJ", "FL"])
                a = m.Address(
                    practice_id = p.id,
                    line_1 = fake.street_address(), 
                    line_2 = choice([None, f"Unit {randint(0, 100)}"]), 
                    city = fake.city(),
                    us_state = us_state, 
                    zip_code = fake.zipcode_in_state(us_state), # Add faker zip code
                    is_primary_shipping = False,
                )
                addresses.append(a)
            # Select one as primary shipping
            primary_shipping_address = choice(addresses)
            primary_shipping_address.is_primary_shipping = True
            # Add addresses to db
            m.db.session.add_all(addresses)
        m.db.session.commit()
        print("Done.")

    # -- DEPENDENCIES: practices, addresses -- #
    @classmethod
    def seed_payment_methods(cls):
        m.PaymentMethod.query.delete()

        print("Seeding payment methods ...")

        practices = m.Practice.query.all()
        for p in practices:
            addresses = m.Address.query.filter_by(practice_id=p.id).all()
            users = m.User.query.filter_by(practice_id=p.id).all()
            payment_methods = []
            for _ in range(randint(1, 3)):
                pm = m.PaymentMethod(
                    practice_id = p.id,
                    billing_address_id = choice(addresses).id,
                    nickname = f"{choice(users).first_name}'s {choice(['Visa', 'MasterCard', 'American Express', 'Discover'])} **{randint(1000, 9999)}",
                    is_primary = False,
                )
                payment_methods.append(pm)
            # Select one as primary payment method
            primary = choice(payment_methods)
            primary.is_primary = True
            m.db.session.add_all(payment_methods)
        m.db.session.commit()
        print("Done.")

    # -- DEPENDENCIES: practices, suppliers -- #
    @classmethod
    def seed_supplier_accounts(cls):
        m.SupplierAccount.query.delete()
        print("Seeding supplier accounts ...")
        practices = m.Practice.query.all()
        suppliers = m.Supplier.query.all()
        for p in practices:
            for s in suppliers:
                created_time = fake.date_between(start_date=p.created_time, end_date='now')
                last_validated = fake.date_between(start_date=created_time, end_date='now')
                if choice([True, False]):
                    sa = m.SupplierAccount(
                        supplier_id = s.id,
                        practice_id = p.id,
                        username = fake.user_name(),
                        password = fake.password(),
                        valid = randint(0, 10) < 8,
                        last_validated = last_validated,
                        created_time = created_time,
                    )
                    m.db.session.add(sa)
        m.db.session.commit()
        print("Done.")

    # -- DEPENDENCIES: practices, addresses, users, payment_methods
    @classmethod
    def seed_orders(cls):
        m.Order.query.delete()
        print("Seeding orders ...")
        practices = m.Practice.query.all()
        for p in practices:
            addresses = m.Address.query.filter_by(practice_id=p.id).all()
            users = m.User.query.filter_by(practice_id=p.id).all()
            payment_methods = m.PaymentMethod.query.filter_by(practice_id=p.id).all()
            created_time = p.created_time
            # 0-10 delivered orders
            for _ in range(randint(0, 10)):
                placed_time = fake.date_between(start_date=created_time, end_date='now')
                o = m.Order(
                    practice_id = p.id,
                    placed_by_user_id = choice(users).id,
                    created_time = created_time,
                    placed_time = placed_time,
                    status = 'delivered',
                    payment_method_id = choice(payment_methods).id,
                    shipping_address_id = choice(addresses).id
                )
                m.db.session.add(o)
                created_time = placed_time
            # 0-2 'placed' orders
            for _ in range(randint(0, 2)):
                placed_time = fake.date_between(start_date=created_time, end_date='now')
                o = m.Order(
                    practice_id = p.id,
                    placed_by_user_id = choice(users).id,
                    created_time = created_time,
                    placed_time = placed_time,
                    status = 'placed',
                    payment_method_id = choice(payment_methods).id,
                    shipping_address_id = choice(addresses).id,
                )
                m.db.session.add(o)
                created_time = placed_time
            # 1 'in_cart' order
            placed_time = fake.date_between(start_date=created_time, end_date='now')
            o = m.Order(
                practice_id = p.id,
                placed_by_user_id = choice(users).id,
                created_time = created_time,
                placed_time = None,
                status = 'in_cart',
                payment_method_id = choice(payment_methods).id,
                shipping_address_id = choice(addresses).id,
            )
            m.db.session.add(o)
        m.db.session.commit()
        print("Done.")
    
    # -- DEPENDENCIES: practices, orders, suppliers, (vendor_users.days_to_ship) -- #
    @classmethod
    def seed_vendor_orders(cls):
        m.VendorOrder.query.delete()
        print("Seeding vendor orders...")
        practices = m.Practice.query.all()
        for p in practices:
            orders = m.Order.query.filter_by(practice_id=p.id).all()
            supplier_accounts = m.SupplierAccount.query.filter_by(practice_id=p.id).all()
            connected_suppliers = m.Supplier.query.filter(m.Supplier.id.in_([sa.supplier_id for sa in supplier_accounts])).all()
            for o in orders:
                # Pick 1-3 suppliers and create vendor orders
                order_suppliers = sample(connected_suppliers, randint(0, len(connected_suppliers)))
                for s in order_suppliers:
                    # Get practice's supplier account for this supplier
                    supplier_account = m.SupplierAccount.query.filter_by(practice_id=p.id, supplier_id=s.id).first()
                    # Get [Vendor]User record for this supplier_account
                    vendor_user_class_name = f"{s.name.lower().replace(' ', '').capitalize()}User"
                    vendor_user_class = getattr(m, vendor_user_class_name)
                    # Get days to ship
                    vendor_user_record = vendor_user_class.query.filter_by(username=supplier_account.username, password=supplier_account.password).first()
                    days_to_ship = vendor_user_record.days_to_ship
                    estimated_delivery_date = o.placed_time + timedelta(days=days_to_ship) if o.placed_time else None
                    vo = m.VendorOrder(
                        order_id = o.id,
                        supplier_id = s.id,
                        # Update this 
                        shipping_and_handling = 9.99,
                        tax = 0.00,
                        tracking_number = fake.bothify(text='Z##?###??#?#?#####?##?'),
                        # Update this to be placed_time + vendor_user.days_to_ship
                        estimated_delivery_date = estimated_delivery_date,
                    )
                    m.db.session.add(vo)
        m.db.session.commit()
        print("Done.")

    # -- DEPENDENCIES: orders, vendor_orders, products, canonical_products
    @classmethod
    def seed_order_items(cls):
        m.OrderItem.query.delete()
        print("Seeding order items...")
        all_cps = m.CanonicalProduct.query.all()
        practices = m.Practice.query.all()
        for (i, p) in enumerate(practices):
            print(f"{DOTS*1}Seeding order items for practice {i+1}/{len(practices)} ({p.name.upper()})...")
            # For each vendor order, created 1-5 order items
            # No canonical product should be in more than one vendor order
            orders = m.Order.query.filter_by(practice_id=p.id).all()
            for o in orders:
                vendor_orders = m.VendorOrder.query.filter_by(order_id=o.id).all()
                canonical_products = []
                for vo in vendor_orders:
                    # Get the vendor user price multiplier
                    # -- vendor_orders.supplier_id -> suppliers.name -> [Suppliername]User table
                    # -- practices.id + suppliers.id -> supplier_accounts.username, password -> [Suppliername]User record -> price_multiplier
                    supplier = m.Supplier.query.filter_by(id=vo.supplier_id).first()
                    vendor_user_class_name = f"{supplier.name.lower().replace(' ', '').capitalize()}User"
                    vendor_user_class = getattr(m, vendor_user_class_name)
                    practice_supplier_account = m.SupplierAccount.query.filter_by(practice_id=p.id, supplier_id=vo.supplier_id).first()
                    vendor_user_record = vendor_user_class.query.filter_by(username=practice_supplier_account.username, password=practice_supplier_account.password).first()
                    price_multiplier = vendor_user_record.price_multiplier
                    # Get all products from this supplier that haven't previously been added to another vendor order for this order
                    vendor_products = m.Product.query.filter(m.Product.supplier_id==vo.supplier_id, ~m.Product.canonical_product_id.in_(canonical_products)).all()
                    sample_products = sample(vendor_products, randint(1, 5))
                    canonical_products += [sp.canonical_product_id for sp in sample_products]
                    for sp in sample_products:
                        # Get the item price preset
                        vendor_product_class_name = f"{supplier.name.lower().replace(' ', '').capitalize()}Product"
                        vendor_product_class = getattr(m, vendor_product_class_name)
                        vendor_product = vendor_product_class.query.filter_by(sku=sp.supplier_sku).first()
                        price_preset = vendor_product.price_preset
                        # Created_time is between order.created_time and order.placed_time (or now if order is in_cart)
                        created_time = fake.date_between(start_date=o.created_time, end_date=(o.placed_time if o.placed_time else datetime.now() ))
                        # Create the order item
                        oi = m.OrderItem(
                            order_id = o.id,
                            fulfilled_by_product_id = sp.id,
                            created_time = created_time,
                            canonical_product_id = sp.canonical_product_id,
                            quantity = randint(1, 9),
                            price = price_preset * price_multiplier,  
                            vendor_order_id = vo.id,
                        )
                        m.db.session.add(oi)
        m.db.session.commit()
        print("Done.")


    # VENDOR DBs #
    # -- DEPENDENCIES: canonical_products -- #
    @classmethod
    def seed_vendor_products(cls):

        print("Seeding vendor products...")

        # Each supplier has a same-named house brand and carries all canonical_products from that brand 
        # lentilcity and dclentil both carry the housebrand manufacturer
        hb_mfcts = m.Manufacturer.query.filter(m.Manufacturer.name.in_(HOUSE_BRAND_MANUFACTURERS.values())).all()
        hb_mfct_ids = [m.id for m in hb_mfcts]

        # Suppliers also carry a random selection of products from 'name brands' like 'Lentilmania', "Barb's Best Beans", "The Puy Tool", and "lTero".
        name_brand_products = (m.CanonicalProduct.query.filter(~m.CanonicalProduct.manufacturer_id.in_(hb_mfct_ids)).all())

        for v in m.VENDORS:

            # Clear products table for vendor #
            m.vendor_classes[v.capitalize() + 'Product'].query.delete()

            print(f"{DOTS*1}Seeding products for {v}...")
            
            house_brand_manufacturer = m.Manufacturer.query.filter_by(name=HOUSE_BRAND_MANUFACTURERS[v]).first()
            house_brand_products = m.CanonicalProduct.query.filter_by(manufacturer_id=house_brand_manufacturer.id).all()
            other_products = [p for p in name_brand_products if choice([True, False])]

            print(f"{DOTS*2}Adding {len(house_brand_products)} house brand and {len(other_products)} other products...")
            
            for cp in house_brand_products + other_products:
                class_name = f"{v.capitalize()}Product"

                # Manufacturer of the canonical product
                manufacturer = m.Manufacturer.query.filter_by(id=cp.manufacturer_id).first()

                vp = m.vendor_classes[class_name](
                    name = cp.name,
                    sku = v[:3].upper() + str(randint(100000, 999999)),
                    manufacturer_name = manufacturer.name,
                    manufacturer_sku = cp.manufacturer_sku,
                    stock = randint(0, 100),
                    image_link = cp.image_link,
                    price_preset = cp.price_preset * len(v) * 0.1 if v not in ('lentilcity','dclentil') else cp.price_preset,
                )
                m.db.session.add(vp)

            m.db.session.commit()
        print("Done seeding vendor products.")

    @classmethod
    def seed_vendor_users(cls):
        # Clear vendor_users tables
        for v in m.VENDORS:
            m.vendor_classes[v.capitalize() + 'User'].query.delete()
        # For each supplier_account, create a corresponding vendor_user
        print("Seeding vendor users...")
        supplier_accounts = m.SupplierAccount.query.all()
        for sa in supplier_accounts:
            # Find the right VendorUser class
            supplier = m.Supplier.query.filter_by(id=sa.supplier_id).first()
            supplier_name = supplier.name.lower().replace(' ', '')
            vendor_user_class_name = f"{supplier_name.capitalize()}User"
            vendor_user_class = getattr(m, vendor_user_class_name)
            vu = vendor_user_class(
                username = sa.username,
                password = sa.password,
                price_multiplier = randint(80, 120) * 0.01 if not supplier.preferred else 1.00,
                days_to_ship = randint(1, 5),
                free_shipping_threshold = choice([0, 49, 99, 99, 199]),
                shipping_cost = choice([9.99, 19.99])
            )
            m.db.session.add(vu)
        m.db.session.commit()
        print("Done.")



if __name__ == '__main__':
    with app.app_context():
        SeedDB.clear_db()
        SeedDB.seed_manufacturers()
        SeedDB.seed_practices()
        SeedDB.seed_users()
        SeedDB.seed_canonical_products()
        SeedDB.seed_vendor_products()
        SeedDB.seed_addresses()
        SeedDB.seed_payment_methods()
        SeedDB.seed_suppliers()
        SeedDB.seed_products()
        SeedDB.seed_supplier_accounts()
        SeedDB.seed_orders()
        SeedDB.seed_vendor_users()
        SeedDB.seed_vendor_orders()
        SeedDB.seed_order_items()
        # import ipdb; ipdb.set_trace()

