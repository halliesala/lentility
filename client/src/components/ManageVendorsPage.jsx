import { useLoaderData } from "react-router-dom";
import { Icon, Label, Table } from "semantic-ui-react";
import ConnectVendorRow from "./ConnectVendorRow";

export default function ManageVendorsPage() {

    const { supplierAccounts, suppliers } = useLoaderData();



    console.log("supplierAccounts", supplierAccounts)
    console.log("suppliers", suppliers)
    console.log(supplierAccounts.map(sa => sa.supplier.name))

    const connectedVendorIds = supplierAccounts.map(sa => sa.supplier.id)

    return (
        <div>
            <h2>Manage Vendors</h2>
            <Table celled>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Vendor</Table.HeaderCell>
                        <Table.HeaderCell>Status</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        suppliers
                            .filter(s => s.preferred)
                            .map(s => <ConnectVendorRow 
                                key={s.id} 
                                supplier={s} 
                                connectedVendorIds={connectedVendorIds} 
                            />)
                    }
                    {
                        suppliers
                            .filter(s => !s.preferred)
                            .map(s => <ConnectVendorRow 
                                key={s.id} 
                                supplier={s} 
                                connectedVendorIds={connectedVendorIds} 
                            />)
                    }
                </Table.Body>
            </Table>

        </div>
    )
}