import { useEffect, useState } from "react"
import { useOutletContext } from "react-router-dom"

export default function SupplierProductsTable({order_item}) {
    const { user, setUser } = useOutletContext()

    const [priceInfo, setPriceInfo] = useState()

    const cp_id = order_item.canonical_product_id
    console.log(order_item.canonical_product.suppliers)

    // Get prices for cp_id and practice_id
    function getPrice() {
        console.log("GET PRICE")
        fetch(`/api/v1/getpriceinfo/cp=${cp_id}/practice=${user.practice_id}`)
        .then(resp => resp.json())
        .then(data => {
            setPriceInfo(data)
            console.log("PRICEINFO: ", data)
        })
    }

    return (
        <>
            <table>
                <thead>
                    <tr>
                        <th>Supplier</th>
                        <th>Price</th>
                        <th>Free Shipping Threshold</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        order_item.canonical_product.suppliers
                        .map(s => {
                            return (
                                <tr key={s.id}>
                                    <td>{s.name}</td>
                                    <td>{(priceInfo?.[s.name]?.price)?.toFixed(2) ?? '--'}</td>
                                    <td>{priceInfo?.[s.name]?.free_shipping_threshold ?? '--'}</td>    
                                </tr>
                            )
                        })
                    }
                </tbody>
            </table>
            <button onClick={getPrice}>Get Prices</button>
        </>
    )
}