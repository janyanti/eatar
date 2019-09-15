import React from 'react'
import { Dimmer, Loader, Image, Segment, Form, Grid, Card, Button, Table, Header, Rating } from 'semantic-ui-react'

import eatar_logo from '../images/eatar-logo.png'

class Select extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      coords: false,
      location: "Boston, MA",
      members: 0,
      selection: []
    }
    this.getCoords = this.getCoords.bind(this)
    this.onChange = this.onChange.bind(this)
    this.onSubmit = this.onSubmit.bind(this)
    this.getMembers = this.getMembers.bind(this)
    this.getLocation = this.getLocation.bind(this)
  }

  onChange(e, {value} ){
    this.setState({ [e.target.name]: value });
  }

  onSubmit(e){
    e.preventDefault()
    const query = {
      group_id: this.state.group_id,
      location: this.state.location,
      latitude: this.state.latitude,
      longitude: this.state.longitude,
      preferences: []
    }

    this.props.onSubmit(query);
  }

  getCoords(){
    const location = window.navigator && window.navigator.geolocation

    if (location) {
      location.getCurrentPosition((position) => {
        this.setState({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          coords: true
        })
      }, (error) => {
        this.setState({ latitude: 'err-latitude', longitude: 'err-longitude' })
      })
    }
  }

  getLocation(){
    const query = {
      group_id: this.state.group_id,
    }

    const json = JSON.stringify(query)
    let url = 'http://localhost:5000/execute_query'
    let options = {
      method: 'POST',
      headers:
       { 'cache-control': 'no-cache',
         'Content-Type': 'application/json'
       },
      body: json
      };

      fetch(url, options)
        .then(response => (response.json()))
        .catch( err => console.log("Error: ", err))
        .then((data, stats) => {
          if (data){
            this.setState({ selection: data })
          }
        })
  }

  getMembers(){
    let data = {
      group_id: this.state.group_id
    }

    const json = JSON.stringify(data)
    let url = 'http://localhost:5000/queries'
    let options = {
      method: 'POST',
      headers:
       { 'cache-control': 'no-cache',
         'Content-Type': 'application/json'
       },
      body: json
      };

      fetch(url, options)
        .then(response => (response.json()))
        .catch( err => console.log("Error: ", err))
        .then((data, stats) => {
          if (data){
            this.setState({ members: data })
          }
        })

  }

  componentDidMount(){
      setInterval(() => {
      if (this.state.group_id !== "")
        this.getMembers()
      }
    ,1000);

  }


  render(){

    let preferences = [
      {  key: 'del', text: 'Deli', value: 'deli' },
      {  key: 'haw', text: 'Hawaiian', value: 'hawaiian' },
      {  key: 'car', text: 'Caribbean', value: 'caribbean' },
      {  key: 'lat', text: 'Latin', value: 'latin' },
      {  key: 'fre', text: 'French', value: 'french' },
      {  key: 'ger', text: 'German', value: 'german' },
      {  key: 'ind', text: 'Indian', value: 'indian' },
      {  key: 'ser', text: 'Serbian', value: 'serbian' },
      {  key: 'chi', text: 'Chinese', value: 'chinese' },
      {  key: 'ind', text: 'Indonesian', value: 'indonesian' },
      {  key: 'jap', text: 'Japanese', value: 'japanese' },
      {  key: 'kor', text: 'Korean', value: 'korean' },
      {  key: 'tha', text: 'Thai', value: 'thai' },
      {  key: 'sou', text: 'South African', value: 'south-african' },
      {  key: 'tex', text: 'Tex-Mex', value: 'tex-mex' },
      {  key: 'ita', text: 'Italian', value: 'italian' },
      {  key: 'fas', text: 'Fast Food', value: 'fast-food' },
      {  key: 'med', text: 'Mediterranean', value: 'mediterranean' },
      {  key: 'mon', text: 'Mongolian', value: 'mongolian' },
      {  key: 'vie', text: 'Vietnamese', value: 'vietnamese' }
    ]

    let table_items = null
    if (this.state.selection) {
      table_items = this.state.selection.map((item) =>
        (
        <Table.Row>
          <Table.Cell>
            <Header as='h2' textAlign='left'>
              {item.name}
            </Header>
          </Table.Cell>
          <Table.Cell singleLine>{item.price}</Table.Cell>
          <Table.Cell>
            <Rating size='large' icon='star' defaultRating={item.rating} maxRating={5} />
          </Table.Cell>
          <Table.Cell textAlign='left'>
            {item.address.join(" ")}
          </Table.Cell>
          <Table.Cell>
          </Table.Cell>
        </Table.Row>
        ))
    }


    let table = null
    if (this.state.selection.length > 0  ) {
      table = (
        <Table cell padded>
          <Table.Header>
          <Table.Row>
          <Table.HeaderCell singleLine>Name</Table.HeaderCell>
          <Table.HeaderCell>Price</Table.HeaderCell>
          <Table.HeaderCell>Rating</Table.HeaderCell>
          <Table.HeaderCell>Address</Table.HeaderCell>
          <Table.HeaderCell>Comments</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {table_items}
        </Table.Body>
        </Table>
      )
    }


    let side_panel =
      (
    <div>
      <Grid rows={2}>
        <Grid.Row>
          <Card centered
          image={eatar_logo}
          header={this.state.group_id}
          meta={this.state.location}
          description={`This Session has ${this.state.members} Member(s)`}
          />
        </Grid.Row>
        <Grid.Row>
          <Button onClick={this.getLocation} size='large' floated color='red'>
            Pick Location
          </Button>
        </Grid.Row>
      </Grid>
    </div>
  )

    return (
      <div className="Select">
        <Segment>
          <Grid columns={2} >
            <Grid.Row>
              <Grid.Column textAlign='left'>
              <Form onSubmit={this.onSubmit}>
              <Form.Group widths='equal'>
                <Form.Input fluid label='Group Name' name='group_id' placeholder='Super Awesome Lunch!' onChange={this.onChange}/>
                <Form.Input fluid label='Location' name='location' onChange={this.onChange} />
              </Form.Group>
              <Form.Group widths='equal'>
                <Form.Input fluid label='Longitude' disabled onChange={this.onChange}>{this.state.longitude}</Form.Input>
                <Form.Input fluid label='Latitude' disabled onChange={this.onChange}>{this.state.latitude}</Form.Input>
                <Form.Button color='red' icon="crosshairs" onClick={this.getCoords}>
                </Form.Button>
              </Form.Group>
              <Form.Group grouped widths='equal'>
                <label>Preferences</label>
                  <Form.Select
                    fluid
                    label='Top Pick'
                    options={preferences}
                    placeholder='Food Category'
                    name='pref1'
                    onChange={this.onChange}
                />
                <Form.Select
                  fluid
                  label='Second Pick'
                  options={preferences}
                  placeholder='Food Category'
              />
                <Form.Select
                  fluid
                  label='Third Pick'
                  options={preferences}
                  placeholder='Food Category'
              />
              </Form.Group>
              <Form.Button onClick={this.onSubmit} color='red'>Add Suggestion</Form.Button>
            </Form>
            </Grid.Column>
            <Grid.Column>
              {side_panel}
            </Grid.Column>
            </Grid.Row>
          </Grid>
        </Segment>
        {table}
      </div>
    )
  }
}

export default Select
