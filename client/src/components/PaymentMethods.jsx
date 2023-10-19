import { useEffect } from "react";
import { useOutletContext, useLoaderData } from "react-router-dom";
import { Table, Icon } from "semantic-ui-react";

export default function PaymentMethods() {
    const { paymentMethods } = useLoaderData()
    const { setMenuActive } = useOutletContext()
    useEffect(() => setMenuActive("payment"), [])

    return (
        <>
            <h2>TODO: Payment Methods</h2>
            <Table >
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Payment Method Nickname</Table.HeaderCell>
                        <Table.HeaderCell>Primary?</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        paymentMethods.map(p => {
                            return (
                                <Table.Row key={p.id}>
                                    <Table.Cell>
                                        <Icon name='credit card' />
                                        {p.nickname}
                                    </Table.Cell>
                                    <Table.Cell>{p.is_primary ? <Icon color='green' name='check' /> : null }</Table.Cell>
                                </Table.Row>
                            )
                        })
                    }
                </Table.Body>
            </Table>
        </>
    )
}