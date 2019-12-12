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
    this.setState({ user: { username: username, token: token } })
  }

  componentDidMount () {
    fetch('http://localhost:5000/pages/')
      .then(response => response.json())
      .then(data => this.setState({ pages: data.pages }))
      .catch(data => {
        this.setState({ errorRetrievingData: true })
      })
  }

  render () {
    return (
      <div id='App' className='bg-lightest-blue sans-serif pt3 min-vh-100'>
        <div className='mw8 center bg-white pv2 ph3 ba b--blue br1'>
          <h1 className='mt0'>
            <Link to='/'>PL Wiki</Link>
          </h1>
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
