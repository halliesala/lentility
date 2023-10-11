import { useLoaderData, useOutletContext } from 'react-router-dom';
import { Grid } from 'semantic-ui-react';
import { useState } from 'react';
import ProductCard from './ProductCard';
import SearchBar from './SearchBar';
import SearchTag from './SearchTag';

export default function ShopPage() {
    const { canonicalProducts } = useLoaderData()
    const { user, setUser } = useOutletContext()

    // All active search bar queries
    const [searchTerms, setSearchTerms] = useState([])

    // Current search bar query
    const [searchBarContent, setSearchBarContent] = useState('')

    console.log("Shop Page", canonicalProducts)
    
    function removeTag(tag) {
        console.log("TODO: Remove tag")
        setSearchTerms(searchTerms.filter(t => t !== tag))
    }

    return (
        <>
            <SearchBar 
                searchBarContent={searchBarContent} 
                setSearchBarContent={setSearchBarContent} 
                searchTerms={searchTerms} 
                setSearchTerms={setSearchTerms} 
            />
            
            <div className="search-sort-tags">
                {
                    searchTerms.map(st => {return <SearchTag key={st} tag={st} removeTag={removeTag} />})
                }
            </div>
            
            <Grid columns={4}>
                {
                    canonicalProducts
                    .filter(cp => {
                        // Return true if cp (name, manufacturer, sku, or suppliers) matches ALL search terms
                        // strip non-alphanumeric characters and make lowercase
                        const corpus = ('' 
                            + cp.name 
                            + cp.manufacturer.name 
                            + cp.manufacturer_sku)
                            .toLowerCase().replace(/[^a-z0-9]/g, '')
                        return searchTerms.every(st => corpus.includes(st)) && corpus.includes(searchBarContent.toLowerCase().replace(/[^a-z0-9]/g, ''))
                    })
                    .map(cp => {
                        return (
                            <Grid.Column key={cp.id}>
                                <ProductCard user={user} cp={cp} />
                            </Grid.Column>
                        )
                    })
                }
            </Grid>
        </>
    )
}