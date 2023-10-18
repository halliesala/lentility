import { useLoaderData, useOutletContext } from "react-router-dom";
import { useEffect, useState } from "react";
import { Card, Checkbox } from "semantic-ui-react";

export default function AddressesPage() {

    const { addresses } = useLoaderData();
    const {user, setUser, setMenuActive} = useOutletContext();
    const [primary, setPrimary] = useState()

    useEffect(() => {
        setMenuActive("addresses")
        setPrimary(addresses.filter(a => a.is_primary_shipping)[0].id)
    }, [])

    return (
        <>
            <h2>Manage Addresses</h2>
            {
                addresses.map(address => {
                    return (
                        <AddressCard key={address.id} address={address} primary={primary} setPrimary={setPrimary} />
                    )
                })
            }
        </>
    )

}

function AddressCard({ address, primary, setPrimary }) {

    // const [checked, setChecked] = useState(address.id === primary)

    function handleChange(e, data) {
        console.log("TODO: update primary shipping address")
        const POST_OPTIONS = {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'address_id': address.id
            })
        }
        fetch('/api/v1/updateprimaryshippingaddress', POST_OPTIONS)
            .then(res => res.json())
            .then(data => {
                console.log(data)
                setPrimary(address.id)
                // setChecked(true)
            })
    }

    return (
        <Card style={{ width: '80vw', textAlign: 'left', padding: '5%' }}>
            <p style={{color: 'red'}}>{address.id}</p>
            <Card.Content>
                <Card.Description>{address.line_1}</Card.Description>
                <Card.Description>{address.line_2}</Card.Description>
                <Card.Description>{address.city}, {address.us_state} {address.zip}</Card.Description>
                <Checkbox label="Primary Shipping Address" checked={address.id === primary} onChange={handleChange}/>
            </Card.Content>
        </Card>
    )
}