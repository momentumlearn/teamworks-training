import React, { useState } from 'react'

const EditPage = ({ page, updatePageBody }) => {
  const [body, setBody] = useState(page.body)

  const handleSave = (event) => {
    event.preventDefault()
    updatePageBody(body)
  }

  return (
    <div id='EditPage'>
      <h2>{page.title}</h2>
      <form onSubmit={handleSave}>
        <div>
          <textarea
            style={{ width: '100%', height: '300px' }}
            value={body}
            onChange={(event) => setBody(event.target.value)}
          />
        </div>
        <button type='submit'>Save page</button>
      </form>
    </div>
  )
}

export default EditPage
