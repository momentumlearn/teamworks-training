/* globals fetch */

import React from 'react'
import ReactMarkdown from 'react-markdown'
import EditPage from './EditPage'

class Page extends React.Component {
  constructor () {
    super()
    this.state = {
      page: null,
      errorRetrievingData: false,
      editing: false
    }

    this.updatePageBody = this.updatePageBody.bind(this)
  }

  componentDidMount () {
    const { pageName } = this.props
    fetch(`http://localhost:5000/pages/${pageName}/`)
      .then(response => response.json())
      .then(data => this.setState({ page: data }))
      .catch(err => this.setState({ errorRetrievingData: true }))
  }

  updatePageBody (newBody) {
    if (!this.props.userToken) {
      return
    }

    const { page } = this.state
    fetch(`http://localhost:5000/pages/${page.title}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.props.userToken}`
      },
      body: JSON.stringify({ body: newBody })
    })
      .then(response => {
        if (response.ok) {
          this.setState({
            editing: false,
            page: { ...page, body: newBody }
          })
        }
      })
  }

  render () {
    const { page } = this.state

    if (this.state.editing) {
      return (
        <EditPage
          page={page}
          updatePageBody={this.updatePageBody}
        />)
    }

    return (
      <div className='page'>
        {page &&
          <div>
            <h2>{page.title}</h2>
            <ReactMarkdown source={page.body} />
            <button onClick={() => this.setState({ editing: true })}>Edit this page</button>
          </div>}
      </div>
    )
  }
}

export default Page
