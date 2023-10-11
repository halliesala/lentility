import { Icon, Table, Input, Form } from 'semantic-ui-react';
import { useState } from 'react';

export default function CartRow({ item }) {

    console.log("CART ROW ITEM", item)

    const [quantity, setQuantity] = useState(item.quantity)

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

    return (
        <Table.Row >
            <Table.Cell>
                <p>{item.canonical_product.manufacturer.name} {item.canonical_product.name}</p>
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
                <Icon name='trash alternate outline' />
            </Table.Cell>
        </Table.Row>
    )
}