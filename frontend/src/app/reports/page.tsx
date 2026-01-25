'use client';

import React, { useState, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Select,
  DatePicker,
  Button,
  Table,
  Tabs,
  Statistic,
  Progress,
  Space,
  Tooltip,
  Typography,
  Alert,
} from 'antd';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
} from 'recharts';
import {
  DownloadOutlined,
  FileTextOutlined,
  BarChartOutlined,
  LineChartOutlined,
  PieChartOutlined,
  TeamOutlined,
  ProjectOutlined,
  DollarOutlined,
  TrophyOutlined,
} from '@ant-design/icons';
import { useAppSelector } from '@/lib/redux/hooks';
import { RootState } from '@/lib/redux/store';
import AppLayout from '@/components/layout/AppLayout';
import { apiClient } from '@/lib/utils/api';

const { RangePicker } = DatePicker;
const { Option } = Select;
const { TabPane } = Tabs;
const { Title, Text } = Typography;

interface ReportData {
  productivity_data: any[];
  project_performance: any[];
  team_workload: any[];
  financial_summary: any;
  sprint_velocity: any[];
  task_completion: any[];
  bug_trends: any[];
  asset_utilization: any[];
}

const ReportsPage: React.FC = () => {
  const { user } = useAppSelector((state: RootState) => state.auth);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('productivity');
  const [dateRange, setDateRange] = useState<any>(null);
  const [selectedProject, setSelectedProject] = useState<string>('all');
  const [selectedTeam, setSelectedTeam] = useState<string>('all');
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [projects, setProjects] = useState<any[]>([]);

  useEffect(() => {
    fetchReportData();
    fetchProjects();
  }, [dateRange, selectedProject, selectedTeam]);

  const fetchProjects = async () => {
    try {
      const response = await apiClient.get('/api/projects/my/');
      setProjects(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    }
  };

  const fetchReportData = async () => {
    setLoading(true);
    try {
      const params: any = {};
      
      if (dateRange) {
        params.start_date = dateRange[0].format('YYYY-MM-DD');
        params.end_date = dateRange[1].format('YYYY-MM-DD');
      }
      if (selectedProject !== 'all') {
        params.project_id = selectedProject;
      }
      if (selectedTeam !== 'all') {
        params.team_id = selectedTeam;
      }

      const response = await apiClient.get('/api/reports/analytics/', { params });
      setReportData(response.data);
    } catch (error) {
      console.error('Failed to fetch report data:', error);
    } finally {
      setLoading(false);
    }
  };

  const exportReport = async (reportType: string, format: string) => {
    try {
      const params: any = {
        report_type: reportType,
        format,
      };
      
      if (dateRange) {
        params.start_date = dateRange[0].format('YYYY-MM-DD');
        params.end_date = dateRange[1].format('YYYY-MM-DD');
      }

      const response = await apiClient.get('/api/reports/export/', {
        params,
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${reportType}-report.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export report:', error);
    }
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  const productivityColumns = [
    {
      title: 'Employee',
      dataIndex: 'employee_name',
      key: 'employee_name',
    },
    {
      title: 'Tasks Completed',
      dataIndex: 'tasks_completed',
      key: 'tasks_completed',
      sorter: (a: any, b: any) => a.tasks_completed - b.tasks_completed,
    },
    {
      title: 'Hours Logged',
      dataIndex: 'hours_logged',
      key: 'hours_logged',
      render: (hours: number) => `${hours.toFixed(1)}h`,
    },
    {
      title: 'Efficiency',
      dataIndex: 'efficiency',
      key: 'efficiency',
      render: (efficiency: number) => (
        <Progress
          percent={efficiency}
          size="small"
          status={efficiency >= 80 ? 'success' : efficiency >= 60 ? 'active' : 'exception'}
        />
      ),
    },
    {
      title: 'Avg Task Time',
      dataIndex: 'avg_task_time',
      key: 'avg_task_time',
      render: (time: number) => `${time.toFixed(1)}h`,
    },
  ];

  const projectColumns = [
    {
      title: 'Project',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Progress',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress: number) => (
        <Progress
          percent={progress}
          size="small"
          status={progress >= 80 ? 'success' : progress >= 50 ? 'active' : 'exception'}
        />
      ),
    },
    {
      title: 'Tasks',
      dataIndex: 'total_tasks',
      key: 'total_tasks',
      render: (tasks: number, record: any) => (
        `${record.completed_tasks}/${tasks}`
      ),
    },
    {
      title: 'Budget Used',
      dataIndex: 'budget_utilization',
      key: 'budget_utilization',
      render: (utilization: number) => (
        <Progress
          percent={utilization}
          size="small"
          status={utilization >= 90 ? 'exception' : utilization >= 70 ? 'active' : 'success'}
        />
      ),
    },
    {
      title: 'Team Size',
      dataIndex: 'team_size',
      key: 'team_size',
    },
  ];

  if (!reportData) {
    return (
    <AppLayout>
        <div style={{ padding: '24px' }}>
          <Card loading={true} />
        </div>
    </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div style={{ padding: '24px' }}>
        <div style={{ marginBottom: '24px' }}>
          <Title level={2}>Reports & Analytics</Title>
          
          <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
            <Col xs={24} sm={8} md={6}>
              <RangePicker
                style={{ width: '100%' }}
                onChange={setDateRange}
                placeholder={['Start Date', 'End Date']}
              />
            </Col>
            <Col xs={24} sm={8} md={6}>
              <Select
                style={{ width: '100%' }}
                value={selectedProject}
                onChange={setSelectedProject}
                placeholder="Select Project"
              >
                <Option value="all">All Projects</Option>
                {projects.map(project => (
                  <Option key={project.id} value={project.id}>
                    {project.name}
                  </Option>
                ))}
              </Select>
            </Col>
            <Col xs={24} sm={8} md={6}>
              <Select
                style={{ width: '100%' }}
                value={selectedTeam}
                onChange={setSelectedTeam}
                placeholder="Select Team"
              >
                <Option value="all">All Teams</Option>
                <Option value="engineering">Engineering</Option>
                <Option value="design">Design</Option>
                <Option value="qa">QA</Option>
              </Select>
            </Col>
            <Col xs={24} sm={24} md={6}>
              <Button
                type="primary"
                icon={<DownloadOutlined />}
                style={{ width: '100%' }}
                onClick={() => exportReport(activeTab, 'pdf')}
              >
                Export Report
              </Button>
            </Col>
          </Row>
        </div>

        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab={<span><BarChartOutlined />Productivity</span>} key="productivity">
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={16}>
                <Card title="Team Productivity Trends" loading={loading}>
                  <ResponsiveContainer width="100%" height={400}>
                    <AreaChart data={reportData.productivity_data}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <RechartsTooltip />
                      <Area
                        type="monotone"
                        dataKey="tasks_completed"
                        stackId="1"
                        stroke="#8884d8"
                        fill="#8884d8"
                      />
                      <Area
                        type="monotone"
                        dataKey="hours_logged"
                        stackId="2"
                        stroke="#82ca9d"
                        fill="#82ca9d"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
              <Col xs={24} lg={8}>
                <Card title="Top Performers" loading={loading}>
                  {reportData.productivity_data.slice(0, 5).map((employee: any, index: number) => (
                    <div key={index} style={{ marginBottom: '16px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <Text strong>{employee.employee_name}</Text>
                        <TrophyOutlined style={{ color: index < 3 ? '#faad14' : '#8c8c8c' }} />
                      </div>
                      <Progress
                        percent={employee.efficiency}
                        size="small"
                        status={employee.efficiency >= 80 ? 'success' : 'active'}
                      />
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        {employee.tasks_completed} tasks completed
                      </Text>
                    </div>
                  ))}
                </Card>
              </Col>
            </Row>
            
            <Card title="Detailed Productivity Report" style={{ marginTop: '16px' }} loading={loading}>
              <Table
                columns={productivityColumns}
                dataSource={reportData.productivity_data}
                rowKey="employee_id"
                pagination={{
                  showSizeChanger: true,
                  showQuickJumper: true,
                }}
              />
            </Card>
          </TabPane>

          <TabPane tab={<span><ProjectOutlined />Projects</span>} key="projects">
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Card title="Project Progress Distribution" loading={loading}>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={reportData.project_performance}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }: any) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="progress"
                      >
                        {reportData.project_performance.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
              <Col xs={24} lg={12}>
                <Card title="Budget Utilization" loading={loading}>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={reportData.project_performance}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="budget_utilization" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
            </Row>
            
            <Card title="Project Performance Summary" style={{ marginTop: '16px' }} loading={loading}>
              <Table
                columns={projectColumns}
                dataSource={reportData.project_performance}
                rowKey="id"
                pagination={{
                  showSizeChanger: true,
                  showQuickJumper: true,
                }}
              />
            </Card>
          </TabPane>

          <TabPane tab={<span><DollarOutlined />Financial</span>} key="financial">
            {reportData.financial_summary && (
              <>
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={8}>
                    <Card>
                      <Statistic
                        title="Total Revenue"
                        value={reportData.financial_summary.total_revenue}
                        precision={2}
                        valueStyle={{ color: '#3f8600' }}
                        prefix={<DollarOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={8}>
                    <Card>
                      <Statistic
                        title="Total Expenses"
                        value={reportData.financial_summary.total_expenses}
                        precision={2}
                        valueStyle={{ color: '#cf1322' }}
                        prefix={<DollarOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={8}>
                    <Card>
                      <Statistic
                        title="Profit Margin"
                        value={reportData.financial_summary.profit_margin}
                        precision={2}
                        suffix="%"
                        valueStyle={{ 
                          color: reportData.financial_summary.profit_margin >= 0 ? '#3f8600' : '#cf1322' 
                        }}
                      />
                    </Card>
                  </Col>
                </Row>
                
                <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
                  <Col xs={24}>
                    <Card title="Revenue vs Expenses Trend" loading={loading}>
                      <ResponsiveContainer width="100%" height={400}>
                        <LineChart data={reportData.financial_summary.monthly_data}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="month" />
                          <YAxis />
                          <RechartsTooltip />
                          <Line type="monotone" dataKey="revenue" stroke="#3f8600" strokeWidth={2} />
                          <Line type="monotone" dataKey="expenses" stroke="#cf1322" strokeWidth={2} />
                          <Line type="monotone" dataKey="profit" stroke="#1890ff" strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    </Card>
                  </Col>
                </Row>
              </>
            )}
          </TabPane>

          <TabPane tab={<span><TeamOutlined />Team</span>} key="team">
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Card title="Team Workload Distribution" loading={loading}>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={reportData.team_workload}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="team" />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="active_tasks" fill="#8884d8" />
                      <Bar dataKey="completed_tasks" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
              <Col xs={24} lg={12}>
                <Card title="Sprint Velocity Trends" loading={loading}>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={reportData.sprint_velocity}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="sprint" />
                      <YAxis />
                      <RechartsTooltip />
                      <Line type="monotone" dataKey="velocity" stroke="#8884d8" strokeWidth={2} />
                      <Line type="monotone" dataKey="capacity" stroke="#82ca9d" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
            </Row>
            
            <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
              <Col xs={24}>
                <Card title="Task Completion Trends" loading={loading}>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={reportData.task_completion}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="week" />
                      <YAxis />
                      <RechartsTooltip />
                      <Area type="monotone" dataKey="completed" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
                      <Area type="monotone" dataKey="in_progress" stackId="1" stroke="#8884d8" fill="#8884d8" />
                      <Area type="monotone" dataKey="todo" stackId="1" stroke="#ffc658" fill="#ffc658" />
                    </AreaChart>
                  </ResponsiveContainer>
                </Card>
              </Col>
            </Row>
          </TabPane>
        </Tabs>
      </div>
    </AppLayout>
  );
};

export default ReportsPage;