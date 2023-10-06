import { useState } from 'react';
import LoginForm from './LoginForm';
import { useOutletContext } from 'react-router-dom';

export default function LoginPage() {
    
    const {user, setUser} = useOutletContext();
    
    const [loginError, setLoginError] = useState(false);

    // If not logged in, display login form
    // If login error, display error message
    if (!user) {
        return (
            <>
                {
                    loginError
                    ? <p>Invalid email or password.</p>
                    : null
                }
                <LoginForm setLoginError={setLoginError} setUser={setUser} />
            </>
        )
    }

    function handleLogout() {
        fetch('/api/v1/logout', {'method': 'DELETE'})
        .then(resp => {
            if (resp.ok) {
                setUser(null)
            }
        })
    }

    // If logged in, display welcome message
    return (
        <>
            <p>You are logged in as {user.email}</p>
        </>
    )

    
}

