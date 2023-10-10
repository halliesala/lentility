export async function canonicalProductsLoader() {
    const response = await fetch("/api/v1/canonical_products")
    const canonicalProducts = await response.json()
    console.log("LOADER: ", canonicalProducts)
    return { canonicalProducts }
}

export async function sessionLoader() {
    const response = await fetch("/api/v1/checksession")
    const session = await response.json()
    console.log("LOADER: " , session)
    return { session }
}

