import { Icon, Table, Input, Form, Popup, Image } from 'semantic-ui-react';
import { useState } from 'react';
import SupplierProductsTable from './SupplierProductsTable';
import { Link } from 'react-router-dom';

export default function CartRow({ item, prices }) {

    const [showFulfillmentExplanation, setShowFulfillmentExplanation] = useState(false)


    console.log("CART ROW ITEM", item)
    // console.log("CART ROW PRICES", prices)
    console.log("FULFILLED BY SUPPLIER NAME: ", item.fulfilled_by_product?.supplier.name)


    const [quantity, setQuantity] = useState(item.quantity)
    const [isDeleted, setIsDeleted] = useState(false)

    // If no prices are available, item is cancellable
    const connectedVendors = []
    const allVendors = Object.keys(prices)
    for (const [key, val] of Object.entries(prices)) {
        if (val.price) connectedVendors.push(key)
    }

    function updateQuantity(e) {
        // Prevent negative quantities
        if (e.target.value < 1) return;

        // Patch quantity update to /orderitem=item.id
        const PATCH_OPTIONS = {
            'method': 'PATCH',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'quantity': e.target.value,
            })
        }
        fetch(`/api/v1/orderitem=${item.id}`, PATCH_OPTIONS)
            .then(resp => resp.json())
            .then(data => {
                console.log(data)
                setQuantity(data.quantity)
            })
    }

    function deleteItem() {
        fetch(`/api/v1/orderitem=${item.id}`, { 'method': 'DELETE' })
            .then(() => setIsDeleted(true))
    }

    if (isDeleted) return null;

    return (
        <Table.Row >
            <Table.Cell>
                <p>{item.canonical_product.manufacturer.name} {item.canonical_product.name}</p>
                <Image size='tiny' src={item.canonical_product.image_link.split('/').slice(-2).join('/')}/>
                {/* <p style={{ color: 'red' }}>order_item_id={item.id}</p> */}
                {/* <p style={{ color: 'red' }}>canonical_product_id={item.canonical_product_id}</p> */}
                <SupplierProductsTable order_item={item} prices={prices} />
            </Table.Cell>
            <Table.Cell>
                <Form>
                    <Form.Field>
                        <Input type="number" value={quantity} onChange={updateQuantity} />
                    </Form.Field>
                </Form>
            </Table.Cell>
            <Table.Cell>
                <p>{item.price ? item.price.toFixed(2) : <i>pending</i>}</p>
                <small>{item.fulfilled_by_product?.supplier.name}</small>
            </Table.Cell>
            <Table.Cell>
                {
                    connectedVendors.length > 0
                    ? (
                        item.price ? (item.price * item.quantity).toFixed(2) : <i>pending</i>
                    )
                    : (<Link to='/account/vendors'>
                            <Popup trigger={<Icon circular name='exclamation' />}>
                                <Popup.Content>
                                    This item is not available from any of your connected vendors 
                                    and will be cancelled at checkout. 
                                    To order, connect one of the following vendors: {allVendors.join(', ')} 
                                </Popup.Content>
                            </Popup>
                            <i>Connect Vendors</i>
                        </Link>)
                }
            </Table.Cell>
            <Table.Cell>
                <Icon className='delete-icon' name='trash alternate outline' onClick={deleteItem} />
            </Table.Cell>
        </Table.Row>
    )
}