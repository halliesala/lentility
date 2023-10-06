
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
            <h1>Lentility</h1>
            {
                user
                ? (
                    <>
                        <span>Hi, {user.first_name} {user.last_name}</span>
                        <button onClick={handleLogout}>Logout</button>
                    </>
                    )
                : null
            }
        </div>
    )
}