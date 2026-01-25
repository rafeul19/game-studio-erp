'use client';

import React, { useState } from 'react';
import {
  Row,
  Col,
  Card,
  Tag,
  Typography,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Select,
  Dropdown,
  Avatar,
  Tooltip,
  App,
} from 'antd';
import {
  PlusOutlined,
  BugOutlined,
  MoreOutlined,
  UserOutlined,
} from '@ant-design/icons';
import AppLayout from '@/components/layout/AppLayout';
import { useGetBugsQuery, useCreateBugMutation, useUpdateBugMutation } from '@/store/api/bugApi';
import { useGetProjectsQuery } from '@/store/api/projectApi';
import { Bug } from '@/types/models';

const { Title, Text } = Typography;
const { Option } = Select;

const BUG_COLUMNS = [
  { id: 'TRIAGE', title: 'Triage', color: '#8c8c8c' },
  { id: 'IN_PROGRESS', title: 'Fixing', color: '#1890ff' },
  { id: 'BLOCKED', title: 'Blocked', color: '#ff4d4f' },
  { id: 'RESOLVED', title: 'Resolved', color: '#52c41a' },
];

export default function BugsPage() {
  const { data: bugs } = useGetBugsQuery({});
  const { data: projects } = useGetProjectsQuery({});
  const [createBug, { isLoading: isCreating }] = useCreateBugMutation();
  const [updateBug] = useUpdateBugMutation();
  
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const { message } = App.useApp();

  const handleStatusChange = async (bugId: number, newStatus: Bug['status']) => {
    try {
      await updateBug({ id: bugId, data: { status: newStatus } }).unwrap();
      message.success('Bug status updated');
    } catch {
      message.error('Failed to update bug');
    }
  };

  const handleCreate = async (values: Partial<Bug>) => {
    try {
      await createBug(values).unwrap();
      message.success('Bug reported successfully');
      setIsModalVisible(false);
      form.resetFields();
    } catch {
      message.error('Failed to report bug');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'volcano';
      case 'HIGH': return 'orange';
      case 'MEDIUM': return 'blue';
      case 'LOW': return 'default';
      default: return 'default';
    }
  };

  return (
    <AppLayout>
      <div className="flex justify-between items-center mb-6">
        <div>
          <Title level={2}>Bug Tracking</Title>
          <Text type="secondary">Studio-wide QA and issue management workflow</Text>
        </div>
        <Button
          type="primary"
          danger
          icon={<PlusOutlined />}
          size="large"
          onClick={() => setIsModalVisible(true)}
          className="bg-red-600 border-none"
        >
          Report Bug
        </Button>
      </div>

      <Row gutter={16} style={{ flexWrap: 'nowrap', overflowX: 'auto', paddingBottom: '16px' }}>
        {BUG_COLUMNS.map((column) => (
          <Col key={column.id} style={{ width: 300, flexShrink: 0 }}>
            <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg flex flex-col h-full min-h-[600px]">
              <div className="flex justify-between items-center mb-4 px-1">
                <Space>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: column.color }} />
                  <Text strong>{column.title}</Text>
                  <Tag className="rounded-full px-2 border-none bg-gray-200 dark:bg-gray-700">
                    {bugs?.filter((b: Bug) => b.status === column.id).length || 0}
                  </Tag>
                </Space>
                <Button type="text" size="small" icon={<MoreOutlined />} />
              </div>

              <div className="flex-1 space-y-3">
                {bugs?.filter((b: Bug) => b.status === column.id).map((bug: Bug & { reporter_name?: string; assignee_name?: string; project_name?: string }) => (
                  <Card
                    key={bug.id}
                    size="small"
                    className="shadow-sm hover:shadow-md transition-shadow cursor-pointer border-l-4"
                    style={{ borderLeftColor: getSeverityColor(bug.severity) === 'volcano' ? '#ff4d4f' : 
                                            getSeverityColor(bug.severity) === 'orange' ? '#faad14' : 
                                            getSeverityColor(bug.severity) === 'blue' ? '#1890ff' : '#d9d9d9' }}
                    variant="borderless"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <Tag color={getSeverityColor(bug.severity)} className="text-[10px] uppercase font-bold px-1.5 leading-tight">
                        {bug.severity}
                      </Tag>
                      <Text type="secondary" className="text-xs">#{bug.id}</Text>
                    </div>
                    <Text strong className="block mb-2">{bug.title}</Text>
                    <Text type="secondary" className="block text-xs mb-3 truncate">{bug.project_name}</Text>
                    
                    <div className="flex justify-between items-center">
                      <Space>
                        <Tooltip title={`Reported by ${bug.reporter_name}`}>
                          <Avatar size="small" icon={<UserOutlined />} className="bg-gray-400" />
                        </Tooltip>
                        {bug.assignee_name && (
                          <Tooltip title={`Assigned to ${bug.assignee_name}`}>
                            <Avatar size="small" icon={<UserOutlined />} className="bg-blue-400" />
                          </Tooltip>
                        )}
                      </Space>
                      
                      <Dropdown
                        menu={{
                          items: BUG_COLUMNS.filter(c => c.id !== column.id).map(c => ({
                            key: c.id,
                            label: `Move to ${c.title}`,
                            onClick: () => handleStatusChange(bug.id, c.id as Bug['status'])
                          }))
                        }}
                      >
                         <Button type="text" size="small" icon={<MoreOutlined />} />
                      </Dropdown>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </Col>
        ))}
      </Row>

      <Modal
        title={
          <Space>
            <BugOutlined className="text-red-500" />
            <span>Report New Bug</span>
          </Space>
        }
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        destroyOnHidden
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreate}
          initialValues={{ severity: 'MEDIUM', status: 'TRIAGE' }}
        >
          <Form.Item
            name="title"
            label="Bug Title"
            rules={[{ required: true, message: 'Please summarize the issue' }]}
          >
            <Input placeholder="e.g. Player falls through terrain in Level 2" />
          </Form.Item>

          <Row gutter={16}>
             <Col span={12}>
                <Form.Item name="project" label="Project" rules={[{ required: true }]}>
                  <Select placeholder="Select project">
                    {projects?.map((p: { id: number; name: string }) => (
                      <Option key={p.id} value={p.id}>{p.name}</Option>
                    ))}
                  </Select>
                </Form.Item>
             </Col>
             <Col span={12}>
                <Form.Item name="severity" label="Severity">
                  <Select>
                    <Option value="LOW">Low</Option>
                    <Option value="MEDIUM">Medium</Option>
                    <Option value="HIGH">High</Option>
                    <Option value="CRITICAL">Critical</Option>
                  </Select>
                </Form.Item>
             </Col>
          </Row>

          <Form.Item
            name="description"
            label="Reproduction Steps / Details"
            rules={[{ required: true, message: 'Please provide details' }]}
          >
            <Input.TextArea rows={4} placeholder="1. Open Game&#10;2. Go to...&#10;3. Observe..." />
          </Form.Item>

          <Form.Item className="mb-0 text-right">
            <Space>
              <Button onClick={() => setIsModalVisible(false)}>Cancel</Button>
              <Button type="primary" danger htmlType="submit" loading={isCreating}>
                Submit Bug Report
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
}
