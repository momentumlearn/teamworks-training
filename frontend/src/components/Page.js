/* globals fetch */

import React, { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import EditPage from './EditPage'

const Page = ({ pageName, userToken }) => {
  const [page, setPage] = useState(null)
  const [error, setError] = useState(false)
  const [editing, setEditing] = useState(false)

  useEffect(() => {
    fetch(`http://localhost:5000/pages/${pageName}/`)
      .then(response => response.json())
      .then(data => setPage(data))
      .catch(err => setError(true))
  }, [])

  useEffect(() => {
    if (page) {
      window.document.title = `${page.title} (${page.body.length})`
    }
  })

  const updatePageBody = (newBody) => {
    if (!userToken) {
      return
    }

    fetch(`http://localhost:5000/pages/${page.title}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${userToken}`
      },
      body: JSON.stringify({ body: newBody })
    })
      .then(response => {
        if (response.ok) {
          setEditing(false)
          setPage({ ...page, body: newBody })
        }
      })
  }

  if (editing) {
    return (
      <EditPage
        page={page}
        updatePageBody={updatePageBody}
      />)
  }

  return (
    <div className='page'>
      {page &&
        <div>
          <h2>{page.title}</h2>
          <ReactMarkdown source={page.body} />
          <button onClick={() => setEditing(true)}>Edit this page</button>
        </div>}
    </div>
  )
}

export default Page
