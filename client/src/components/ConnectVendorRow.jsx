import { Table, Label, Icon, Form, Card } from "semantic-ui-react"
import { useState } from "react";

export default function ConnectVendorRow({ supplier, connectedVendorIds } ) {

    const [connectedVendors, setConnectedVendors] = useState(connectedVendorIds)
    const [displayForm, setDisplayForm] = useState(false)

    


    return (
        <Table.Row>
            <Table.Cell>
                {
                    supplier.preferred
                    ? <Label color='green' ribbon>Preferred</Label>
                    : null
                }
                {supplier.name}
            </Table.Cell>
            <Table.Cell style={{width: '50%'}}>
                {
                    connectedVendors.includes(supplier.id)
                    ? <Icon name='checkmark' color='green' />
                    : (
                        displayForm
                        ? <ConnectVendorForm 
                            setDisplayForm={setDisplayForm} 
                            supplierID={supplier.id} 
                            connectedVendors={connectedVendors} 
                            setConnectedVendors={setConnectedVendors}
                          />
                        : <button onClick={() => setDisplayForm(true)}>Connect Vendor</button>
                      )   
                }
            </Table.Cell>
        </Table.Row>
    )
}



function ConnectVendorForm({ supplierID, setDisplayForm, connectedVendors, setConnectedVendors }) {
    const BLANK_FORM_DATA = {
        'username': '',
        'password': '',
    }
    const [formData, setFormData] = useState(BLANK_FORM_DATA)

    function handleChange(e) {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    function connectVendor() {
        console.log("TODO: connect vendor with id ", supplierID)
        const POST_OPTIONS = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                'vendor_id': supplierID,
                'username': formData['username'],
                'password': formData['password'],
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
        <>
            <Card centered style={{width: '100%', padding: '5%', textAlign: 'center'}}>
                
                <Card.Description><Icon name='info circle' />Enter your existing login credentials for this vendor.</Card.Description>
                <Card.Description>Questions? Contact Lentility customer support anytime.</Card.Description>
            </Card>
            <Form onSubmit={() => connectVendor()}>
                <Form.Field>
                    <label>Username</label>
                    <input name='username' type='text' value={formData['username']} onChange={handleChange}/>
                </Form.Field>
                <Form.Field>
                    <label>Password</label>
                    <input name='password' type='password' value={formData['password']} onChange={handleChange}/>
                </Form.Field>
                <input type='submit' value='Connect Vendor' />
            </Form>
            <button className='cancel-button' onClick={() => setDisplayForm(false)}>Cancel</button>
        </>
    )
}