import { useLoaderData } from "react-router-dom";
import { Icon, Label, Table } from "semantic-ui-react";

export default function ManageVendorsPage() {

    const { supplierAccounts, suppliers } = useLoaderData();

    function connectVendor(supplierID) {
        console.log("TODO: connect vendor with id ", supplierID)
    }

    console.log("supplierAccounts", supplierAccounts)
    console.log("suppliers", suppliers)
    console.log(supplierAccounts.map(sa => sa.supplier.name))

    const connectedVendorIds = supplierAccounts.map(sa => sa.supplier.id)

    return (
        <div>
            <h2>Manage Vendors</h2>
            <h3>All Vendors</h3>
            <Table celled>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Vendor</Table.HeaderCell>
                        <Table.HeaderCell>Status</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        suppliers.filter(s => s.preferred).map(s => {
                            return (
                                <Table.Row key={s.id}>
                                    <Table.Cell>
                                        <Label color='green' ribbon>Preferred</Label>
                                        {s.name}
                                    </Table.Cell>
                                    <Table.Cell><Icon name='checkmark' color='green' /></Table.Cell>
                                </Table.Row>
                            )
                        }

                        )
                    }
                    {
                        suppliers.filter(s => !s.preferred).map(s => {
                            return (
                                <Table.Row key={s.id}>
                                    <Table.Cell>
                                        {s.name}
                                    </Table.Cell>
                                    
                                    <Table.Cell>
                                        {
                                            connectedVendorIds.includes(s.id)
                                            ? <Icon name='checkmark' color='green' />
                                            : <button onClick={() => connectVendor(s.id)}>Connect Vendor</button>
                                        }
                                    </Table.Cell>
                                </Table.Row>
                            )
                        })
                    }
                </Table.Body>
            </Table>
            
        </div>
    )
}