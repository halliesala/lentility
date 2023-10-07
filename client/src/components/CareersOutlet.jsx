import { useOutletContext } from "react-router-dom";
import { Outlet } from "react-router-dom";

export default function CareersOutlet() {
    const { user, setUser } = useOutletContext();

    return (
        <>
          <Outlet context={{user, setUser}} />
        </>
    )
}