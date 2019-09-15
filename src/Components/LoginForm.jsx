import React from 'react'
import { Button, Form, Grid, Header, Image, Message, Segment } from 'semantic-ui-react'

import eatar_logo from '../images/eatar-logo.png'


class LoginForm extends React.Component {

  constructor(props){
      super()
      this.state = {}
      this.onChange = this.onChange.bind(this)
      this.onSubmit = this.onSubmit.bind(this)
    }

    onChange(e, {value} ){
      this.setState({ [e.target.name]: value });
    }

    onSubmit(e){
      e.preventDefault()
      const user_data = {
        email: this.state.email,
        password: this.state.password,
      }
      this.props.onSubmit(user_data);
    }

    render(){
      return (
      <Segment>
        <Grid textAlign='center' style={{ height: '100vh' }} verticalAlign='middle'>
          <Grid.Column style={{ maxWidth: 450 }}>
            <Header as='h2' color='red' textAlign='center'>
              <Image src={ eatar_logo } /> Log-in to your account
            </Header>
            <Form size='large' onSubmit={this.onSubmit}>
              <Segment stacked>
                <Form.Input
                fluid icon='user'
                iconPosition='left'
                placeholder='E-mail address'
                name='email'
                onChange={this.onChange}/>
                <Form.Input
                  fluid
                  icon='lock'
                  iconPosition='left'
                  placeholder='Password'
                  name='password'
                  type='password'
                  onChange={this.onChange}
                />
                <Button color='red' fluid size='large'>
                  Login
                </Button>
              </Segment>
            </Form>
            <Message>
              New to us? <a href='#'>Sign Up</a>
            </Message>
          </Grid.Column>
        </Grid>
      </Segment>
    )
  }
}

export default LoginForm
