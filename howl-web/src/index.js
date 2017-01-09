import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import { Layout, Menu, Icon } from 'antd';
import Api from './ApiConfig';
import Result from './Howl';

const { Header, Content } = Layout;

class App extends Component {
  render() {
    return (
      <Layout>
        <Header className="header">
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['2']}
            style={{ lineHeight: '64px' }}
            >
            <Menu.Item key="1"><Icon type="search" />Search</Menu.Item>
            <Menu.Item key="2"><Icon type="bulb" />API</Menu.Item>
            <Menu.Item key="3"><Icon type="appstore-o" />Dork</Menu.Item>
          </Menu>
        </Header>
        <Content>
            <Result apiurl={Api} />
        </Content>

      </Layout>
    );
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
