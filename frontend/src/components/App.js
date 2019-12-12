import React from 'react'
import PageList from './PageList'
import Page from './Page'
import { Router } from '@reach/router'

class App extends React.Component {
  constructor () {
    super()
    this.state = {
      activePage: null,
      pages: [],
      errorRetrievingData: false
    }

    this.setActivePage = this.setActivePage.bind(this)
  }

  componentDidMount () {
    fetch('http://localhost:5000/pages/')
      .then(response => response.json())
      .then(data => this.setState({ pages: data.pages }))
      .catch(data => {
        this.setState({ errorRetrievingData: true })
      })
  }

  setActivePage (page) {
    this.setState({ activePage: page })
  }

  render () {
    return (
      <div id='App' className='bg-lightest-blue sans-serif pt3 min-vh-100'>
        <div className='mw8 center bg-white pv2 ph3 ba b--blue br1'>
          <h1 className='mt0'>
            <a
              onClick={(event) => { event.preventDefault(); this.setActivePage(null) }}
              href='#'
            >
            PL Wiki
            </a>
          </h1>
          {this.state.errorRetrievingData && <div>We couldn't get your data! Try again later.</div>}
          <Router>
            <PageList pages={this.state.pages} path='/' />
            <Page path=':pageName/' />
          </Router>
        </div>
      </div>
    )
  }
}

export default App
