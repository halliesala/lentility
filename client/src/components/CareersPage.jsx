import { useEffect, useState } from 'react'
import { Container, Header } from 'semantic-ui-react'
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
            <h1>Roles We're Hiring For</h1>
            <Container text>
                <Header as='h3'>Business Operations Analyst</Header>
                <button><Link to='/careers/apply'>Apply</Link></button>
                {
                    jobDescription
                    ? jobDescription.map((line, idx) => <p key={idx}>{line}</p>)
                    : null
                }
            </Container>
        </>
    )
}