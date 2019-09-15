import React, { Component } from 'react'
import { Form, Segment, Select, Icon, Checkbox, Grid, Header, Image } from 'semantic-ui-react'

import eatar_logo from '../images/eatar-logo.png'

class RegisterForm extends Component{

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
      first_name: this.state.first_name,
      last_name: this.state.last_name,
      password: this.state.pass,
      email: this.state.email,
      user_id: this.state.user_id = Math.ceil(Math.random() * Number.MAX_VALUE)
    }
    this.props.onSubmit(user_data);
  }

  render(){

    return(
      <Segment>
      <Grid textAlign='center' style={{ height: '100vh' }} verticalAlign='middle'>
        <Grid.Column style={{ maxWidth: 650 }}>
          <Header as='h2' color='red' textAlign='center'>
            <Image src={ eatar_logo } /> Create Your Account to your account
          </Header>
          <Form onSubmit={this.onSubmit}>
            <Form.Group widths={2}>
              <Form.Input required={true} label="Fisrt Name" type="text" name="first_name" placeholder="First Name" onChange={this.onChange}/>
              <Form.Input required={true} label="Last Name" type="text" name="last_name" placeholder="Last Name" onChange={this.onChange}/>
            </Form.Group>
            <Form.Group >
              <Form.Input width={6} required={true} label="Email" type="text" name="email" placeholder="johndoe@example.com" onChange={this.onChange}/>
              <Form.Input width={6} required={true} label="Password" type="password" name="pass" onChange={this.onChange}/>
              </Form.Group>
              <br/><br/><br/><br/><br/>
              <Form.Field required={true}>
                <Checkbox  label='I agree to the Terms and Conditions' />
              </Form.Field>
            <Form.Button icon labelPosition='left' size='medium' color='red' >
            Register
              <Icon name='check'/>
            </Form.Button>
            <br/>
          </Form>
        </Grid.Column>
      </Grid>

      </Segment>
    )
  }
}

export default RegisterForm
