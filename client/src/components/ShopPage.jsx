import { Link, useLoaderData, useOutletContext } from 'react-router-dom';
import { Card, Input, Form } from 'semantic-ui-react';
import { useState } from 'react';
import ProductCard from './ProductCard';

export default function ShopPage() {
    const { canonicalProducts } = useLoaderData()
    const { user, setUser } = useOutletContext()

    console.log("Shop Page", canonicalProducts)
    
    

    return (
        <>
            {
                canonicalProducts.map(cp => {
                    return <ProductCard key={cp.id} user={user} cp={cp} />
                })
            }
        </>
    )
}