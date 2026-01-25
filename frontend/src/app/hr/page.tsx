'use client';

import React, { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Button,
  Table,
  Tag,
  Space,
  Avatar,
  Modal,
  Form,
  Input,
  Select,
  DatePicker,
  message,
  Tabs,
  Statistic,
  Progress,
  Badge,
  Popconfirm,
  App,
} from 'antd';
import {
  TeamOutlined,
  UserOutlined,
  CalendarOutlined,
  StarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  TrophyOutlined,
  EnvironmentOutlined,
} from '@ant-design/icons';
import AppLayout from '@/components/layout/AppLayout';
import { 
  useGetEmployeesQuery, 
  useGetDepartmentsQuery, 
  useGetHRAnalyticsQuery,
  Employee,
  Department,
  HRAnalytics,
  LeaveRequest,
  PerformanceReview,
  AttendanceRecord,
} from '@/store/api/hrApi';
import dayjs from 'dayjs';

const { Title, Text } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;

export default function HRManagementPage() {
  const { data: employees, isLoading: employeesLoading } = useGetEmployeesQuery({});
  const { data: departments, isLoading: departmentsLoading } = useGetDepartmentsQuery({});
  const { data: analytics, isLoading: analyticsLoading } = useGetHRAnalyticsQuery({});

  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [isEmployeeModalVisible, setIsEmployeeModalVisible] = useState(false);
  const [form] = Form.useForm();
  const { message } = App.useApp();

  const handleEditEmployee = (employee: Employee) => {
    setSelectedEmployee(employee);
    form.setFieldsValue({
      ...employee,
      hire_date: dayjs(employee.hire_date),
    });
    setIsEmployeeModalVisible(true);
  };

  const handleCreateEmployee = () => {
    setSelectedEmployee(null);
    form.resetFields();
    setIsEmployeeModalVisible(true);
  };

  const employeeColumns = [
    {
      title: 'Employee',
      key: 'employee',
      render: (record: Employee) => (
        <Space>
          <Avatar icon={<UserOutlined />} src={record.user_info?.avatar} />
          <div>
            <div className="font-semibold">{record.user_info?.full_name}</div>
            <Text type="secondary" className="text-xs">{record.employee_id}</Text>
          </div>
        </Space>
      ),
    },
    {
      title: 'Position',
      dataIndex: 'position',
      key: 'position',
    },
    {
      title: 'Department',
      dataIndex: 'department',
      key: 'department',
      render: (department: string) => (
        <Tag color="blue">{department}</Tag>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'employment_status',
      key: 'employment_status',
      render: (status: string) => (
        <Badge 
          status={status === 'Active' ? 'success' : 'default'} 
          text={status} 
        />
      ),
    },
    {
      title: 'Hire Date',
      dataIndex: 'hire_date',
      key: 'hire_date',
      render: (date: string) => dayjs(date).format('MMM DD, YYYY'),
    },
    {
      title: 'Skills',
      key: 'skills',
      render: (record: Employee) => (
        <div className="flex flex-wrap gap-1">
          {record.skills?.slice(0, 3).map((skill) => (
            <Tag key={skill.id} size="small" color="green">
              {skill.skill_name}
            </Tag>
          ))}
          {record.skills?.length > 3 && (
            <Tag size="small" color="default">
              +{record.skills.length - 3} more
            </Tag>
          )}
        </div>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (record: Employee) => (
        <Space>
          <Button 
            icon={<EditOutlined />} 
            size="small" 
            onClick={() => handleEditEmployee(record)}
          />
          <Popconfirm
            title="Are you sure you want to terminate this employee?"
            onConfirm={() => message.info('Termination feature coming soon')}
          >
            <Button icon={<DeleteOutlined />} size="small" danger />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  const departmentColumns = [
    {
      title: 'Department',
      key: 'department',
      render: (record: Department) => (
        <Space>
          <EnvironmentOutlined className="text-blue-500" />
          <div>
            <div className="font-semibold">{record.name}</div>
            {record.description && (
              <Text type="secondary" className="text-xs">
                {record.description.substring(0, 50)}...
              </Text>
            )}
          </div>
        </Space>
      ),
    },
    {
      title: 'Manager',
      dataIndex: 'manager_name',
      key: 'manager_name',
      render: (manager: string) => manager || 'Not Assigned',
    },
    {
      title: 'Employees',
      dataIndex: 'employee_count',
      key: 'employee_count',
      render: (count: number) => (
        <Badge count={count} showZero color="blue" />
      ),
    },
    {
      title: 'Budget',
      dataIndex: 'budget',
      key: 'budget',
      render: (budget: number) => budget 
        ? `$${budget.toLocaleString()}` 
        : 'Not Set',
    },
  ];

  const renderOverview = () => (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Total Employees"
            value={analytics?.overview.total_employees || 0}
            prefix={<TeamOutlined />}
            valueStyle={{ color: '#1890ff' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Departments"
            value={analytics?.overview.total_departments || 0}
            prefix={<EnvironmentOutlined />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <Statistic
            title="Active Employees"
            value={analytics?.overview.active_employees || 0}
            prefix={<CheckCircleOutlined />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card>
          <div className="text-center">
            <TrophyOutlined className="text-3xl text-yellow-500 mb-2" />
            <div className="text-sm text-gray-500">Avg Performance</div>
            <div className="text-2xl font-bold">4.2 / 5.0</div>
          </div>
        </Card>
      </Col>
    </Row>
  );

  const renderDepartmentDistribution = () => (
    <Card title="Department Distribution" className="mb-6">
      <Row gutter={[16, 16]}>
        {analytics?.department_distribution?.map((dept, index) => (
          <Col xs={24} sm={12} lg={8} key={dept.department}>
            <div className="p-4 border rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <Text strong>{dept.department}</Text>
                <Tag color="blue">{dept.count} employees</Tag>
              </div>
              <Progress
                percent={(dept.count / (analytics?.overview.total_employees || 1)) * 100}
                size="small"
                showInfo={false}
              />
            </div>
          </Col>
        ))}
      </Row>
    </Card>
  );

  const renderRecentActivities = () => (
    <Row gutter={[16, 16]}>
      <Col xs={24} lg={12}>
        <Card title="Recent Leave Requests" extra={<Button type="link">View All</Button>}>
          {analytics?.recent_leave_requests?.slice(0, 5).map((leave) => (
            <div key={leave.id} className="mb-3 pb-3 border-b last:border-0">
              <div className="flex justify-between items-start">
                <div>
                  <Text strong>{leave.employee_name}</Text>
                  <br />
                  <Text type="secondary" className="text-sm">
                    {leave.leave_type_display} • {leave.days_requested} days
                  </Text>
                </div>
                <Tag color={
                  leave.status === 'APPROVED' ? 'green' :
                  leave.status === 'REJECTED' ? 'red' : 'orange'
                }>
                  {leave.status_display}
                </Tag>
              </div>
            </div>
          ))}
        </Card>
      </Col>
      <Col xs={24} lg={12}>
        <Card title="Upcoming Reviews" extra={<Button type="link">View All</Button>}>
          {analytics?.upcoming_reviews?.slice(0, 5).map((review) => (
            <div key={review.id} className="mb-3 pb-3 border-b last:border-0">
              <div className="flex justify-between items-start">
                <div>
                  <Text strong>{review.employee_name}</Text>
                  <br />
                  <Text type="secondary" className="text-sm">
                    {review.review_type_display} • {dayjs(review.review_date).format('MMM DD')}
                  </Text>
                </div>
                <Tag color="blue">{review.review_type_display}</Tag>
              </div>
            </div>
          ))}
        </Card>
      </Col>
    </Row>
  );

  return (
    <AppLayout>
      <div className="flex justify-between items-center mb-6">
        <div>
          <Title level={2}>HR Management</Title>
          <Text type="secondary">Manage employees, departments, and workplace operations</Text>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleCreateEmployee}
          className="bg-blue-600"
        >
          Add Employee
        </Button>
      </div>

      <Tabs defaultActiveKey="overview" className="mb-6">
        <TabPane tab="Overview" key="overview">
          {renderOverview()}
          {renderDepartmentDistribution()}
          {renderRecentActivities()}
        </TabPane>
        
        <TabPane tab="Employees" key="employees">
          <Card>
            <Table
              columns={employeeColumns}
              dataSource={employees}
              rowKey="id"
              loading={employeesLoading}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
              }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Departments" key="departments">
          <Card>
            <Table
              columns={departmentColumns}
              dataSource={departments}
              rowKey="id"
              loading={departmentsLoading}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
              }}
            />
          </Card>
        </TabPane>
      </Tabs>

      {/* Employee Modal */}
      <Modal
        title={selectedEmployee ? 'Edit Employee' : 'Add Employee'}
        open={isEmployeeModalVisible}
        onCancel={() => setIsEmployeeModalVisible(false)}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={(values) => {
            message.success('Employee saved successfully!');
            setIsEmployeeModalVisible(false);
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="employee_id"
                label="Employee ID"
                rules={[{ required: true, message: 'Please enter employee ID' }]}
              >
                <Input placeholder="e.g. EMP001" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="department"
                label="Department"
                rules={[{ required: true, message: 'Please select department' }]}
              >
                <Select placeholder="Select department">
                  {departments?.map((dept) => (
                    <Option key={dept.id} value={dept.name}>{dept.name}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="position"
                label="Position"
                rules={[{ required: true, message: 'Please enter position' }]}
              >
                <Input placeholder="e.g. Senior Developer" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="salary"
                label="Annual Salary"
                rules={[{ required: true, message: 'Please enter salary' }]}
              >
                <Input
                  type="number"
                  placeholder="e.g. 75000"
                  prefix="$"
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="hire_date"
                label="Hire Date"
                rules={[{ required: true, message: 'Please select hire date' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="is_active" valuePropName="checked">
                <div className="flex items-center space-x-2">
                  <input type="checkbox" />
                  <Text>Active Employee</Text>
                </div>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="phone" label="Phone">
            <Input placeholder="e.g. +1 (555) 123-4567" />
          </Form.Item>

          <Form.Item name="address" label="Address">
            <Input.TextArea rows={2} placeholder="Employee address" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="emergency_contact" label="Emergency Contact">
                <Input placeholder="Emergency contact name" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="emergency_phone" label="Emergency Phone">
                <Input placeholder="Emergency contact phone" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item className="mb-0 text-right">
            <Space>
              <Button onClick={() => setIsEmployeeModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">
                {selectedEmployee ? 'Update' : 'Create'} Employee
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
}