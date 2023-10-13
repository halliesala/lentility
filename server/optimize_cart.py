from app import app, getAllProductPriceInfo, getPriceInfo
import models
import itertools

def getBestFulfillmentInfo(user_id):

    user = models.User.query.filter_by(id=user_id).first()

    practice_id = user.practice_id
    order_id = models.Order.query.filter_by(practice_id=practice_id, status='in_cart').first().id
    
    # Get cart -- #89  is Thursday Test Practice's active cart
    cart = models.Order.query.filter_by(id=order_id).first()

    # Get prices for all products in cart
    fulfillment_options = {}
    for item in cart.order_items:
        fulfillment_options[item.id] = getAllProductPriceInfo(item.canonical_product_id, practice_id=practice_id)

    connected_fulfillments = {}
    # Get all combinations of product fulfillments
    for (order_item_id, options) in fulfillment_options.items():
        for (vendor_name, product_info) in options.items():
            if 'price' in product_info:
                connected_fulfillments[order_item_id] = connected_fulfillments.get(order_item_id, []) + [product_info['product_id']]


    # Get Cartesian product of all fulfillments
    all_fulfillments = list(itertools.product(*connected_fulfillments.values()))
    # print(all_fulfillments)

    # For each possible fulfillment, calculate total price
    fulfillment_prices = []
    fulfillment_prices_dict = {}
    for fulfillment in all_fulfillments:
        total = 0
        subtotal = 0
        shipping = 0
        vendor_subtotals = {}
        vendor_free_shipping_threshold = {}
        vendor_shipping_below_threshold = {}
        vendor_shipping = {}
        for product_id in fulfillment:
            product = models.Product.query.filter_by(id=product_id).first()
            supplier = product.supplier
            price_info = getPriceInfo(product_id, practice_id=practice_id)
            subtotal += price_info['price']
            vendor_subtotals[supplier.name] = vendor_subtotals.get(supplier.name, 0) + price_info['price']
            vendor_shipping_below_threshold[supplier.name] = price_info['shipping_cost']
            vendor_free_shipping_threshold[supplier.name] = price_info['free_shipping_threshold']
        for (vendor, subtotal) in vendor_subtotals.items():
            # calculate shipping cost
            if subtotal < vendor_free_shipping_threshold[vendor]:
                vendor_shipping[vendor] = vendor_shipping_below_threshold[vendor]
                shipping += vendor_shipping[vendor]
        total = subtotal + shipping
        fulfillment_prices.append((fulfillment, total, subtotal, shipping, vendor_subtotals, vendor_shipping_below_threshold))
        fulfillment_prices_dict[fulfillment] = {'total': total, 'subtotal': subtotal, 'shipping': shipping, 'vendor_subtotals': vendor_subtotals, 'vendor_shipping_below_threshold': vendor_shipping_below_threshold}
    fulfillment_prices.sort(key=lambda x: x[1])
    # for fp in fulfillment_prices:
        # print(fp)
        


    # For now, 'best' fulfillment is the one with the lowest total price
    best_fulfillment = min(fulfillment_prices_dict, key=lambda x: fulfillment_prices_dict[x]['total'])
    print("Best fulfillment:", best_fulfillment)

    fulfilled_product_to_order_item_map = {}
    for product_id in best_fulfillment:
        product = models.Product.query.filter_by(id=product_id).first()
        order_item = models.OrderItem.query.filter_by(order_id=order_id, canonical_product_id=product.canonical_product_id).first()
        fulfilled_product_to_order_item_map[order_item.id] = product_id

    # print(fulfilled_product_to_order_item_map, fulfillment_prices_dict[best_fulfillment]['total'])

    return {'fulfilled_product_to_order_item_map': fulfilled_product_to_order_item_map, 'info': fulfillment_prices_dict[best_fulfillment]}


if __name__ == '__main__':
    with app.app_context(): 
        print(getBestFulfillmentInfo(26))

        



        

        