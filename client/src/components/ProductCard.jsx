import { Card, Input, Form, Image, Label, Segment, Icon } from 'semantic-ui-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function ProductCard({ cp, user }) {

    const [quantity, setQuantity] = useState(1)

    const colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'grey', 'black']


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
        <Card key={cp.id} 
            color={colors[cp.manufacturer.id]}
            // style={{ width: '40vh'}}
        >
            <Image
                src={cp.image_link.split('/').slice(-2).join('/')} 
                label={{
                    color: colors[cp.manufacturer.id],
                    content: cp.manufacturer.name,
                    attached: 'top',
                }}>
            </Image>
\            <Card.Header as='h2'>{cp.name}</Card.Header>
            <Card.Meta>{cp.manufacturer_sku}</Card.Meta>
            <div style={{height: '10vh'}}>
                {
                    cp.products
                    .sort((a, b) => 0.5 - Math.random())
                    .map(p => {
                        return (
                            <Card.Description key={p.id}>{p.supplier.name}</Card.Description>
                        )
                    })
                }
            </div>
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