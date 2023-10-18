import { useEffect } from "react";
import { useOutletContext } from "react-router-dom";

export default function DataPage( ) {
    const { setMenuActive } = useOutletContext()
    useEffect(() => setMenuActive("stats"), [])

    return (
        <>
            <h2>Data</h2>
            <p>TODO: Add data page</p>
        </>
    )
}