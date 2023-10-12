from app import app
import models

def calculate_price(product_id, practice_id):
    return getPriceInfo(product_id, practice_id)['price']

def getPriceInfo(product_id, practice_id):
    
    product = models.Product.query.filter_by(id=product_id).first()
    supplier = product.supplier
    # print("SUPPLIER: ", supplier.name, supplier.id)
     
    supplier_account = models.SupplierAccount.query.filter_by(practice_id=practice_id, supplier_id=supplier.id).first()
    # print("SUPPLIER ACCOUNT: ", supplier_account)
    if not supplier_account:
        return "Practice is missing this supplier"

    vendor_prefix = f"{product.supplier.name.replace(' ', '').capitalize()}"
    
    vendor_product_class = getattr(models, f"{vendor_prefix}Product")
    vendor_product = vendor_product_class.query.filter_by(sku=product.supplier_sku).first()
    
    vendor_user_class= getattr(models, f"{vendor_prefix}User")
    vendor_user = vendor_user_class.query.filter_by(username=supplier_account.username, password=supplier_account.password).first()
    
    return {
        'preset': vendor_product.price_preset, 
        'multiplier': vendor_user.price_multiplier, 
        'price': vendor_product.price_preset * vendor_user.price_multiplier,
        'days_to_ship': vendor_user.days_to_ship, 
        'free_shipping_threshold': vendor_user.free_shipping_threshold, 
        'shipping_cost': vendor_user.shipping_cost
    }

def getAllProductPriceInfo(cp_id, practice_id):

    products = models.Product.query.filter_by(canonical_product_id=cp_id).all()
    info = {p.supplier.name: getPriceInfo(p.id, practice_id) for p in products}
    return info


if __name__ == '__main__':
    with app.app_context(): 
        # Get VendorProduct preset
        # Get VendorUser multiplier
        # Return product

        print(getAllProductPriceInfo(cp_id=1, practice_id=14))


        


