import React from 'react'

class EditPage extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      body: props.page.body
    }

    this.handleSave = this.handleSave.bind(this)
  }

  handleSave (event) {
    event.preventDefault()
    this.props.updatePageBody(this.state.body)
  }

  render () {
    const { page } = this.props
    const { body } = this.state

    return (
      <div id='EditPage'>
        <h2>{page.title}</h2>
        <form onSubmit={this.handleSave}>
          <div>
            <textarea
              style={{ width: '100%', height: '300px' }}
              value={body}
              onChange={(event) => this.setState({ body: event.target.value })}
            />
          </div>
          <button type='submit'>Save page</button>
        </form>
      </div>
    )
  }
}

export default EditPage
