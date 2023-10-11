import { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Form, Input } from 'semantic-ui-react';

export default function ApplyPage() {

    const {user, setUser} = useOutletContext()

    const BLANK_FORM_DATA = {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
    }
    const [formData, setFormData] = useState(BLANK_FORM_DATA);
    const [loginError, setLoginError] = useState(false);

    function handleChange(e) {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    // Create new user with role 'admin'
    function handleSubmitNewUser(e) {
        e.preventDefault()
        const POST_OPTIONS = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }
        fetch('/api/v1/apply', POST_OPTIONS)
        .then(res => res.json())
        .then(data => {
            setUser(data)
            setFormData(BLANK_FORM_DATA)
        })
    }

    function handleQuit() {
        const PATCH_OPTIONS = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({role: 'disgruntled former employee'})
        }
        fetch('/api/v1/apply', PATCH_OPTIONS)
        .then(res => res.json())
        .then(data => {
            setUser(data)
            console.log(data)
        })
    }


    // Patch existing user with role 'admin'
    function handleSubmitExistingUser() {
        const PATCH_OPTIONS = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({role: 'admin'})
        }
        fetch('/api/v1/apply', PATCH_OPTIONS)
        .then(res => res.json())
        .then(data => {
            setUser(data)
            console.log(data)
        })
    }

    // If user account already exists and has role 'admin'
    if (user && user.role === 'admin') {
        return (
            <>
                <p>Hey, {user.first_name}! Thank you for being a part of the Lentility team!</p>
                <button onClick={handleQuit}>Quit</button>
            </>
        )
    } else if (user && user.role === 'disgruntled former employee') {
        return (
            <>
                <p>Sorry to see you go. We hope you'll consider rejoining the Lentility team as a Business Operations Analyst!</p>
                <button onClick={handleSubmitExistingUser}>Withdraw Resignation</button>
            </>
        )
    } else if (user) {
        return (
            <>
                <p>Hey, {user.first_name}! Love Lentility as much as we do? Join our team as a Business Operations Analyst!</p>
                <button onClick={handleSubmitExistingUser}>Apply</button>
            </>
            
        )   
    }

    
    return (
        <>
            <p>Thank you for your interest in joining the Lentility team as a Business Operations Analyst!</p>
            <p>Please fill out the application below.</p>
            {
                loginError
                ? <p>Error creating account.</p>
                : null
            }
            <Form onSubmit={handleSubmitNewUser}>
                <Form.Field>
                    <label>First Name</label>
                    <Input type='text' name='first_name' onChange={handleChange} value={formData.first_name} />
                </Form.Field>
                <Form.Field>
                    <label>Last Name</label>
                    <Input type='text' name='last_name' onChange={handleChange} value={formData.last_name} />
                </Form.Field>
                <Form.Field>
                    <label>Email</label>
                    <Input type='text' name='email' onChange={handleChange} value={formData.email} />
                </Form.Field>
                <Form.Field>
                    <label>Password</label>
                    <Input type='password' name='password' onChange={handleChange} value={formData.password} />
                </Form.Field>
                <input type='submit' value='Apply' />
            </Form>
        </>
    )
    
}