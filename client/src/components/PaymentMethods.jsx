import { useEffect } from "react";
import { useOutletContext } from "react-router-dom";

export default function PaymentMethods() {
    const { setMenuActive } = useOutletContext()
    useEffect(() => setMenuActive("payment"), [])

    return (
        <h2>TODO: Payment Methods</h2>
    )
}