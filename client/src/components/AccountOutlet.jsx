import { useOutletContext } from "react-router-dom";
import { Outlet, Link } from "react-router-dom";
import { Menu } from "semantic-ui-react";
import { useState } from 'react';

export default function AccountOutlet() {
    const { user, setUser } = useOutletContext();

    const [menuActive, setMenuActive] = useState()

    return (
        <>
          <Menu style={{width: '80vw'}}> 
            <Menu.Item active={menuActive==='vendors'} link>
              <Link to='/account/vendors'>Vendors</Link>
            </Menu.Item>
            <Menu.Item active={menuActive==='orders'} >
              <Link to='/account/orders'>Orders</Link>
            </Menu.Item>
            <Menu.Item active={menuActive==='addresses'} >
              <Link to='/account/addresses'>Addresses</Link>
            </Menu.Item>
            <Menu.Item active={menuActive==='payment'} >
              <Link to='/account/paymentmethods'>Payment Methods</Link>
            </Menu.Item>
          </Menu>

          <Outlet context={{user, setUser, setMenuActive}} />
        </>
    )
}