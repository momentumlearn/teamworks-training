import React from 'react'
import moment from 'moment'
import ReactMarkdown from 'react-markdown'

class Page extends React.Component {
  render () {    
    const page = this.props.page

    return (
      <div className='page'>
        <h2>{page.title}</h2>
        <ReactMarkdown source={page.body} />
      </div>
    )
  }
}

export default Page
