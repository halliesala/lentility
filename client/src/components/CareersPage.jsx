import { useEffect, useState } from 'react'
import { Card, Header } from 'semantic-ui-react'
import { Link } from 'react-router-dom'

export default function CareersPage() {

    const [jobDescription, setJobDescription] = useState("")

    // Read job description from file
    useEffect(() => {
        fetch("/job_description.txt")
        .then(resp => resp.text())
        .then(text => {
            const lines = text.split("\n")
            setJobDescription(lines)
        })
    }, [])
    
    

    return (
        <>
            <h2>Roles We're Hiring For</h2>
            <Card style={{ width: '80vw', textAlign: 'left', padding: '5%' }}>
                <Header as='h3'>
                    Business Operations Analyst
                    <Link className="apply-link" to='/careers/apply'>Apply</Link>
                </Header>
                {
                    jobDescription
                    ? jobDescription.map((line, idx) => {
                        return (
                            line.startsWith("--")
                            ? <li key={idx}>{line.slice(2)}</li>
                            : <p key={idx}>{line}</p>
                        )   
                    })
                    : null
                }
            </Card>
        </>
    )
}