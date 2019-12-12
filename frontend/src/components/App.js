import React from 'react'
import PageList from './PageList'
import Page from './Page'
import Login from './Login'
import { Router, Link } from '@reach/router'

class App extends React.Component {
  constructor () {
    super()
    this.state = {
      activePage: null,
      pages: [],
      errorRetrievingData: false,
      user: {}
    }

    this.setUser = this.setUser.bind(this)
  }

  setUser (username, token) {
    window.localStorage.setItem('wikiUsername', username)
    window.localStorage.setItem('wikiUserToken', token)
    this.setState({ user: { username: username, token: token } })
  }

  componentDidMount () {
    const username = window.localStorage.getItem('wikiUsername')
    const token = window.localStorage.getItem('wikiUserToken')
    if (username && token) {
      this.setState({ user: { username: username, token: token } })
    }

    fetch('http://localhost:5000/pages/')
      .then(response => response.json())
      .then(data => this.setState({ pages: data.pages }))
      .catch(data => {
        this.setState({ errorRetrievingData: true })
      })
  }

  render () {
    const { user } = this.state
    return (
      <div id='App' className='bg-lightest-blue sans-serif pt3 min-vh-100'>
        <div className='mw8 center bg-white pv2 ph3 ba b--blue br1'>
          <div className='flex items-center justify-between'>
            <h1 className='mv0'>
              <Link to='/'>PL Wiki</Link>
            </h1>
            <div className='tr'>
              {user.username
                ? <span>Logged in as {user.username}</span>
                : <Link to='/login/'>Login</Link>}
            </div>
          </div>
          {this.state.errorRetrievingData && <div>We couldn't get your data! Try again later.</div>}
          <Router>
            <PageList pages={this.state.pages} path='/' />
            <Login path='login/' setUser={this.setUser} />
            <Page path=':pageName/' />
          </Router>
        </div>
      </div>
    )
  }
}

export default App
