import { useEffect } from "react";
import { useLoaderData, useOutletContext } from "react-router-dom"
import { Card } from 'semantic-ui-react';

export default function OrdersPage() {
    const { orders, vendorOrdersDict, orderItemsByVO } = useLoaderData()
    const { setMenuActive } = useOutletContext();

    useEffect(() => setMenuActive("orders"), [])

    return (
        <>
            {
                orders.map(o => {
                    return (
                        <OrderCard
                            key={o.id}
                            order={o}
                            vendorOrders={vendorOrdersDict[o.id]}
                            orderItemsByVO={orderItemsByVO}
                        />
                    )
                })
            }
        </>
    )
}

function OrderCard({ order, vendorOrders, orderItemsByVO }) {


    if (vendorOrders.length === 0) return null;

    // const subtotal = orderItems.reduce((acc, oi) => oi.price * oi.quantity + acc, 0)
    // const shipping = 0;

    const orderDate = (new Date(order.placed_time)).toLocaleDateString()
    return (
        <Card style={{ width: '80vw', textAlign: 'left', padding: '5%' }}>
            <Card.Header>Order #{order.id} -- {order.status === 'delivered' ? 'Delivered' : 'In Progress'}</Card.Header>
            <Card.Meta>Placed by {order.placed_by_user.first_name} {order.placed_by_user.last_name} on {orderDate}</Card.Meta>
            <Card.Content>
                {
                    vendorOrders.map(vo => {
                        return (
                            <Card key={vo.id} style={{ width: '80vw', textAlign: 'left', padding: '5%' }}>
                                <Card.Header>{vo.supplier.name}</Card.Header>
                                {
                                    orderItemsByVO[vo.id].map(oi => {
                                        return (
                                            <Card.Content key={oi.id}>
                                                <Card.Header>{oi.canonical_product.name}</Card.Header>
                                                <Card.Meta>{oi.canonical_product.manufacturer.name}</Card.Meta>
                                                <Card.Description>Quantity: {oi.quantity}</Card.Description>
                                                <Card.Description>Price: ${oi.price}</Card.Description>
                                            </Card.Content>
                                        )
                                    })
                                }
                            </Card>
                        )
                    })
                }

            </Card.Content>
        </Card>
    )
}