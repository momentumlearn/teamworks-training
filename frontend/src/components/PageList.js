import React from 'react'
import PageListItem from './PageListItem'

class PageList extends React.Component {
  constructor () {
    super()

    this.state = {
      open: null
    }

    this.openPage = this.openPage.bind(this)
  }

  openPage (pageId) {
    if (this.state.open === pageId) {
      this.setState({ open: null })
    } else {
      this.setState({ open: pageId })
    }
  }

  render () {
    return (
      <ul>
        {this.props.pages.map((page) => (
          <PageListItem
            key={page.id}
            openPage={this.openPage}
            page={page} open={page.id === this.state.open}
          />)
        )}
      </ul>
    )
  }
}

export default PageList
