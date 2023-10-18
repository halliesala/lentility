import { useState } from "react";
import { useLoaderData } from "react-router-dom";
import { Form } from "semantic-ui-react";

export default function CheckoutPage() {

    const { addresses, paymentMethods } = useLoaderData();
    const [orderPlaced, setOrderPlaced] = useState(false)
    const [loading, setLoading] = useState(false)

    const primaryShippingAddress = addresses.find(a => a.is_primary_shipping)
    const primaryPaymentMethod = paymentMethods.find(pm => pm.is_primary)

    const [shippingAddress, setShippingAddress] = useState(primaryShippingAddress)
    const [paymentMethod, setPaymentMethod] = useState(primaryPaymentMethod)

    function handleSubmit(e) {
        e.preventDefault()
        console.log("Placing order...")
        setLoading(true)
        const POST_OPTIONS = {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'shipping_address_id': shippingAddress.id,
                'payment_method_id': paymentMethod.id
            })
        }
        fetch('/api/v1/placeorder', POST_OPTIONS)
            .then(res => res.json())
            .then(data => {
                console.log(data)
                setOrderPlaced(true)
                setLoading(false)
            })
    }

    if (loading) {
        return (
            <p>Loading ...</p>
        )
    }

    if (orderPlaced) {
        return (
            <p>Your order has been placed!</p>
        )
    }

    return (
        <>
            <h2>Checkout</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Field>
                    <label>Shipping Address</label>
                    <select
                        value={shippingAddress}
                        onChange={(e) => setShippingAddress(e.target.value)}
                    >
                        {
                            addresses.map(a => {
                                return (
                                    <option
                                        key={a.id}
                                        value={a}>
                                        {a.line_1}{a.line_2 ? ' ' + a.line_2 : ''}, {a.city}, {a.us_state} {a.zip_code}
                                    </option>
                                )
                            })
                        }
                    </select>
                </Form.Field>
                <Form.Field>
                    <label>Payment Method</label>
                    <select
                        value={paymentMethod}
                        onChange={(e) => setPaymentMethod(e.target.value)}
                    >
                        {
                            paymentMethods.map(pm => {
                                return (
                                    <option
                                        key={pm.id}
                                        value={pm}
                                    >
                                        {pm.nickname}
                                    </option>
                                )
                            })
                        }
                    </select>
                </Form.Field>
                <input type='submit' value='Confirm Order'/>
            </Form>

        </>

    )
}