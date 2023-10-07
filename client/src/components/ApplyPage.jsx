import { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Form, Input } from 'semantic-ui-react';

export default function ApplyPage() {

    const {user, setUser} = useOutletContext()
    console.log("User: ", user)

    const BLANK_FORM_DATA = {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
    }
    const [formData, setFormData] = useState(BLANK_FORM_DATA);

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
            console.log(data)
            setFormData(BLANK_FORM_DATA)
        })
    }

    // Patch existing user with role 'admin'
    function handleSubmitExistingUser(e) {
        e.preventDefault()
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
            console.log(data)
        })
    }

    // If user account already exists and has role 'admin'
    if (user && user.role === 'admin') {
        return (
            <p>Hey, {user.first_name}! You've already applied and been accepted. Get back to work!</p>
        )
    } else if (user) {
        return (
            <>
                <p>Hey, {user.first_name}! Love Lentility as much as we do? Join our team as a Business Operations Analyst!</p>
                <Form onSubmit={handleSubmitExistingUser}>
                    <Form.Field>
                        <Input type='submit' value='Apply' />
                    </Form.Field>
                </Form>
            </>
            
        )   
    }

    
    return (
        <>
            <p>Thank you for your interest in joining the Lentility team as a Business Operations Analyst!</p>
            <p>Please fill out the application below.</p>
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