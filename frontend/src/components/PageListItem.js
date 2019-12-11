import React from 'react'
import moment from 'moment'

class PageListItem extends React.Component {
  render () {
    const { page } = this.props
    return (
      <li>
        <strong>{page.title}</strong>{' '}
        <span>{moment(page.updated_at).fromNow()}</span>
      </li>)
  }
}

export default PageListItem
