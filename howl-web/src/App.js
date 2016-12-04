import React, { Component } from 'react';
import './App.css';
import Result from './Howl';
import Api from './ApiConfig';
class App extends Component {
  render() {
    return (

          <div className="ant-layout-wrapper">
            <div className="ant-layout-container">
              <div style={{ height: 210 }}>
                <Result apiurl={Api} />
              </div>
            </div>
            </div>

    );
  }
}

export default App;
