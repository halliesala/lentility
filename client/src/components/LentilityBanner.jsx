import { Link } from "react-router-dom"

export default function LentilityBanner({user, setUser}) {

    function handleLogout() {
        fetch('/api/v1/logout', {'method': 'DELETE'})
        .then(resp => {
            if (resp.ok) {
                setUser(null)
            }
        })
    }
    
    return (
        <div>
            <Link to='/'><h1>Lentility</h1></Link>
            {
                user
                ? (
                    <>
                        <nav>
                            <span>Hi, {user.first_name} {user.last_name}</span>
                            <button onClick={handleLogout}>Logout</button>
                        </nav>
                        <nav>
                            <Link to='/shop'>Shop</Link>
                            <Link to='/cart'>Cart</Link>
                        </nav>
                    </>
                    )
                : <Link to='login'>Login</Link>
            }
        </div>
    )
}