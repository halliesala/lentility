import { useOutletContext } from "react-router-dom";
import { useEffect } from "react";
import { Icon } from "semantic-ui-react";

export default function Logout() {
    const { user, setUser } = useOutletContext()

    useEffect(() => {
        fetch('/api/v1/logout', { 'method': 'DELETE' })
            .then(resp => {
                if (resp.ok) {
                    setUser(null)
                }
            })
    }, [])

    if (user) {
        return (
        <Icon loading name='spinner' size='huge' />
        )
    }

    return (
        <div>
            <h2>You have been logged out.</h2>
        </div>
    )
}