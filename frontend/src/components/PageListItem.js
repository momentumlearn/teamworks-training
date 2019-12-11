import React from 'react'
import moment from 'moment'

class PageListItem extends React.Component {
  render () {
    const { page, open } = this.props
    return (
      <li>
        <strong>{page.title}</strong>{' '}
        <span>{moment(page.updated_at).fromNow()}</span>
        {open && <pre>{page.body}</pre>}
      </li>)
  }
}

export default PageListItem
