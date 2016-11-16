import React, { Component } from 'react';
import './App.css';
import { Menu } from 'antd';

import Result from './Howl';
import whatwebApi from './ApiConfig';

class App extends Component {
  render() {
    return (
        <div className="ant-layout-top">
          <div className="ant-layout-header">
            <div className="ant-layout-wrapper">
              <div className="ant-layout-logo"></div>
              <Menu theme="dark" mode="horizontal"
                defaultSelectedKeys={['1']} style={{ lineHeight: '64px' }}>
                <Menu.Item key="1">Search</Menu.Item>
                <Menu.Item key="2">Api</Menu.Item>
                <Menu.Item key="3">About</Menu.Item>
              </Menu>
            </div>
          </div>
          <div className="ant-layout-wrapper">
            <div className="ant-layout-container">
              <div style={{ height: 210 }}>
                <Result apiurl={whatwebApi} filterurl={whatwebApi} />
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default App;
