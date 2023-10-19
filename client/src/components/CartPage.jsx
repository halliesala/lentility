import { useLoaderData, Link } from "react-router-dom";
import { Table, Loader, Segment, Popup, Icon } from "semantic-ui-react";
import CartRow from "./CartRow";
import { useState } from "react";
import { XlviLoader } from "react-awesome-loaders";


const XlviLoaderComponent = () => {
  return (
    <>
      <XlviLoader
        boxColors={["#646cff", "#610cf", "green"]}
        desktopSize={"128px"}
        mobileSize={"100px"}
      />
    </>
  );
};


export default function CartPage() {
    const { order, order_items, prices } = useLoaderData()
    const [orderItems, setOrderItems] = useState(order_items)
    const [loading, setLoading] = useState(false)
    
    function onTimeIn() {
        console.log("Time in")
        setLoading(false)
    }
    
    
    function optimizeCart() {
        setLoading(true)
        const start = Date.now()
        console.log("Start optimization: ", start)
        fetch('/api/v1/optimizecart', { method: 'POST' })
        .then(resp => resp.json())
        .then(data => {
            const end = Date.now()
            console.log("Optimization complete: ", end-start, "ms");
            if (end - start < 3000) {
                console.log("TODO: set timeout to 3000ms")
                setTimeout(onTimeIn, 3000)
            } else {
                setLoading(false)
            }
            console.log(data)
            setOrderItems(data.order_items)
        })
    }
    

    if (orderItems.length === 0) {
        return (
            <>
                {/* <p style={{ color: 'red' }}>order_id: {order.id}</p> */}
                <p>There are no items in your cart. Time to <Link to="/shop">restock?</Link></p>
            </>
        )
    }
    
    if (loading) {
        // return (
        //     <Segment style={{height: '10vh'}}>
        //         <Loader active={true}>Optimizing cart...</Loader>
        //     </Segment>

        // )

        return (
            <>
                <h2>Optimizing your cart ...</h2>
                <XlviLoaderComponent />
            </>
        )
    }


    

    return (
        <>
            <h2>Cart</h2>
            {/* <p style={{ color: 'red' }}>order_id: {order.id}</p> */}
            
            <Table celled>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Product</Table.HeaderCell>
                        <Table.HeaderCell>Quantity</Table.HeaderCell>
                        <Table.HeaderCell>Optimized Price
                            <Popup trigger={<Icon circular name='info' />}>
                                <Popup.Content>
                                    Your cart is optimized for maximum savings. 
                                    Prices may change as you add or remove items. 
                                </Popup.Content>
                            </Popup>
                        </Table.HeaderCell>
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
            <button onClick={optimizeCart}>Optimize My Cart</button>
            <div>
                <Link to="/checkout">Continue to Checkout</Link>
            </div>
        </>
    )
}