'use client';

import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, Typography, Table, Tag, Spin, Alert } from 'antd';
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
  AreaChart,
  Area,
  Line,
} from 'recharts';
import AppLayout from '@/components/layout/AppLayout';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const { Title, Text } = Typography;

// Mock revenue for now as it wasn't in the initial scope of the fix, preserving UI
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

interface DashboardStats {
  active_projects: number;
  completed_tasks: number;
  pending_approval: number;
  open_bugs: number;
  sprint_data: any[];
  project_data: any[];
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('access');
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/dashboard/stats/`, { headers });
        setStats(response.data);
      } catch (err: any) {
        if (err.response && err.response.status === 401) {
             router.push('/login');
             return;
        }
        console.error("Failed to fetch dashboard stats", err);
        setError('Failed to load dashboard statistics.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [router]);

  if (loading) {
    return (
      <AppLayout>
        <div className="flex flex-col justify-center items-center h-screen">
          <Spin size="large" />
          <div className="mt-4 text-gray-600">Loading Dashboard...</div>
        </div>
      </AppLayout>
    );
  }

  if (error) {
    return (
      <AppLayout>
         <Alert message="Error" description={error} type="error" showIcon />
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="mb-6">
        <Title level={2}>Studio Dashboard</Title>
        <Text type="secondary">Real-time overview of your game development projects</Text>
      </div>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card variant="borderless" className="shadow-sm">
            <Statistic
              title="Active Projects"
              value={stats?.active_projects || 0}
              prefix={<ProjectOutlined className="text-blue-500" />}
            />
            <div className="mt-2 text-green-500">
              <ArrowUpOutlined /> <Text type="success">Live Data</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card variant="borderless" className="shadow-sm">
            <Statistic
              title="Tasks Completed"
              value={stats?.completed_tasks || 0}
              prefix={<CheckCircleOutlined className="text-green-500" />}
            />
            <div className="mt-2 text-green-500">
              <ArrowUpOutlined /> <Text type="success">Total finished</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card variant="borderless" className="shadow-sm">
            <Statistic
              title="Pending Approval"
              value={stats?.pending_approval || 0}
              prefix={<ClockCircleOutlined className="text-orange-500" />}
            />
             <div className="mt-2 text-gray-500">
              <Text type="secondary">In Review</Text>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card variant="borderless" className="shadow-sm">
            <Statistic
              title="Open Bugs"
              value={stats?.open_bugs || 0}
              prefix={<WarningOutlined className="text-red-500" />}
            />
            <div className="mt-2 text-red-500">
               <Text type="danger">Needs attention</Text>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="mt-6">
        <Col xs={24} lg={16}>
          <Card title="Sprint Velocity & Trends" variant="borderless" className="shadow-sm">
            <div style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer>
                <BarChart data={stats?.sprint_data || []}>
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
          <Card title="Recent Projects" variant="borderless" className="shadow-sm">
            <Table
              columns={projectColumns}
              dataSource={stats?.project_data || []}
              pagination={false}
              size="small"
              rowKey="id"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="mt-6">
        <Col span={24}>
           <Card title="Revenue vs Development Cost" variant="borderless" className="shadow-sm">
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
