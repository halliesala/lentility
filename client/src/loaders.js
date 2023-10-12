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
    const response = await fetch("/api/v1/cart")
    const cart = await response.json()
    console.log("CART LOADER: ", cart)
    // Load prices for each item in cart
    const response2 = await fetch("/api/v1/getcartprices")
    const prices = await response2.json()
    console.log("PRICES LOADER: ", prices)
    return { cart, prices }
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

