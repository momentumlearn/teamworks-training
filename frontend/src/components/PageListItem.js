import React from 'react'
import moment from 'moment'
import ReactMarkdown from 'react-markdown'

class PageListItem extends React.Component {
  openPage (event) {
    event.preventDefault()
    this.props.openPage(this.props.page)
  }

  render () {
    const { page, open, openPage } = this.props
    return (
      <li className='mb2'>
        <a href='#' onClick={this.openPage.bind(this)}>{page.title}</a>{' '}
        <span className='f6'>Updated {moment(page.updated_at).fromNow()}</span>
        {open && <ReactMarkdown source={page.body} />}
      </li>)
  }
}

export default PageListItem
