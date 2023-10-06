import './App.css'
import { Outlet } from 'react-router-dom'
import { useState, useEffect } from 'react'
import LentilityBanner from './components/LentilityBanner';
import 'semantic-ui-css/semantic.min.css';

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
      <LentilityBanner user={user} setUser={setUser} />
      <Outlet context={{user, setUser}}/>
    </>
  )
}

export default App
