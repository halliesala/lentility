import './App.css'
import LoginPage from './components/LoginPage'
import { useState, useEffect } from 'react'

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
      <LoginPage user={user} setUser={setUser} />
    </>
  )
}

export default App
