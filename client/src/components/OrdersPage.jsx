import { useLoaderData } from "react-router-dom"
import { Card } from 'semantic-ui-react';

export default function OrdersPage() {
    const { orders, orderItems } = useLoaderData()

    return (
        <>
        {
            orders.map(o => {
                return <OrderCard key={o.id} order={o} orderItems={orderItems[o.id]} />
            })
        }
        </>
    )
}

function OrderCard({ order, orderItems}) {

    const orderDate = (new Date(order.placed_time)).toLocaleDateString()
    return (
        <Card style={{ width: '80vw', textAlign: 'left', padding: '5%' }}>
            <Card.Header>Order #{order.id} -- {order.status==='delivered' ? 'Delivered' : 'In Progress'}</Card.Header>
            <Card.Meta>{`Placed by ${order.placed_by_user.first_name} ${order.placed_by_user.last_name} on ${orderDate}`}</Card.Meta>
        </Card>
    )
}