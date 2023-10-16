import { useOutletContext } from "react-router-dom";
import { Outlet, Link } from "react-router-dom";
import { Menu } from "semantic-ui-react";

export default function AccountOutlet() {
    const { user, setUser } = useOutletContext();

    return (
        <>
          <Menu>
            <Link to='/account/vendors'>Manage Vendors</Link>
            <Link to='/account/orders'>View Orders</Link>
          </Menu>

          <Outlet context={{user, setUser}} />
        </>
    )
}