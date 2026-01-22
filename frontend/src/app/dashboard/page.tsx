'use client';

import React from 'react';
import { Row, Col, Card, Statistic, Typography, Table, Tag, Space } from 'antd';
import {
  ProjectOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  WarningOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
} from 'recharts';
import { AppLayout } from '@/components/layout/AppLayout';

const { Title, Text } = Typography;

const sprintData = [
  { name: 'Sprint 1', velocity: 45, bugs: 12 },
  { name: 'Sprint 2', velocity: 52, bugs: 8 },
  { name: 'Sprint 3', velocity: 48, bugs: 15 },
  { name: 'Sprint 4', velocity: 61, bugs: 5 },
  { name: 'Sprint 5', velocity: 55, bugs: 10 },
];

const revenueData = [
  { month: 'Jan', revenue: 4000, cost: 2400 },
  { month: 'Feb', revenue: 3000, cost: 1398 },
  { month: 'Mar', revenue: 2000, cost: 9800 },
  { month: 'Apr', revenue: 2780, cost: 3908 },
  { month: 'May', revenue: 1890, cost: 4800 },
  { month: 'Jun', revenue: 2390, cost: 3800 },
];

const projectColumns = [
  {
    title: 'Project Name',
    dataIndex: 'name',
    key: 'name',
    render: (text: string) => <Text strong>{text}</Text>,
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    render: (status: string) => {
      let color = 'blue';
      if (status === 'Completed') color = 'green';
      if (status === 'At Risk') color = 'volcano';
      return <Tag color={color}>{status.toUpperCase()}</Tag>;
    },
  },
  {
    title: 'Progress',
    dataIndex: 'progress',
    key: 'progress',
    render: (progress: number) => <Text>{progress}%</Text>,
  },
];

const projectData = [
  { id: 1, name: 'Cyberpunk Odyssey', status: 'In Progress', progress: 65 },
  { id: 2, name: 'Neon Knights', status: 'At Risk', progress: 40 },
  { id: 3, name: 'Pixel Quest', status: 'Completed', progress: 100 },
];

export default function Dashboard() {
  return (
    <AppLayout>
      <div className="mb-6">
        <Title level={2}>Studio Dashboard</Title>
        <Text type="secondary">Real-time overview of your game development projects</Text>
      </div>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm">
            <Statistic
              title="Active Projects"
              value={12}
              prefix={<ProjectOutlined className="text-blue-500" />}
            />
            <div className="mt-2 text-green-500">
              <ArrowUpOutlined /> <Text type="success">12% from last month</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm">
            <Statistic
              title="Tasks Completed"
              value={154}
              prefix={<CheckCircleOutlined className="text-green-500" />}
            />
            <div className="mt-2 text-green-500">
              <ArrowUpOutlined /> <Text type="success">8.2% vs target</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm">
            <Statistic
              title="Pending Approval"
              value={24}
              prefix={<ClockCircleOutlined className="text-orange-500" />}
            />
            <div className="mt-2 text-red-500">
              <ArrowUpOutlined /> <Text type="danger">Needs attention</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm">
            <Statistic
              title="Bugs Reported"
              value={8}
              prefix={<WarningOutlined className="text-red-500" />}
            />
            <div className="mt-2 text-green-500">
               <ArrowDownOutlined /> <Text type="success">15% fewer than avg</Text>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="mt-6">
        <Col xs={24} lg={16}>
          <Card title="Sprint Velocity & Trends" bordered={false} className="shadow-sm">
            <div style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer>
                <BarChart data={sprintData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="velocity" fill="#1890ff" radius={[4, 4, 0, 0]} name="Velocity" />
                  <Bar dataKey="bugs" fill="#ff4d4f" radius={[4, 4, 0, 0]} name="Bugs Fixed" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Recent Projects" bordered={false} className="shadow-sm">
            <Table
              columns={projectColumns}
              dataSource={projectData}
              pagination={false}
              size="small"
              rowKey="id"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="mt-6">
        <Col span={24}>
           <Card title="Revenue vs Development Cost" bordered={false} className="shadow-sm">
            <div style={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <AreaChart data={revenueData}>
                  <defs>
                    <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1890ff" stopOpacity={0.1}/>
                      <stop offset="95%" stopColor="#1890ff" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="month" />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <Tooltip />
                  <Area type="monotone" dataKey="revenue" stroke="#1890ff" fillOpacity={1} fill="url(#colorRev)" />
                  <Line type="monotone" dataKey="cost" stroke="#ffc658" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
      </Row>
    </AppLayout>
  );
}
