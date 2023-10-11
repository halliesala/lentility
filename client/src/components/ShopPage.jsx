import { Link, useLoaderData, useOutletContext } from 'react-router-dom';
import { Card, Input, Form, Grid } from 'semantic-ui-react';
import { useState } from 'react';
import ProductCard from './ProductCard';

export default function ShopPage() {
    const { canonicalProducts } = useLoaderData()
    const { user, setUser } = useOutletContext()

    console.log("Shop Page", canonicalProducts)
    
    

    return (
        <>
            <Grid columns={4}>
                {
                    canonicalProducts.map(cp => {
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