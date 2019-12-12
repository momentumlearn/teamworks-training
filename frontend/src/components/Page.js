/* globals fetch */

import React from 'react'
import ReactMarkdown from 'react-markdown'

class Page extends React.Component {
  constructor () {
    super()
    this.state = {
      page: null,
      errorRetrievingData: false
    }
  }

  componentDidMount () {
    const { pageName } = this.props
    fetch(`http://localhost:5000/pages/${pageName}/`)
      .then(response => response.json())
      .then(data => this.setState({ page: data }))
      .catch(err => this.setState({ errorRetrievingData: true }))
  }

  render () {
    const { page } = this.state

    return (
      <div className='page'>
        {page &&
          <>
            <h2>{page.title}</h2>
            <ReactMarkdown source={page.body} />
          </>}
      </div>
    )
  }
}

export default Page
