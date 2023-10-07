export async function canonicalProductsLoader() {
    const response = await fetch("/api/v1/canonical_products")
    const canonicalProducts = await response.json()
    console.log(canonicalProducts)
    return { canonicalProducts }
}