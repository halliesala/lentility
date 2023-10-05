import { useState } from 'react';
import LoginForm from './LoginForm';

export default function LoginPage({ user }) {
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
                <LoginForm setLoginError={setLoginError} />
            </>
        )
    }

    // If logged in, display welcome message
    return (
        <>
            <h1>Welcome, {user.name}</h1>
            <p>You are logged in as {user.email}</p>
        </>
    )

    
}