'use client';

import React from 'react';
import {
  Typography,
  Card,
  Row,
  Col,
  Tabs,
  Form,
  Input,
  Button,
  Switch,
  Divider,
  App,
  Avatar,
  Space,
  Tag,
} from 'antd';
import {
  UserOutlined,
  BellOutlined,
  SettingOutlined,
  GlobalOutlined,
  LockOutlined,
  RocketOutlined,
} from '@ant-design/icons';
import AppLayout from '@/components/layout/AppLayout';
import { useAppSelector } from '@/store/hooks';

const { Title, Text } = Typography;

const AppearanceSettings = ({ onSave }: { onSave: () => void }) => (
  <div className="max-w-xl">
    <Space direction="vertical" size="large" className="w-full">
      <div>
        <Text strong>Theme Customization</Text>
        <div className="mt-4 flex justify-between items-center bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg">
          <Space direction="vertical" size={0}>
            <Text>Dark Mode</Text>
            <Text type="secondary" className="text-xs">Optimized for game studio lighting environments</Text>
          </Space>
          <Switch defaultChecked disabled />
        </div>
      </div>
      <div>
        <Text strong>Interface</Text>
        <div className="mt-4 flex justify-between items-center bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg">
          <Space direction="vertical" size={0}>
            <Text>Compact Sidebar</Text>
            <Text type="secondary" className="text-xs">Maximize screen space for project boards</Text>
          </Space>
          <Switch />
        </div>
      </div>
      <Button type="primary" onClick={onSave}>Save Changes</Button>
    </Space>
  </div>
);

const NotificationSettings = ({ onSave }: { onSave: () => void }) => (
  <div className="max-w-xl">
    <Space direction="vertical" size="large" className="w-full">
      <div>
        <Text strong>Studio Alerts</Text>
        <div className="mt-4 space-y-2">
          {[
            { label: 'Asset Reuse Warnings', desc: 'Notify when duplicate assets are detected' },
            { label: 'Sprint Risk Alerts', desc: 'AI-driven notifications for delayed sprints' },
            { label: 'Task Assignments', desc: 'Real-time alert when a task is moved to your column' },
          ].map((item, i) => (
            <div key={i} className="flex justify-between items-center bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg">
              <Space direction="vertical" size={0}>
                <Text>{item.label}</Text>
                <Text type="secondary" className="text-xs">{item.desc}</Text>
              </Space>
              <Switch defaultChecked />
            </div>
          ))}
        </div>
      </div>
      <Button type="primary" onClick={onSave}>Update Preferences</Button>
    </Space>
  </div>
);

const ProfileSettings = ({ user, onSave }: { user: any, onSave: () => void }) => (
  <Form layout="vertical" className="max-w-xl">
    <Row gutter={24} className="mb-8">
      <Col>
         <Avatar size={100} icon={<UserOutlined />} src={user?.avatar} className="border-4 border-blue-500/20 shadow-xl" />
      </Col>
      <Col className="flex flex-col justify-center">
         <Title level={3} className="m-0">{user?.username || 'Studio User'}</Title>
         <Space>
            <Tag color="blue">{user?.role?.toUpperCase() || 'DEVELOPER'}</Tag>
            <Text type="secondary">Member since Jan 2026</Text>
         </Space>
         <Button size="small" className="mt-2 text-xs w-fit">Change Avatar</Button>
      </Col>
    </Row>
    
    <Divider />

    <Row gutter={16}>
      <Col span={12}>
        <Form.Item label="Display Name">
          <Input defaultValue={user?.username} />
        </Form.Item>
      </Col>
      <Col span={12}>
        <Form.Item label="Email Address">
          <Input placeholder="yourname@studio.com" />
        </Form.Item>
      </Col>
    </Row>
    
    <Form.Item label="Bio / Skills">
      <Input.TextArea rows={4} placeholder="e.g. Senior Technical Artist | Unreal Engine 5 Specialist" />
    </Form.Item>

    <Button type="primary" onClick={onSave}>Update Profile</Button>
  </Form>
);

export default function SettingsPage() {
  const { user } = useAppSelector((state) => state.auth);
  const { message } = App.useApp();

  const handleSave = () => {
    message.success('Settings updated successfully');
  };

  const tabItems = [
    {
      key: 'profile',
      label: (
        <span>
          <UserOutlined />
          Profile
        </span>
      ),
      children: <ProfileSettings user={user} onSave={handleSave} />,
    },
    {
      key: 'appearance',
      label: (
        <span>
          <RocketOutlined />
          Appearance
        </span>
      ),
      children: <AppearanceSettings onSave={handleSave} />,
    },
    {
      key: 'notifications',
      label: (
        <span>
          <BellOutlined />
          Notifications
        </span>
      ),
      children: <NotificationSettings onSave={handleSave} />,
    },
    {
      key: 'security',
      label: (
        <span>
          <LockOutlined />
          Security
        </span>
      ),
      children: (
        <div className="max-w-xl py-4">
           <Text type="secondary">Manage your password and API access keys here.</Text>
           <Divider />
           <Button>Reset Password</Button>
        </div>
      ),
    },
  ];

  return (
    <AppLayout>
      <div className="mb-8">
        <Title level={2} className="flex items-center gap-2">
          <SettingOutlined className="text-gray-400" />
          Studio Settings
        </Title>
        <Text type="secondary">Configure your workspace preferences and personal profile</Text>
      </div>

      <Card variant="borderless" className="shadow-lg rounded-2xl overflow-hidden min-h-[600px]">
        <Tabs
          defaultActiveKey="profile"
          items={tabItems}
          tabPosition="left"
          size="large"
          className="settings-tabs"
        />
      </Card>

      <style jsx global>{`
        .settings-tabs .ant-tabs-nav {
          min-width: 200px;
          border-right: 1px solid rgba(255, 255, 255, 0.05);
          padding-right: 12px;
        }
        .settings-tabs .ant-tabs-tab {
          border-radius: 8px !important;
          margin-bottom: 8px !important;
          padding: 12px 16px !important;
        }
        .settings-tabs .ant-tabs-tab-active {
          background: rgba(24, 144, 255, 0.1) !important;
        }
      `}</style>
    </AppLayout>
  );
}
