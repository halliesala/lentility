import { useEffect, useState } from "react"
import { useOutletContext } from "react-router-dom"

export default function SupplierProductsTable({order_item, prices}) {
    const { user, setUser } = useOutletContext()
    const [pricesLastRefreshed, setPricesLastRefreshed] = useState(new Date())

    const [priceInfo, setPriceInfo] = useState(prices)

    const cp_id = order_item.canonical_product_id
    console.log(order_item.canonical_product.suppliers)

    // Get prices for cp_id and practice_id
    function refreshPrice() {
        console.log("Refresh PRICE")
        fetch(`/api/v1/getpriceinfo/cp=${cp_id}/practice=${user.practice_id}`)
        .then(resp => resp.json())
        .then(data => {
            setPriceInfo(data)
            console.log("PRICEINFO: ", data)
            setPricesLastRefreshed(new Date())
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
                                    <td>{(priceInfo?.[s.name]?.price)?.toFixed(2) ?? 'Connect Vendor'}</td>
                                    <td>{priceInfo?.[s.name]?.free_shipping_threshold ?? 'Connect Vendor'}</td>    
                                </tr>
                            )
                        })
                    }
                </tbody>
            </table>
            <button onClick={refreshPrice}>Refresh Prices</button>
            <p>prices last refreshed: {pricesLastRefreshed.toLocaleString()}</p>
        </>
    )
}