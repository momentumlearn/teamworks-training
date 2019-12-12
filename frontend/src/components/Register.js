import React from 'react'
import { navigate, Link } from '@reach/router'

class Register extends React.Component {
  constructor () {
    super()
    this.state = {
      username: '',
      password: '',
      errors: []
    }
    this.handleRegister = this.handleRegister.bind(this)
  }

  handleRegister (event) {
    event.preventDefault()

    const { username, password } = this.state
    fetch('http://localhost:5000/auth/user/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.errors) {
          this.setState({ errors: data.errors })
        } else {
          this.props.setUser(data.username, data.token)
          navigate('/')
        }
      })
  }

  handleInputChange (stateKey) {
    return (event) => this.setState({ [stateKey]: event.target.value })
  }

  render () {
    return (
      <div id='Register'>
        {this.state.errors.length > 0 &&
          this.state.errors.map(error => <p key={error[0]} className='red'>{error[1]}</p>)}

        <form className='measure center' onSubmit={this.handleRegister}>
          <fieldset id='sign_up' className='ba b--transparent ph0 mh0'>
            <legend className='f4 fw6 ph0 mh0'>Register</legend>
            <div className='mt3'>
              <label className='db fw6 lh-copy f6' htmlFor='username'>Username</label>
              <input
                className='pa2 input-reset ba bg-transparent w-100' type='text'
                name='username' id='username'
                onChange={this.handleInputChange('username')}
                value={this.state.username}
              />
            </div>
            <div className='mv3'>
              <label className='db fw6 lh-copy f6' htmlFor='password'>Password</label>
              <input
                className='b pa2 input-reset ba bg-transparent w-100'
                type='password' name='password' id='password'
                onChange={this.handleInputChange('password')}
                value={this.state.password}
              />
            </div>
          </fieldset>
          <div>
            <input className='b ph3 pv2 input-reset ba b--black bg-transparent grow pointer f6 dib' type='submit' value='Register' />
          </div>
        </form>
        <p>Already have an account? <Link to='/login/'>Login</Link></p>
      </div>
    )
  }
}

export default Register
