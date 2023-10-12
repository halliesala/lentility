import { Icon, Table, Input, Form } from 'semantic-ui-react';
import { useState } from 'react';
import SupplierProductsTable from './SupplierProductsTable';

export default function CartRow({ item, prices }) {

    console.log("CART ROW ITEM", item)
    console.log("CART ROW PRICES", prices)

    const [quantity, setQuantity] = useState(item.quantity)
    const [isDeleted, setIsDeleted] = useState(false)

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
        fetch(`/api/v1/orderitem=${item.id}`, {'method': 'DELETE'})
        .then(() => setIsDeleted(true))
    }

    if (isDeleted) return null;

    return (
        <Table.Row >
            <Table.Cell>
                <p>{item.canonical_product.manufacturer.name} {item.canonical_product.name}</p>
                <SupplierProductsTable order_item={item} prices={prices} />
            </Table.Cell>
            <Table.Cell>
                <Form>
                    <Form.Field>
                        <Input type="number" value={quantity} onChange={updateQuantity}/>
                    </Form.Field>
                </Form>                
            </Table.Cell>
            <Table.Cell>{item.price ? item.price.toFixed(2) : <i>pending</i>}</Table.Cell>
            <Table.Cell>
                {item.price ? (item.price * item.quantity).toFixed(2): <i>pending</i>}
            </Table.Cell>
            <Table.Cell>
                <Icon className='delete-icon' name='trash alternate outline' onClick={deleteItem} />
            </Table.Cell>
        </Table.Row>
    )
}