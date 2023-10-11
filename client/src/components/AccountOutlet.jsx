import { useOutletContext } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { Menu } from "semantic-ui-react";

export default function AccountOutlet() {
    const { user, setUser } = useOutletContext();

    return (
        <>
          <Outlet context={{user, setUser}} />
        </>
    )
}