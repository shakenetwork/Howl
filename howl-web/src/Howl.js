import SearchInput from './HowlSearch';
import reqwest from 'reqwest';
import React from 'react';
import { Table, message, Card, BackTop } from 'antd';
import { Col, Row } from 'antd';
import 'antd/dist/antd.css';
import { Radio,Tag } from 'antd';

const RadioGroup = Radio.Group;

const vuldbColumns = [{
    title: 'Submit Time',
    dataIndex: 'time'

}, {
    title: 'Name',
    render: (vul) => (
        <span>
            <a href={vul.reference} target='_blank'>{vul.title} <Tag color="#87d068">{vul.source}</Tag></a>
        </span>
    )
}]

const whatwebColumns = [{
    title: 'Traget',
    dataIndex: 'target',
    render: target => (<a href={target} target='_blank'>{target}</a>)
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
            columns: whatwebColumns,
            url: this.props.apiurl,
            api: this.props.apiurl.whatwebApi
        };
    },

    handleTableChange(pagination, filters) {
        const pager = this.state.pagination;
        pager.current = pagination.current;
        this.setState({
            pagination: pager,
        });
        // this.fetch({
        //     page: pagination.current,
        //     ...filters,
        // });
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
    this.setState({ url: this.state.api + filter }, () => this.fetch());
    this.setState({ loading: false });
},
componentDidMount() {
    this.fetch();
},
onChange(e) {
    
    e.target.value === 1 ? this.setState({
        api: this.props.apiurl.vuldbApi,
        data:[],
        columns: vuldbColumns,
        value: e.target.value
    }) : this.setState({
        api: this.props.apiurl.whatwebApi,
        data: [],
        columns: whatwebColumns,
        value: e.target.value
    })
    console.log('radio checked', this.state.api);
},
render() {
    return (
        <div style={{ background: '#FFF', padding: '40px' }}>
            <BackTop />
            <div style={{ background: '#FFF', padding: '30px' }}>
                <Row align='middle' gutter={16} >
                    <Col span={6}>
                        <RadioGroup defaultValue={1} onChange={this.onChange} value={this.state.value}>
                            <Radio key="vuldb" value={1}>漏洞库</Radio>
                            <Radio key="whatweb" defaultChecked value={2}>web指纹库</Radio>
                        </RadioGroup>
                    </Col>
                    <Col span={6}>
                        <SearchInput placeholder='管理 '
                            onSearch={filter => {
                                this.handleSearch(filter);
                            } } style={{ width: 400 }}
                            />
                    </Col>
                </Row>
            </div>

            <Card >
                <Row align="middle">
                    <Col>
                        <Table
                            bordered={false}
                            columns={this.state.columns}
                            rowKey='target'
                            dataSource={this.state.data}
                            pagination={this.state.pagination}
                            loading={this.state.loading}
                            onChange={this.handleTableChange}
                            title={() => `共${this.state.pagination.total}条记录`}
                            footer={() => `共${this.state.pagination.total}条记录`}
                            />
                    </Col>
                </Row>
            </Card>
        </div>
    );
},
});


export default Result;
