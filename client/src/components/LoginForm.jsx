import { useState } from 'react';
import { Form, Input } from 'semantic-ui-react';
import { useNavigate } from 'react-router-dom';

export default function Login({ setLoginError, setUser }) {

    const BLANK_FORM_DATA = {
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

    function login(e) {
        e.preventDefault()
        const POST_OPTIONS = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }
        fetch('/api/v1/login', POST_OPTIONS)
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
            setUser(data.user)
        })
    }

    return (
        <>
            <Form  onSubmit={login}>
                <Form.Field>
                    <label>Email</label>
                    <Input type='text' name='email' onChange={handleChange} value={formData.email} />
                </Form.Field>
                <Form.Field>
                    <label>Password</label>
                    <Input type='password' name='password' onChange={handleChange} value={formData.password} />
                </Form.Field>
                <input type='submit' value='Login'/>
            </Form>
        </>
    )
}
