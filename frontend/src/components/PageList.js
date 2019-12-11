import React from 'react'
import PageListItem from './PageListItem'

class PageList extends React.Component {
  render () {
    return (
      <ul>
        {this.props.pages.map((page) => <PageListItem page={page} />)}
      </ul>
    )
  }
}

export default PageList
