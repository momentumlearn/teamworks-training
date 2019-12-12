import React from 'react'
import { navigate } from '@reach/router'

class Login extends React.Component {
  constructor () {
    super()
    this.state = {
      username: '',
      password: '',
      invalidUsernameOrPassword: false
    }

    this.handleLogin = this.handleLogin.bind(this)
    this.handleInputChange = this.handleInputChange.bind(this)
  }

  handleLogin (event) {
    event.preventDefault()
    console.log('logging in')
    fetch('http://localhost:5000/auth/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: this.state.username, password: this.state.password })
    })
      .then(response => response.json())
      .then(data => {
        if (data.token) {
          this.props.setUser(this.state.username, data.token)
          navigate('/')
        } else {
          this.setState({ invalidUsernameOrPassword: true })
        }
      })
  }

  handleInputChange (stateKey) {
    return (event) => this.setState({ [stateKey]: event.target.value })
  }

  render () {
    return (
      <div id='Login'>
        {
          this.state.invalidUsernameOrPassword &&
            <p className='red'>
            That username or password is invalid.
            </p>
        }
        <form className='measure center' onSubmit={this.handleLogin}>
          <fieldset id='sign_up' className='ba b--transparent ph0 mh0'>
            <legend className='f4 fw6 ph0 mh0'>Sign In</legend>
            <div className='mt3'>
              <label className='db fw6 lh-copy f6' htmlFor='username'>Username</label>
              <input
                className='pa2 input-reset ba bg-transparent w-100' type='text'
                name='username' id='email-address'
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
            <input className='b ph3 pv2 input-reset ba b--black bg-transparent grow pointer f6 dib' type='submit' value='Sign in' />
          </div>
        </form>
      </div>
    )
  }
}

export default Login
