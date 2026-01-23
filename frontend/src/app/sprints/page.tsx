'use client';

import React, { useState } from 'react';
import {
  Row,
  Col,
  Card,
  Typography,
  Table,
  Tag,
  Button,
  Progress,
  Space,
  Modal,
  Form,
  Input,
  DatePicker,
  Select,
  message,
  Alert,
  Statistic,
} from 'antd';
import {
  PlusOutlined,
  DashboardOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  RobotOutlined,
} from '@ant-design/icons';
import { AppLayout } from '@/components/layout/AppLayout';
import {
  useGetProjectSprintsQuery,
  useCreateSprintMutation,
  useGetSprintRiskQuery,
} from '@/store/api/sprintApi';
import { useGetProjectsQuery } from '@/store/api/projectApi';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

export default function SprintsPage() {
  const { data: projects } = useGetProjectsQuery({});
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const { data: sprints, isLoading } = useGetProjectSprintsQuery(selectedProjectId, {
    skip: !selectedProjectId,
  });
  const [createSprint, { isLoading: isCreating }] = useCreateSprintMutation();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const handleProjectChange = (value: number) => {
    setSelectedProjectId(value);
  };

  const onFinish = async (values: any) => {
    try {
      const payload = {
        ...values,
        project: selectedProjectId,
        start_date: values.dates[0].format('YYYY-MM-DD'),
        end_date: values.dates[1].format('YYYY-MM-DD'),
      };
      await createSprint(payload).unwrap();
      message.success('Sprint created successfully');
      setIsModalVisible(false);
      form.resetFields();
    } catch (err) {
      message.error('Failed to create sprint');
    }
  };

  const columns = [
    {
      title: 'Sprint Name',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <Text strong>{text}</Text>,
    },
    {
      title: 'Duration',
      key: 'duration',
      render: (_: any, record: any) => `${record.start_date} to ${record.end_date}`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const colors: any = { ACTIVE: 'blue', COMPLETED: 'green', PLANNED: 'default' };
        return <Tag color={colors[status] || 'default'}>{status}</Tag>;
      },
    },
    {
      title: 'AI Risk',
      key: 'risk',
      render: (_: any, record: any) => {
        // This would ideally come from the useGetSprintRiskQuery
        // For demonstration, we'll show a sample AI risk badge
        return (
          <Space>
            <Tag icon={<RobotOutlined />} color="orange">MEDIUM RISK</Tag>
          </Space>
        );
      },
    },
    {
      title: 'Progress',
      key: 'progress',
      render: (_: any, record: any) => (
        <Progress percent={record.completion_percentage || 0} size="small" />
      ),
    },
  ];

  return (
    <AppLayout>
      <div className="flex justify-between items-center mb-6">
        <div>
          <Title level={2}>Sprints & Cycles</Title>
          <Text type="secondary">Manage agile game development cycles and predict risks</Text>
        </div>
        <Space>
          <Select
            placeholder="Select a project"
            style={{ width: 250 }}
            onChange={handleProjectChange}
            options={projects?.map((p: any) => ({ label: p.name, value: p.id }))}
          />
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
            disabled={!selectedProjectId}
            className="bg-blue-600"
          >
            Start Sprint
          </Button>
        </Space>
      </div>

      {!selectedProjectId ? (
        <Alert
          message="No Project Selected"
          description="Please select a project from the dropdown above to view and manage sprints."
          type="info"
          showIcon
          className="rounded-lg"
        />
      ) : (
        <>
          <Row gutter={[16, 16]} className="mb-6">
            <Col span={8}>
              <Card size="small" className="shadow-sm">
                <Statistic
                  title="Avg Velocity"
                  value={42.5}
                  precision={1}
                  prefix={<DashboardOutlined />}
                  suffix="pts"
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card size="small" className="shadow-sm">
                <Statistic
                  title="Success Rate"
                  value={88}
                  suffix="%"
                  prefix={<CheckCircleOutlined />}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card size="small" className="shadow-sm">
                <Statistic
                  title="At Risk Tasks"
                  value={5}
                  valueStyle={{ color: '#cf1322' }}
                  prefix={<WarningOutlined />}
                />
              </Card>
            </Col>
          </Row>

          <Card bordered={false} className="shadow-sm">
            <Table
              dataSource={sprints}
              columns={columns}
              loading={isLoading}
              rowKey="id"
              pagination={false}
            />
          </Card>
        </>
      )}

      <Modal
        title="Initialize New Sprint"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{ status: 'PLANNED' }}
        >
          <Form.Item
            name="name"
            label="Sprint Name"
            rules={[{ required: true, message: 'Please enter sprint name' }]}
          >
            <Input placeholder="e.g. Sprint 01 - Core Mechanics" />
          </Form.Item>

          <Form.Item
            name="dates"
            label="Sprint Duration"
            rules={[{ required: true, message: 'Please select dates' }]}
          >
            <RangePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="goal"
            label="Sprint Goal"
          >
            <Input.TextArea rows={3} placeholder="What do we want to achieve?" />
          </Form.Item>

          <Form.Item className="mb-0 text-right">
            <Space>
              <Button onClick={() => setIsModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit" loading={isCreating}>
                Create Sprint
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
}
