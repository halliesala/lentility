import { Link } from "react-router-dom";
import { Image } from "semantic-ui-react";

export default function LentilityBanner({ user, setUser }) {
    return (
        <div>
            <div className='logo-name-div'>
                <Image className='logo' src='/lentility_icon.png' alt="Lentility logo" size="small"  />
                <Link to='/'><h1>Lentility</h1></Link>
            </div>
            {
                user
                    ? <LoggedInLinks user={user} setUser={setUser} />
                    : <LoggedOutLinks />
            }
        </div>
    )

}

function LoggedInLinks({ user, setUser }) {

    function handleLogout() {
        fetch('/api/v1/logout', { 'method': 'DELETE' })
            .then(resp => {
                if (resp.ok) {
                    setUser(null)
                }
            })
    }

    return (
        <>
            <nav>
                <span>Hi, {user.first_name} {user.last_name}!</span>
                <p style={{color: 'red'}}>user_id={user.id}</p>
                <p style={{color: 'red'}}>practice_id={user.practice_id}</p>
            </nav>
            <nav className="header-nav">
                <Link className="nav-bar-link" to='/shop'>Shop</Link>
                <Link className="nav-bar-link" to='/cart'>Cart</Link>
                <Link className="nav-bar-link" to='/account/vendors'>Account</Link>
                <Link className="nav-bar-link" to='/logout'>Logout</Link>
            </nav>
        </>
    )
}

function LoggedOutLinks() {
    return (
        <nav className="header-nav">
            <Link className="nav-bar-link" to='login'>Login</Link>
            <Link className="nav-bar-link" to='signup'>Sign Up</Link>
        </nav>
    )
}