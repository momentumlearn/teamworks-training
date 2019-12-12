import React from 'react'
import moment from 'moment'
import ReactMarkdown from 'react-markdown'
import { Link } from '@reach/router'

class PageListItem extends React.Component {
  render () {
    const { page, open } = this.props
    return (
      <li className='mb2'>
        <Link to={`/${page.title}/`}>{page.title}</Link>{' '}
        <span className='f6'>Updated {moment(page.updated_at).fromNow()}</span>
        {open && <ReactMarkdown source={page.body} />}
      </li>)
  }
}

export default PageListItem
