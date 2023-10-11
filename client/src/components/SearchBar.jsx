import { Button, Form, Input } from "semantic-ui-react";
import { useState } from "react";

export default function SearchBar({ searchBarContent, setSearchBarContent, searchTerms, setSearchTerms}) {

    function handleChange(e) {
        setSearchBarContent(e.target.value)
    }
    
    function addSearchTerm(e) {
        e.preventDefault()
        // No duplicate tags
        if (searchBarContent in searchTerms) {
            return
        }
        setSearchTerms([...searchTerms, searchBarContent])
        setSearchBarContent('')
    }
    return (
        <Form onSubmit={addSearchTerm}>
            <Form.Field  >
                <Input type='text' placeholder='red lentils...' value={searchBarContent} onChange={handleChange}/>
            </Form.Field>
            <input className='search-bar-submit' type='submit' value='Search'/>
        </Form>
    )
}