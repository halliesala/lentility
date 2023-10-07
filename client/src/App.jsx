import './App.css'
import { Outlet } from 'react-router-dom'
import { useState, useEffect } from 'react'
import LentilityBanner from './components/LentilityBanner';
import 'semantic-ui-css/semantic.min.css';
import Footer from './components/Footer';

function App() {

  const[user, setUser] = useState(null);

  useEffect(() => {
    console.log("Checking session...")
    fetch("api/v1/checksession")
    .then(resp => {
      if (resp.ok) {
        return resp.json().then(data => {
          console.log("Session found. Logged in as: ", data.user.email)
          setUser(data.user)
        })
      } else {
        return null
      }
    })
    
  }, [])

  return (
    <>
      <p>----------HEADER----------</p>
      <LentilityBanner user={user} setUser={setUser} />
      <p>----------OUTLET----------</p>
      <Outlet context={{user, setUser}}/>
      <p>----------FOOTER----------</p>
      <Footer />
    </>
  )
}

export default App
