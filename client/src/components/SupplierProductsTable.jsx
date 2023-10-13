import { useEffect, useState } from "react"
import { useOutletContext } from "react-router-dom"
import { Icon, Table, Dimmer } from "semantic-ui-react"

export default function SupplierProductsTable({order_item, prices}) {
    const { user, setUser } = useOutletContext()
    const [pricesLastRefreshed, setPricesLastRefreshed] = useState(new Date())
    const [hideTable, setHideTable] = useState(true)

    const [priceInfo, setPriceInfo] = useState(prices)

    const cp_id = order_item.canonical_product_id

    // Get prices for cp_id and practice_id
    function refreshPrice() {
        fetch(`/api/v1/getpriceinfo/cp=${cp_id}/practice=${user.practice_id}`)
        .then(resp => resp.json())
        .then(data => {
            setPriceInfo(data)
            setPricesLastRefreshed(new Date())
        })
    }

    return (
        <>
            <button className='show-detail-button' onClick={() => setHideTable(!hideTable)}>{hideTable ? "Show Details" : "Hide Details"}</button>
            {/* <Icon name={hideTable ? 'angle double down' : 'angle double up'} className='show-detail-button' onClick={() => setHideTable(!hideTable)} hidden={hideTable} /> */}
            <div className='detail-div' hidden={hideTable}>
                <Table celled >
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Supplier</Table.HeaderCell>
                            <Table.HeaderCell>Price</Table.HeaderCell>
                            <Table.HeaderCell>Free Shipping Threshold</Table.HeaderCell>
                            <Table.HeaderCell>Shipping Cost</Table.HeaderCell>
                            <Table.HeaderCell>Days to Ship</Table.HeaderCell>
                            <Table.HeaderCell>Stock</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {
                            order_item.canonical_product.suppliers
                            .map(s => {
                                return (
                                    <Table.Row key={s.id} >
                                        <Table.Cell>
                                            <p>{s.name}</p>
                                            <p>{priceInfo?.[s.name]?.supplier_sku}</p>
                                            <p style={{color:'red'}}>product_id={priceInfo?.[s.name]?.product_id}</p>
                                        </Table.Cell>
                                        <Table.Cell>{(priceInfo?.[s.name]?.price)?.toFixed(2) ?? 'Connect Vendor'}</Table.Cell>
                                        <Table.Cell>{priceInfo?.[s.name]?.free_shipping_threshold ?? 'Connect Vendor'}</Table.Cell>
                                        <Table.Cell>{priceInfo?.[s.name]?.shipping_cost ?? 'Connect Vendor'}</Table.Cell>   
                                        <Table.Cell>{priceInfo?.[s.name]?.days_to_ship ?? 'Connect Vendor'}</Table.Cell> 
                                        <Table.Cell>{priceInfo?.[s.name]?.stock ?? 'Connect Vendor'}</Table.Cell>
                                    </Table.Row>
                                )
                            })
                        }
                    </Table.Body>
                </Table>
                <button onClick={refreshPrice}>Refresh Prices</button>
                <p>prices last refreshed: {pricesLastRefreshed.toLocaleString()}</p>
            </div>
        </>
    )
}