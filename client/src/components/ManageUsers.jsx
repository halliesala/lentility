import { useEffect } from "react";
import { useOutletContext, useLoaderData } from "react-router-dom";
import { Card, Checkbox, Table, Icon } from "semantic-ui-react";


export default function PaymentMethods() {
    const { users } = useLoaderData()
    const { setMenuActive } = useOutletContext()
    useEffect(() => setMenuActive("users"), [])

    return (
        <>
            <h2>Users</h2>
            <Table>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>ID</Table.HeaderCell>
                        <Table.HeaderCell>Name</Table.HeaderCell>
                        <Table.HeaderCell>Email</Table.HeaderCell>
                        <Table.HeaderCell>Primary</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        users.map(u => {
                            return (
                                <Table.Row key={u.id}>
                                    <Table.Cell>{u.id}</Table.Cell>
                                    <Table.Cell>{u.first_name} {u.last_name}</Table.Cell>
                                    <Table.Cell>{u.email}</Table.Cell>
                                    <Table.Cell>{u.is_primary ? <Icon color='green' name='check' /> : null }</Table.Cell>
                                </Table.Row>
                            )
                        })
                    }
                </Table.Body>
            </Table>
        </>
    )
}