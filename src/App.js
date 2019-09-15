import React from 'react';
import HomepageLayout from './Components/Home'
import LoginForm from './Components/LoginForm'
import RegisterForm from './Components/RegisterForm'
import LoaderView from './Components/Loader'
import logo from './logo.svg';
import './App.css';


class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = { page: "home"}
    this.change_state = this.change_state.bind(this)
    this.add_user = this.add_user.bind(this)
    this.auth_user = this.auth_user.bind(this)

  }

  add_user(data){
    const json = JSON.stringify(data)
    let url = 'http://localhost:5000/register'
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
        .then((data, stats) => console.log("Success: ", data, stats))
        .catch( err => console.log("Error: ", err))
  }

  auth_user(data){
    const json = JSON.stringify(data)
    let url = 'http://localhost:5000/authenticate'
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
        .then((data, stats) => console.log("Success: ", data, stats))
        .catch( err => console.log("Error: ", err))
  }

  change_state(state){

    this.setState({ page: 'loading'})
    setTimeout(() => this.setState({ page: state}), 1000)
    console.log(`State changed to ${state}`)

  }


  render() {
    let home = (
      <div>
        <HomepageLayout onState={this.change_state}/>
      </div>
    );

    let login = (
      <div>
        <LoginForm onSubmit={this.auth_user}/>
      </div>
    )

    let sign_up = (
      <div>
        <RegisterForm onSubmit={this.add_user}/>
      </div>
    )

    let loader = (
      <div>
        <LoaderView/>
      </div>
    )

    switch (this.state.page) {
      case "home":
        return home
      case "login":
        return login
      case "sign_up":
        return sign_up
      case "loading":
        return loader
      default:
        return home
    }

  }
}

export default App;
