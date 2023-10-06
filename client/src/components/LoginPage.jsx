import { useState } from 'react';
import LoginForm from './LoginForm';

export default function LoginPage({ user, setUser }) {
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
            <h1>Hi, {user.first_name} {user.last_name}</h1>
            <p>You are logged in as {user.email}</p>
            <button onClick={handleLogout}>Logout</button>
        </>
    )

    
}