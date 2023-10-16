import { useLoaderData, Link } from "react-router-dom";
import { Table, Loader, Segment } from "semantic-ui-react";
import CartRow from "./CartRow";
import { useState } from "react";

export default function CartPage() {
    const { order, order_items, prices } = useLoaderData()
    const [orderItems, setOrderItems] = useState(order_items)
    const [loading, setLoading] = useState(false)
    
    
    
    function optimizeCart() {
        setLoading(true)
        const start = Date.now()
        console.log("Start optimization: ", start)
        console.log("Optimizing cart...")
        fetch('/api/v1/optimizecart', { method: 'POST' })
        .then(resp => resp.json())
        .then(data => {
            const end = Date.now()
            console.log("Optimization complete: ", end-start, "ms");
            if (end - start < 3000) {
                console.log("TODO: set timeout to 3000ms")
            }
            console.log(data)
            setOrderItems(data.order_items)
            setLoading(false)
        })
    }
    

    if (orderItems.length === 0) {
        return (
            <>
                <p style={{ color: 'red' }}>order_id: {order.id}</p>
                <p>There are no items in your cart. Time to <Link to="/shop">restock?</Link></p>
            </>
        )
    }
    
    if (loading) {
        return (
            <Segment>
                <Loader active={true}>Optimizing cart...</Loader>
            </Segment>

        )
    }


    

    return (
        <>
            <h2>Cart</h2>
            <p style={{ color: 'red' }}>order_id: {order.id}</p>
            <button onClick={optimizeCart}>Optimize My Cart</button>
            
            <Table celled>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Product</Table.HeaderCell>
                        <Table.HeaderCell>Quantity</Table.HeaderCell>
                        <Table.HeaderCell>Optimized Price</Table.HeaderCell>
                        <Table.HeaderCell>Extended Price</Table.HeaderCell>
                        <Table.HeaderCell>Actions</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        orderItems.map(item => <CartRow key={item.id} item={item} prices={prices[item.id]} />)
                    }
                </Table.Body>
            </Table>
            <Link to="/checkout">Continue to Checkout</Link>
        </>
    )
}