import React, { useState, useEffect } from 'react'
import { useLocalStorage } from '../hooks'
import PageList from './PageList'
import Page from './Page'
import Login from './Login'
import Register from './Register'
import { Router, Link } from '@reach/router'

const App = () => {
  const [activePage, setActivePage] = useState(null)
  const [pages, setPages] = useState([])
  const [error, setError] = useState(false)
  const [user, setUser] = useState({})
  const [username, setUsername] = useLocalStorage('wikiUsername', null)
  const [userToken, setUserToken] = useLocalStorage('wikiUserToken', null)

  const storeUser = (username, token) => {
    setUsername(username)
    setUserToken(token)
  }

  const clearUser = () => {
    setUsername(undefined)
    setUserToken(undefined)
  }

  const handleLogout = (event) => {
    event.preventDefault()
    clearUser()
  }

  useEffect(() => {
    fetch('http://localhost:5000/pages/')
      .then(response => response.json())
      .then(data => setPages(data.pages))
      .catch(data => setError(true))
  }, [])

  return (
    <div id='App' className='bg-lightest-blue sans-serif pt3 min-vh-100'>
      <div className='mw8 center bg-white pv2 ph3 ba b--blue br1'>
        <div className='flex items-center justify-between'>
          <h1 className='mv0'>
            <Link to='/'>PL Wiki</Link>
          </h1>
          <div className='tr'>
            {username
              ? <span>Logged in as {username} / <a href='#' onClick={handleLogout}>Logout</a></span>
              : <span><Link to='/login/'>Login</Link> / <Link to='/register/'>Register</Link></span>}
          </div>
        </div>
        {error && <div>We couldn't get your data! Try again later.</div>}
        <Router>
          <PageList pages={pages} path='/' />
          <Login path='login/' setUser={storeUser} />
          <Register path='register/' setUser={storeUser} />
          <Page path=':pageName/' userToken={userToken} />
        </Router>
      </div>
    </div>
  )
}

export default App
