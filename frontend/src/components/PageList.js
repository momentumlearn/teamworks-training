import React from 'react'
import PageListItem from './PageListItem'

class PageList extends React.Component {
  render () {
    return (
      <div id='PageList'>
        <ul>
          {this.props.pages.map((page) => (
            <PageListItem
              key={page.id}
              page={page}
              openPage={this.props.setPage}
            />)
          )}
        </ul>
      </div>
    )
  }
}

export default PageList
