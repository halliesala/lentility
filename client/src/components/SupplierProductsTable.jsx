import { useOutletContext } from "react-router-dom"

export default function SupplierProductsTable({cp}) {
    const { user, setUser } = useOutletContext()


    return (
        <table>
            <thead>
                <tr>
                    <th>Supplier</th>
                    <th>Price</th>
                    <th>Free Shipping Threshold</th>
                </tr>
            </thead>
            <tbody>
                {
                    cp.products.map(p => {
                        return (
                            <tr key={p.id}>
                                <td>{p.supplier.name}</td>
                            </tr>
                        )
                    })
                }
            </tbody>
        </table>
    )
}