import { Button, Form, Grid, Input } from "semantic-ui-react";
import { useState } from "react";

export default function SearchBar({ searchBarContent, setSearchBarContent, searchTerms, setSearchTerms, resetPagination}) {

    function handleChange(e) {
        setSearchBarContent(e.target.value)
        resetPagination()
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
            <Grid>
                <Grid.Column width={14}>
                    <Form.Field  >
                        <Input type='text' placeholder='red lentils...' value={searchBarContent} onChange={handleChange}/>
                    </Form.Field>
                </Grid.Column>
                <Grid.Column width={1}>
                    <input className='search-bar-submit' type='submit' value='Search'/>
                </Grid.Column>
            </Grid>

        </Form>
    )
}