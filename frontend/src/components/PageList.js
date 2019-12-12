import React from 'react'
import PageListItem from './PageListItem'

class PageList extends React.Component {
  render () {
    return (
      <div id='PageList'>
        <h2>Pages</h2>
        {
          this.props.pages.length === 0
            ? <p>Loading...</p>
            : (
              <ul className='list pl0'>
                {this.props.pages.map((page) => (
                  <PageListItem
                    key={page.id}
                    page={page}
                    openPage={this.props.setPage}
                  />)
                )}
              </ul>
            )
        }

      </div>
    )
  }
}

export default PageList
