import { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Form, Input } from 'semantic-ui-react';


export default function SignUpPage() {
    const {user, setUser} = useOutletContext()
    const [existingPractice, setExistingPractice] = useState(false)

    const BLANK_FORM_DATA = {
        practice_name: "",
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

    // Create new practice and associated user with role 'lentist'
    function handleSubmit(e) {
        e.preventDefault()
        const POST_OPTIONS = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }
        
        fetch('/api/v1/signup', POST_OPTIONS)
        .then(res => {
            if (res.ok) {
                setFormData(BLANK_FORM_DATA)
                setLoginError(false)
            } else {
                setLoginError(true)
            }
            return res.json()
        })
        .then(data => {
            setUser(data)
            setFormData(BLANK_FORM_DATA)
        })
    }

    function handleClick() {
        setExistingPractice(!existingPractice)
    }

    // If practice already has an account, new accounts should be created via practice controls
    if (user) {
        return (
            <>
                <h2>Sign Up</h2>
                <p>Create additional user accounts for your practice via Account Settings.</p>
            </>
        )
    }
    if (existingPractice) {
        return (
            <>
                <h2>Sign Up</h2>
                <button onClick={handleClick}>My office is new to Lentility.</button>
                <p>Create additional user accounts for your practice via Account Settings.</p>
            </>
        )
    }
    

    // Otherwise, show new practice signup form
    return (
        <>
            <h2>Sign Up</h2>
            {
                loginError
                ? <p>Error creating account.</p>
                : null
            }
            <button onClick={handleClick}>My office already has a Lentility account.</button>
            <Form onSubmit={handleSubmit}>
                <Form.Field>
                    <label>Practice Name</label>
                    <Input type='text' name='practice_name' onChange={handleChange} value={formData.practice_name} />
                </Form.Field>
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
                <input type='submit' value='Sign Up' />
            </Form>
        </>
    )
}

