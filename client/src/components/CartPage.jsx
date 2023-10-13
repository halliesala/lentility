import { useLoaderData, Link } from "react-router-dom";
import { Table } from "semantic-ui-react";
import CartRow from "./CartRow";

export default function CartPage() {
    const { order, order_items, prices } = useLoaderData()
    
    if (order_items.length === 0) {
        return (
            <p>There are no items in your cart. Time to <Link to="/shop">restock?</Link></p>
        )
    }

    


    return (
        <>
            <h2>Cart</h2>
            <p style={{color:'red'}}>order_id: {order.id}</p>
            <Table celled>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Product</Table.HeaderCell>
                        <Table.HeaderCell>Quantity</Table.HeaderCell>
                        <Table.HeaderCell>Price</Table.HeaderCell>
                        <Table.HeaderCell>Extended Price</Table.HeaderCell>
                        <Table.HeaderCell>Actions</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        order_items.map(item => <CartRow key={item.id} item={item} prices={prices[item.id]} />)
                    }
                </Table.Body>
            </Table>
            <Link to="/checkout">Continue to Checkout</Link>
        </>
    )
}