import { Card, Input, Form } from 'semantic-ui-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function ProductCard({ cp, user }) {

    const [quantity, setQuantity] = useState(1)


    function addToCart() {
        console.log('TODO: add to cart')
        // Post item to /additemtocart with user_id, canonical_product_id, and quantity
        const POST_OPTIONS = {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'user_id': user.id,
                'canonical_product_id': cp.id,
                'quantity': quantity,
            })
        }
        fetch('/api/v1/cart', POST_OPTIONS)
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })

    }

    return (
        <Card key={cp.id} >
            <h2>{cp.name}</h2>
            <h3>{cp.manufacturer.name}</h3>
            <h3>{cp.manufacturer_sku}</h3>
            <ul>
                {
                    cp.products.map(p => {
                        return (
                            <li key={p.id}>{p.supplier.name}</li>
                        )
                    })
                }
            </ul>
            {
                user
                    ? <button onClick={() => addToCart(cp.id)}>Quick Add</button>
                    // TODO: Item should be added to cart upon logging in
                    : <button><Link to='/login'>Login to add to cart</Link></button>
            }
            <Form>
                <Form.Field >
                    <Input type='number' value={quantity} onChange={e => setQuantity(Math.max(e.target.value, 0))} />
                </Form.Field>
            </Form>

        </Card>
    )
}