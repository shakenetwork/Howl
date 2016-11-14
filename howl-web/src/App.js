import React, { Component } from 'react';
import './App.css';
import Result from './Howl';
import whatwebApi from './ApiConfig';

class App extends Component {
  render() {
    return (
      <div>
        <Result apiurl={whatwebApi} filterurl={whatwebApi}/>
      </div>
    );
  }
}

export default App;
