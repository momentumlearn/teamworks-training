import React from 'react'
import moment from 'moment'
import ReactMarkdown from 'react-markdown'

class PageListItem extends React.Component {
  render () {
    const { page, open, openPage } = this.props
    return (
      <li>
        <strong style={{ cursor: 'pointer' }} onClick={() => openPage(page.id)}>{page.title}</strong>{' '}
        <span>{moment(page.updated_at).fromNow()}</span>
        {open && <ReactMarkdown source={page.body} />}
      </li>)
  }
}

export default PageListItem
