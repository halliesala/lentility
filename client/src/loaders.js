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

// export async function pricesLoader({ params }) {
//     const response = await fetch(`/api/v1/getpriceinfo/cp=${params.cp_id}/practice=${params.practice_id}`)
//     const priceInfo = await response.json()
//     console.log("PRICES LOADER: ", priceInfo)
//     return { priceInfo }
// }

