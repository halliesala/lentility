import { useLoaderData, useOutletContext } from 'react-router-dom';
import { Grid, Pagination } from 'semantic-ui-react';
import { useState } from 'react';
import ProductCard from './ProductCard';
import SearchBar from './SearchBar';
import SearchTag from './SearchTag';

export default function ShopPage() {
    const { canonicalProducts } = useLoaderData()
    const { user, setUser } = useOutletContext()

    // Pagination
    const [itemsPerPage, setItemsPerPage] = useState(16)
    const [activePage, setActivePage] = useState(1)  
    
    // All active search bar queries
    const [searchTerms, setSearchTerms] = useState([])

    // Current search bar query
    const [searchBarContent, setSearchBarContent] = useState('')
    
    // Pagination    
    function removeTag(tag) {
        console.log("TODO: Remove tag")
        setSearchTerms(searchTerms.filter(t => t !== tag))
    }
    
    const displayItems = canonicalProducts
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

    console.log("displayItems", displayItems)
    
    // Pagination numbers -- ex., "Showing 1-16 of 32 items"
    const firstItemNum = (activePage-1) * itemsPerPage + 1;
    const lastItemNum = Math.min(displayItems.length, (activePage * itemsPerPage));
    const totalItems = displayItems.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage)
        
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
                    displayItems
                    .slice((activePage - 1) * itemsPerPage, activePage * itemsPerPage)
                }
            </Grid>
            <div className="pagination-div">
                <PaginationBar 
                    activePage={activePage} 
                    setActivePage={setActivePage} 
                    totalPages={totalPages}
                />
                <p>Showing {firstItemNum}-{lastItemNum} of {totalItems} items</p>
            </div>
        </>
    )
}

function PaginationBar({ activePage, setActivePage, totalPages}) {

    function handlePageChange(e) {
        setActivePage(e.target.getAttribute('value'))
    }

    return (
        <Pagination 
            onPageChange={handlePageChange}
            totalPages={totalPages} 
            activePage={activePage} 
        />
    )
}