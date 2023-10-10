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
    return { cart }
}
