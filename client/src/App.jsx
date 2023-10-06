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
        return resp.json()
      } else {
        return null
      }
    })
    .then(data => {
      console.log("CHECK SESSION DATA: ", data)
      setUser(data['user'])
    })
  }, [])

  return (
    <>
      <LoginPage user={user} setUser={setUser} />
    </>
  )
}

export default App
