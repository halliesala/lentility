import { useLoaderData, useOutletContext } from "react-router-dom";
import { useEffect } from "react";
import { Card } from "semantic-ui-react";

export default function AddressesPage() {

    const { addresses } = useLoaderData();
    const {user, setUser, setMenuActive} = useOutletContext();
    useEffect(() => setMenuActive("addresses"), [])

    return (
        <>
            <h2>Manage Addresses</h2>
            <Card style={{ width: '80vw', textAlign: 'left', padding: '5%' }}>
                An Address Card
            </Card>

        </>
    )

}