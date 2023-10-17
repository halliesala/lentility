export async function canonicalProductsLoader() {
    const response = await fetch("/api/v1/canonical_products")
    const canonicalProducts = await response.json()
    console.log("CANONICAL PRODUCTS LOADER: ", canonicalProducts)
    return { canonicalProducts }
}

export async function sessionLoader() {
    const response = await fetch("/api/v1/checksession")
    const session = await response.json()
    console.log("SESSION LOADER: " , session)
    return { session }
}

export async function cartLoader() {
    // Load order and order items
    const order_and_items_response = await fetch("/api/v1/cart");
    const order_and_items = await order_and_items_response.json();
    console.log("ORDER AND ITEMS LOADER: ", order_and_items);
    const order = order_and_items.order;
    const order_items = order_and_items.order_items;
    console.log("CART LOADER: ", order_items);
    // Load prices for each order item
    const prices_response = await fetch("/api/v1/getcartprices");
    const prices = await prices_response.json();
    console.log("PRICES LOADER: ", prices);
    return { order, order_items, prices };
}

export async function supplierAccountsLoader() {
    const response = await fetch("/api/v1/supplieraccounts")
    const supplierAccounts = await response.json()
    console.log("SUPPLIER ACCOUNTS LOADER: ", supplierAccounts)
    const response2 = await fetch("/api/v1/suppliers")
    const suppliers = await response2.json()
    console.log("SUPPLIERS LOADER: ", suppliers)
    return { supplierAccounts, suppliers }
}

export async function ordersLoader() {
    // Get orders for logged-in practice
    const response = await fetch('/api/v1/ordersbyloggedinpractice')
    const orders = await response.json()
    console.log("ORDERS LOADER -- ORDERS: ", orders)
    // Get order items for each order
    const orderItemsByVO = {}
    const vendorOrdersDict = {}
    for (const o of orders) {
        const vendorOrderResponse = await fetch(`/api/v1/order=${o.id}/vendororders`)
        const vendorOrders = await vendorOrderResponse.json()
        vendorOrdersDict[o.id] = vendorOrders

        // Get order items for each order
        // const orderItemResponse = await fetch(`/api/v1/order=${o.id}/items`)
        // const orderItem = await orderItemResponse.json()
        // orderItems[o.id] = orderItem

        // Get order items for each vendor order
        for (const vo of vendorOrders) {
            const orderItemResponse = await fetch(`/api/v1/vendororder=${vo.id}/items`)
            const orderItems = await orderItemResponse.json()
            orderItemsByVO[vo.id] = orderItems
        }
    }
    console.log("ORDERS LOADER -- ORDERITEMS: ", orderItemsByVO)
    console.log("ORDERS LOADER -- VENDORORDERS: ", vendorOrdersDict)
    return { orders, vendorOrdersDict, orderItemsByVO }
}

export async function checkoutLoader() {
    const response = await fetch('/api/v1/addressesbyloggedinpractice')
    const addresses = await response.json()
    console.log("CHECKOUT LOADER -- ADDRESSES:", addresses)
    const response2 = await fetch('api/v1/paymentmethodsbyloggedinpractice')
    const paymentMethods = await response2.json()
    console.log("CHECKOUT LOADER -- PAYMENTMETHODS:", paymentMethods)
    return { addresses, paymentMethods }
}

export async function addressesLoader() {
    const response = await fetch('/api/v1/addressesbyloggedinpractice')
    const addresses = await response.json()
    console.log("ADDRESSES LOADER: ", addresses)
    return { addresses }
}

