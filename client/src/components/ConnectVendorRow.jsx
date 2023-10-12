import { Table, Label, Icon } from "semantic-ui-react"
import { useState } from "react";

export default function ConnectVendorRow({ supplier, connectedVendorIds } ) {

    const [connectedVendors, setConnectedVendors] = useState(connectedVendorIds)

    function connectVendor(supplierID) {
        console.log("TODO: connect vendor with id ", supplierID)
        const POST_OPTIONS = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                'vendor_id': supplierID,
                'username': 'testuser',
                'password': 'password',
             })
        }
        fetch('/api/v1/connectvendor', POST_OPTIONS)
        .then(resp => resp.json())
        .then(data => {
            setConnectedVendors([...connectedVendors, supplierID])
            console.log(data)
        })
    }


    return (
        <Table.Row>
            <Table.Cell>
                <Label color='green' ribbon>Preferred</Label>
                {supplier.name}
            </Table.Cell>
            <Table.Cell>
                {
                    connectedVendors.includes(supplier.id)
                    ? <Icon name='checkmark' color='green' />
                    : <button onClick={() => connectVendor(supplier.id)}>Connect Vendor</button>
                }
            </Table.Cell>
        </Table.Row>
    )
}