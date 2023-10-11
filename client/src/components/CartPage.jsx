import { useLoaderData, Link } from "react-router-dom"

export default function CartPage() {
    const { cart } = useLoaderData()


    return (
        <>
            <h2>Cart</h2>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Extended Price</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        // Format numbers to two decimal places
                        cart.map(item => {
                            return (
                                <tr key={item.id}>
                                    <td>
                                        <p>{item.canonical_product.manufacturer.name} {item.canonical_product.name}</p>
                                    </td>
                                    <td>{item.quantity}</td>
                                    <td>{item.price ? item.price.toFixed(2) : <i>pending</i>}</td>
                                    <td>{item.price ? (item.price * item.quantity).toFixed(2): <i>pending</i>}</td>
                                </tr>
                            )
                        })
                    }
                </tbody>
            </table>
            <Link to="/checkout">Continue to Checkout</Link>
        </>
    )
}