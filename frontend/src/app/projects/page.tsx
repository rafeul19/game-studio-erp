'use client';

import React, { useState } from 'react';
import {
  Table,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Select,
  Typography,
  Card,
  Tag,
  App,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons';
import { AppLayout } from '@/components/layout/AppLayout';
import { useGetProjectsQuery, useCreateProjectMutation } from '@/store/api/projectApi';
import { Project } from '@/types/models';

const { Title, Text } = Typography;
const { Option } = Select;

export default function ProjectsPage() {
  const { data: projects, isLoading } = useGetProjectsQuery({});
  const [createProject, { isLoading: isCreating }] = useCreateProjectMutation();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const { message } = App.useApp();

  const showModal = () => setIsModalVisible(true);
  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
  };

  const onFinish = async (values: Partial<Project>) => {
    try {
      await createProject(values).unwrap();
      message.success('Project created successfully');
      setIsModalVisible(false);
      form.resetFields();
    } catch {
      message.error('Failed to create project');
    }
  };

  const columns = [
    {
      title: 'Project Name',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <Text strong>{text}</Text>,
    },
    {
      title: 'Type',
      dataIndex: 'budget_type',
      key: 'budget_type',
      render: (type: string) => <Tag color="blue">{type}</Tag>,
    },
    {
      title: 'Manager',
      dataIndex: 'manager_name',
      key: 'manager_name',
    },
    {
      title: 'Budget',
      dataIndex: 'total_budget',
      key: 'total_budget',
      render: (budget: number) => `$${budget?.toLocaleString()}`,
    },
    {
        title: 'Actions',
        key: 'actions',
        render: (_: unknown, record: Project) => (
          <Space size="middle">
            <Button type="text" icon={<EyeOutlined />} onClick={() => message.info(`Viewing ${record.name}`)} />
            <Button type="text" icon={<EditOutlined />} />
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Space>
        ),
      },
  ];

  return (
    <AppLayout>
      <div className="flex justify-between items-center mb-6">
        <div>
          <Title level={2}>Projects</Title>
          <Text type="secondary">Manage your studio&apos;s game projects and resources</Text>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          size="large"
          onClick={showModal}
          className="bg-blue-600"
        >
          New Project
        </Button>
      </div>

      <Card variant="borderless" className="shadow-sm">
        <Table
          dataSource={projects}
          columns={columns}
          loading={isLoading}
          rowKey="id"
        />
      </Card>

      <Modal
        title="Create New Project"
        open={isModalVisible}
        onCancel={handleCancel}
        footer={null}
        destroyOnHidden
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{ budget_type: 'FIXED' }}
        >
          <Form.Item
            name="name"
            label="Project Name"
            rules={[{ required: true, message: 'Please enter project name' }]}
          >
            <Input placeholder="e.g. Cyberpunk Odyssey" />
          </Form.Item>

          <Form.Item
            name="budget_type"
            label="Budget Type"
          >
            <Select>
              <Option value="FIXED">Fixed Budget</Option>
              <Option value="T&M">Time & Materials</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="total_budget"
            label="Total Budget ($)"
            rules={[{ required: true, message: 'Please enter budget' }]}
          >
            <Input type="number" placeholder="50000" />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
          >
            <Input.TextArea rows={4} placeholder="Project goals, milestones, etc." />
          </Form.Item>

          <Form.Item className="mb-0 text-right">
            <Space>
              <Button onClick={handleCancel}>Cancel</Button>
              <Button type="primary" htmlType="submit" loading={isCreating}>
                Create Project
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
}
