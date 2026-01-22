'use client';

import React, { useState } from 'react';
import {
  Row,
  Col,
  Card,
  Tag,
  Typography,
  Avatar,
  Tooltip,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Select,
  message,
  Dropdown,
} from 'antd';
import {
  PlusOutlined,
  MoreOutlined,
  UserOutlined,
  ClockCircleOutlined,
  FireOutlined,
} from '@ant-design/icons';
import { AppLayout } from '@/components/layout/AppLayout';
import { useGetTasksQuery, useUpdateTaskStatusMutation, useCreateTaskMutation } from '@/store/api/taskApi';
import { useGetProjectsQuery } from '@/store/api/projectApi';

const { Title, Text } = Typography;
const { Option } = Select;

const COLUMNS = [
  { id: 'TODO', title: 'To Do', color: '#d9d9d9' },
  { id: 'IN_PROGRESS', title: 'In Progress', color: '#1890ff' },
  { id: 'REVIEW', title: 'Review', color: '#faad14' },
  { id: 'DONE', title: 'Done', color: '#52c41a' },
];

export default function TasksPage() {
  const { data: tasks, isLoading } = useGetTasksQuery({});
  const { data: projects } = useGetProjectsQuery({});
  const [updateStatus] = useUpdateTaskStatusMutation();
  const [createTask, { isLoading: isCreating }] = useCreateTaskMutation();
  
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      await updateStatus({ id: taskId, status: newStatus }).unwrap();
      message.success('Task updated');
    } catch (err) {
      message.error('Failed to update task');
    }
  };

  const onFinish = async (values: any) => {
    try {
      await createTask(values).unwrap();
      message.success('Task created successfully');
      setIsModalVisible(false);
      form.resetFields();
    } catch (err) {
      message.error('Failed to create task');
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'URGENT': return 'volcano';
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
          <Title level={2}>Task Board</Title>
          <Text type="secondary">Track progress across all development workflows</Text>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          size="large"
          onClick={() => setIsModalVisible(true)}
          className="bg-blue-600"
        >
          Create Task
        </Button>
      </div>

      <Row gutter={16} style={{ flexWrap: 'nowrap', overflowX: 'auto', paddingBottom: '16px' }}>
        {COLUMNS.map((column) => (
          <Col key={column.id} style={{ width: 300, flexShrink: 0 }}>
            <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg flex flex-col h-full min-h-[600px]">
              <div className="flex justify-between items-center mb-4 px-1">
                <Space>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: column.color }} />
                  <Text strong>{column.title}</Text>
                  <Tag className="rounded-full px-2 border-none bg-gray-200 dark:bg-gray-700">
                    {tasks?.filter((t: any) => t.status === column.id).length || 0}
                  </Tag>
                </Space>
                <Button type="text" size="small" icon={<MoreOutlined />} />
              </div>

              <div className="flex-1 space-y-3">
                {tasks?.filter((t: any) => t.status === column.id).map((task: any) => (
                  <Card
                    key={task.id}
                    size="small"
                    className="shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                    bordered={false}
                  >
                    <div className="mb-2">
                       <Tag color={getPriorityColor(task.priority)} className="text-[10px] uppercase font-bold px-1.5 leading-tight">
                         {task.priority}
                       </Tag>
                    </div>
                    <Text strong className="block mb-2">{task.title}</Text>
                    <div className="flex justify-between items-center mt-4">
                      <Space>
                        <Tooltip title={task.assignee_name}>
                          <Avatar size="small" icon={<UserOutlined />} src={task.assignee_avatar} />
                        </Tooltip>
                        {task.story_points && (
                          <Tag icon={<FireOutlined />} className="m-0 border-none bg-orange-50 text-orange-600">
                            {task.story_points}
                          </Tag>
                        )}
                      </Space>
                      <Dropdown
                        menu={{
                          items: COLUMNS.filter(c => c.id !== column.id).map(c => ({
                            key: c.id,
                            label: `Move to ${c.title}`,
                            onClick: () => handleStatusChange(task.id, c.id)
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
        title="Create New Task"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{ priority: 'MEDIUM', status: 'TODO' }}
        >
          <Form.Item
            name="title"
            label="Task Title"
            rules={[{ required: true, message: 'Please enter task title' }]}
          >
            <Input placeholder="e.g. Implement Player Movement" />
          </Form.Item>

          <Row gutter={16}>
             <Col span={12}>
                <Form.Item name="project" label="Project" rules={[{ required: true }]}>
                  <Select placeholder="Select project">
                    {projects?.map((p: any) => (
                      <Option key={p.id} value={p.id}>{p.name}</Option>
                    ))}
                  </Select>
                </Form.Item>
             </Col>
             <Col span={12}>
                <Form.Item name="priority" label="Priority">
                  <Select>
                    <Option value="LOW">Low</Option>
                    <Option value="MEDIUM">Medium</Option>
                    <Option value="HIGH">High</Option>
                    <Option value="URGENT">Urgent</Option>
                  </Select>
                </Form.Item>
             </Col>
          </Row>

          <Form.Item
            name="description"
            label="Description"
          >
            <Input.TextArea rows={4} placeholder="Detailed repro steps or requirements..." />
          </Form.Item>

          <Form.Item className="mb-0 text-right">
            <Space>
              <Button onClick={() => setIsModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit" loading={isCreating}>
                Create Task
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
}
