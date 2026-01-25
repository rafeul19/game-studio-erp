'use client';

import React, { useState, useEffect } from 'react';
import {
  Card,
  List,
  Badge,
  Button,
  Switch,
  Typography,
  Space,
  Tag,
  Avatar,
  Empty,
  Tooltip,
  Divider,
  Row,
  Col,
  Select,
  DatePicker,
  Input,
  Modal,
} from 'antd';
import {
  BellOutlined,
  DeleteOutlined,
  CheckOutlined,
  SettingOutlined,
  UserOutlined,
  ProjectOutlined,
  BugOutlined,
  DollarOutlined,
  TeamOutlined,
  InfoCircleOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import { useAppSelector } from '@/lib/redux/hooks';
import { RootState } from '@/lib/redux/store';
import AppLayout from '@/components/layout/AppLayout';
import { apiClient } from '@/lib/utils/api';

const { Text, Title } = Typography;
const { Option } = Select;
const { Search } = Input;

interface Notification {
  id: string;
  type: string;
  title: string;
  message: string;
  read: boolean;
  created_at: string;
  data: any;
  actor?: {
    username: string;
    full_name?: string;
  };
  target_object?: string;
}

interface NotificationSettings {
  email_notifications: boolean;
  push_notifications: boolean;
  project_updates: boolean;
  task_assignments: boolean;
  bug_reports: boolean;
  finance_alerts: boolean;
  team_updates: boolean;
}

const NotificationsPage: React.FC = () => {
  const { user } = useAppSelector((state: RootState) => state.auth);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [filteredNotifications, setFilteredNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [settings, setSettings] = useState<NotificationSettings>({
    email_notifications: true,
    push_notifications: true,
    project_updates: true,
    task_assignments: true,
    bug_reports: true,
    finance_alerts: false,
    team_updates: false,
  });
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    fetchNotifications();
    setupWebSocket();
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  useEffect(() => {
    filterNotifications();
  }, [notifications, activeTab, searchTerm]);

  const setupWebSocket = () => {
    if (user && user.access_token) {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
      
      const websocket = new WebSocket(wsUrl);
      
      websocket.onopen = () => {
        console.log('WebSocket connected');
        // Send authentication
        websocket.send(JSON.stringify({
          type: 'authenticate',
          token: user.access_token,
        }));
      };
      
      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type !== 'connection_established') {
          setNotifications(prev => [data, ...prev]);
        }
      };
      
      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
      websocket.onclose = () => {
        console.log('WebSocket disconnected');
        // Reconnect after 5 seconds
        setTimeout(setupWebSocket, 5000);
      };
      
      setWs(websocket);
    }
  };

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get('/api/notifications/');
      setNotifications(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterNotifications = () => {
    let filtered = notifications;
    
    // Filter by tab
    if (activeTab === 'unread') {
      filtered = filtered.filter(n => !n.read);
    } else if (activeTab === 'read') {
      filtered = filtered.filter(n => n.read);
    }
    
    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(n =>
        n.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        n.message.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    setFilteredNotifications(filtered);
  };

  const markAsRead = async (notificationId: string) => {
    try {
      await apiClient.patch(`/api/notifications/${notificationId}/`, { read: true });
      setNotifications(prev =>
        prev.map(n => (n.id === notificationId ? { ...n, read: true } : n))
      );
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await apiClient.post('/api/notifications/mark-all-read/');
      setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error);
    }
  };

  const deleteNotification = async (notificationId: string) => {
    try {
      await apiClient.delete(`/api/notifications/${notificationId}/`);
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
    } catch (error) {
      console.error('Failed to delete notification:', error);
    }
  };

  const updateSettings = async (newSettings: NotificationSettings) => {
    try {
      await apiClient.put('/api/notifications/settings/', newSettings);
      setSettings(newSettings);
      setSettingsVisible(false);
    } catch (error) {
      console.error('Failed to update notification settings:', error);
    }
  };

  const getNotificationIcon = (type: string) => {
    const iconMap: { [key: string]: React.ReactNode } = {
      task_assignment: <CheckCircleOutlined style={{ color: '#1890ff' }} />,
      project_update: <ProjectOutlined style={{ color: '#52c41a' }} />,
      bug_report: <BugOutlined style={{ color: '#ff4d4f' }} />,
      finance_alert: <DollarOutlined style={{ color: '#faad14' }} />,
      team_update: <TeamOutlined style={{ color: '#722ed1' }} />,
      system_notification: <InfoCircleOutlined style={{ color: '#13c2c2' }} />,
      warning: <ExclamationCircleOutlined style={{ color: '#faad14' }} />,
    };
    return iconMap[type] || <BellOutlined style={{ color: '#8c8c8c' }} />;
  };

  const getTypeColor = (type: string) => {
    const colorMap: { [key: string]: string } = {
      task_assignment: 'blue',
      project_update: 'green',
      bug_report: 'red',
      finance_alert: 'orange',
      team_update: 'purple',
      system_notification: 'cyan',
      warning: 'gold',
    };
    return colorMap[type] || 'default';
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    return date.toLocaleDateString();
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  const renderNotificationItem = (notification: Notification) => (
    <List.Item
      key={notification.id}
      className={`notification-item ${!notification.read ? 'unread' : 'read'}`}
      style={{
        padding: '16px',
        borderLeft: notification.read ? 'none' : '4px solid #1890ff',
        backgroundColor: notification.read ? '#fafafa' : '#fff',
      }}
      actions={[
        !notification.read && (
          <Tooltip title="Mark as read">
            <Button
              icon={<CheckOutlined />}
              type="text"
              onClick={() => markAsRead(notification.id)}
            />
          </Tooltip>
        ),
        <Tooltip title="Delete">
          <Button
            icon={<DeleteOutlined />}
            type="text"
            danger
            onClick={() => deleteNotification(notification.id)}
          />
        </Tooltip>,
      ]}
    >
      <List.Item.Meta
        avatar={
          <Avatar
            icon={getNotificationIcon(notification.type)}
            style={{
              backgroundColor: notification.read ? '#f0f0f0' : '#1890ff',
            }}
          />
        }
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Text strong={!notification.read}>{notification.title}</Text>
            <Tag color={getTypeColor(notification.type)}>
              {notification.type.replace('_', ' ')}
            </Tag>
          </div>
        }
        description={
          <div>
            <Text type="secondary">{notification.message}</Text>
            <br />
            <Text type="secondary" style={{ fontSize: '12px' }}>
              <ClockCircleOutlined /> {formatTimeAgo(notification.created_at)}
              {notification.actor && (
                <span>
                  {' '}by {notification.actor.full_name || notification.actor.username}
                </span>
              )}
            </Text>
          </div>
        }
      />
    </List.Item>
  );

  return (
    <AppLayout>
      <div style={{ padding: '24px' }}>
        <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Title level={2} style={{ margin: 0 }}>
              Notifications
            </Title>
            {unreadCount > 0 && (
              <Badge count={unreadCount} size="small">
                <BellOutlined style={{ fontSize: '20px' }} />
              </Badge>
            )}
          </div>
          <Space>
            <Button
              icon={<SettingOutlined />}
              onClick={() => setSettingsVisible(true)}
            >
              Settings
            </Button>
            {unreadCount > 0 && (
              <Button onClick={markAllAsRead}>
                Mark All as Read
              </Button>
            )}
          </Space>
        </div>

        <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
          <Col xs={24} md={12}>
            <Card size="small">
              <Space>
                <Text strong>Filter:</Text>
                <Select
                  value={activeTab}
                  onChange={setActiveTab}
                  style={{ width: 120 }}
                >
                  <Option value="all">
                    All ({notifications.length})
                  </Option>
                  <Option value="unread">
                    Unread ({unreadCount})
                  </Option>
                  <Option value="read">
                    Read ({notifications.length - unreadCount})
                  </Option>
                </Select>
              </Space>
            </Card>
          </Col>
          <Col xs={24} md={12}>
            <Card size="small">
              <Search
                placeholder="Search notifications..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ width: '100%' }}
                allowClear
              />
            </Card>
          </Col>
        </Row>

        <Card
          loading={loading}
          bodyStyle={{ padding: 0 }}
        >
          {filteredNotifications.length > 0 ? (
            <List
              dataSource={filteredNotifications}
              renderItem={renderNotificationItem}
              pagination={{
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) =>
                  `${range[0]}-${range[1]} of ${total} notifications`,
              }}
            />
          ) : (
            <Empty
              image={Empty.PRESENTED_IMAGE_SIMPLE}
              description={
                activeTab === 'unread'
                  ? 'No unread notifications'
                  : searchTerm
                  ? 'No notifications found'
                  : 'No notifications'
              }
            />
          )}
        </Card>

        <Modal
          title="Notification Settings"
          open={settingsVisible}
          onCancel={() => setSettingsVisible(false)}
          onOk={() => updateSettings(settings)}
          width={500}
        >
          <Space direction="vertical" style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Email Notifications</Text>
              <Switch
                checked={settings.email_notifications}
                onChange={(checked) =>
                  setSettings({ ...settings, email_notifications: checked })
                }
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Push Notifications</Text>
              <Switch
                checked={settings.push_notifications}
                onChange={(checked) =>
                  setSettings({ ...settings, push_notifications: checked })
                }
              />
            </div>
            <Divider />
            <Text strong>Notification Types</Text>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Project Updates</Text>
              <Switch
                checked={settings.project_updates}
                onChange={(checked) =>
                  setSettings({ ...settings, project_updates: checked })
                }
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Task Assignments</Text>
              <Switch
                checked={settings.task_assignments}
                onChange={(checked) =>
                  setSettings({ ...settings, task_assignments: checked })
                }
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Bug Reports</Text>
              <Switch
                checked={settings.bug_reports}
                onChange={(checked) =>
                  setSettings({ ...settings, bug_reports: checked })
                }
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Finance Alerts</Text>
              <Switch
                checked={settings.finance_alerts}
                onChange={(checked) =>
                  setSettings({ ...settings, finance_alerts: checked })
                }
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>Team Updates</Text>
              <Switch
                checked={settings.team_updates}
                onChange={(checked) =>
                  setSettings({ ...settings, team_updates: checked })
                }
              />
            </div>
          </Space>
        </Modal>
      </div>
    </AppLayout>
  );
};

export default NotificationsPage;