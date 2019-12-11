import React from 'react'

class PageList extends React.Component {
  render () {
    return (
      <pre>{this.props.pages[0].title}</pre>
    )
  }
}

export default PageList
