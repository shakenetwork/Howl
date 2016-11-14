import SearchInput from './HowlSearch';
import reqwest from 'reqwest';
import React from 'react';
import { Table, message } from 'antd';
import { Col, Row } from 'antd';
import 'antd/dist/antd.css';

const columns = [{
    title: 'Traget',
    dataIndex: 'target',
    render:target=>(<a href={target} target='_blank'>{target}</a>)
}, {
    title: 'Country',
    render: (target) => (
        <span>{target.plugins.Country ? target.plugins.Country.string.toString() : ''}

</span>)
}, {
    title: 'Code',
    dataIndex: 'http_status',
},
{
    title: 'Title',
    dataIndex: 'plugins',
    render: plugins => (
        plugins.Title ? plugins.Title.string.toString() : '')
},
{
    title: 'Server',
    render: (target) => (
        <span>{target.plugins.HTTPServer ? target.plugins.HTTPServer.string.toString() : ''}

</span>)
}
];
const Result = React.createClass({
    getInitialState() {
        return {
            data: [],
            pagination: {},
            loading: false,
            url: this.props.apiurl
        };
    },

    handleTableChange(pagination, filters) {
        const pager = this.state.pagination;
        pager.current = pagination.current;
        this.setState({
            pagination: pager,
        });
        this.fetch({
            page: pagination.current,
            ...filters,
        });
    },
fetch(params = {}) {
    this.setState({ loading: true });
    reqwest({
        url: this.state.url,
        method: 'get',
        data: {
            limit: 10000,
                ...params,
            },
type: 'json',
        }).then(data => {
    const pagination = this.state.pagination;
    pagination.total = data.count;
    // pagination.total === 0 ? message.error('暂无相关数据'):message.success(`成功加载${data.count}条数据`);
    if (pagination.total) {
        message.success(`成功加载${data.count}条数据`)
    }
    else {
        message.error('暂无相关数据')
    }
    this.setState({
        loading: false,
        data: data.data,
        count: data.count,
        pagination,
    });
});
    },
handleSearch(filter){
    this.setState({ loading: true });
    this.setState({ url: this.props.filterurl + filter }, () => this.fetch());
    this.setState({ loading: false });
},
componentDidMount() {
    this.fetch();
},
render() {
    return (
        <div style={{ background: '#FFF', padding: '40px' }}>
            <div style={{ background: '#FFF', padding: '30px' }}>
                <Row>
                    <Col span="4">
                    </Col>
                    <Col span="16">
                            <SearchInput placeholder='Apache || kibana || index of || Login '
                                onSearch={filter => {
                                    this.handleSearch(filter);
                                } } style={{ width: 400 }}
                                />
                    </Col>

                    <Col span="4">

                    </Col>
                </Row>
            </div>
            <Row>
                <Col span="2">

                </Col>

                <Col span="20">
                    <Table
                        bordered
                        columns={columns}
                        rowKey='target'
                        dataSource={this.state.data}
                        pagination={this.state.pagination}
                        loading={this.state.loading}
                        onChange={this.handleTableChange}
                        title={() => `共${this.state.pagination.total}条记录`}
                        footer={() => `共${this.state.pagination.total}条记录`}
                        />
                </Col>
                <Col span="2">

                </Col>
            </Row>
        </div>
    );
},
});


export default Result;
