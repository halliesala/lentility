import { useLoaderData } from 'react-router-dom';
import { Card } from 'semantic-ui-react'

export default function ShopPage() {
    const { canonicalProducts } = useLoaderData()

    return (
        <>
            {
                canonicalProducts.map(cp => {
                    return (
                        <Card key={cp.id} >
                            <h2>{cp.name}</h2>
                            <h3>{cp.manufacturer.name}</h3>
                            <h3>{cp.manufacturer_sku}</h3>
                            <span>{} Suppliers</span>
                        </Card>
                    )
                })
            }
        </>
    )
}