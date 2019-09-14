import React from 'react';
import HomepageLayout from './Components/Home'
import LoginForm from './Components/LoginForm'
import logo from './logo.svg';
import './App.css';

class App extends React.Component {
  render() {
    return (
      <div>
        <HomepageLayout/>
      </div>
    );
  }
}

export default App;
