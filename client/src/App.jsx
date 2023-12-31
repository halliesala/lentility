import './App.css'
import { Outlet, useLoaderData } from 'react-router-dom'
import { useState } from 'react'
import LentilityBanner from './components/LentilityBanner';
import 'semantic-ui-css/semantic.min.css';
import Footer from './components/Footer';
// import ChatWindow from './components/ChatWindow';

function App() {

  const {session} = useLoaderData()

  const[user, setUser] = useState(session.user);

  return (
    <>
      {/* <p>----------HEADER----------</p> */}
      <LentilityBanner user={user} setUser={setUser} />
      {/* <p>----------OUTLET----------</p> */}
      <Outlet context={{user, setUser}}/>
      {/* <p>----------FOOTER----------</p> */}
      {/* <ChatWindow /> */}
      <Footer />
    </>
  )
}

export default App
