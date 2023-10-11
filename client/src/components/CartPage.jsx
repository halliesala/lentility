import { useLoaderData, Link } from "react-router-dom";
import { Table } from "semantic-ui-react";
import CartRow from "./CartRow";

export default function CartPage() {
    const { cart } = useLoaderData()
    

    console.log(cart)

    if (cart.length === 0) {
        return (
            <p>There are no items in your cart. Time to <Link to="/shop">restock?</Link></p>
        )
    }

    


    return (
        <>
            <h2>Cart</h2>
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
                        cart.map(item => <CartRow key={item.id} item={item} />)
                    }
                </Table.Body>
            </Table>
            <Link to="/checkout">Continue to Checkout</Link>
        </>
    )
}