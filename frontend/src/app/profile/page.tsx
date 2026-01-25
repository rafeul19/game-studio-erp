'use client';

import React, { useState, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Form,
  Input,
  Button,
  Upload,
  Avatar,
  Typography,
  Divider,
  Tabs,
  List,
  Tag,
  Space,
  Tooltip,
  Progress,
  Statistic,
  Alert,
  Modal,
  message,
} from 'antd';
import {
  UserOutlined,
  MailOutlined,
  PhoneOutlined,
  CalendarOutlined,
  TeamOutlined,
  TrophyOutlined,
  BookOutlined,
  EditOutlined,
  UploadOutlined,
  LockOutlined,
  SafetyOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import { useAppSelector } from '@/lib/redux/hooks';
import { RootState } from '@/lib/redux/store';
import AppLayout from '@/components/layout/AppLayout';
import { apiClient } from '@/lib/utils/api';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;
const { TextArea } = Input;

interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  bio: string;
  phone: string;
  avatar: string;
  date_joined: string;
  last_login: string;
  employee_profile: {
    employee_id: string;
    department: string;
    position: string;
    hire_date: string;
    salary: number;
    years_of_service: number;
    employment_status: string;
  };
  stats: {
    tasks_completed: number;
    projects_count: number;
    hours_logged: number;
    efficiency_score: number;
  };
  skills: any[];
  recent_activities: any[];
  achievements: any[];
}

const ProfilePage: React.FC = () => {
  const { user } = useAppSelector((state: RootState) => state.auth);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [passwordModalVisible, setPasswordModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get('/api/profile/');
      setProfile(response.data);
      form.setFieldsValue(response.data);
    } catch (error) {
      message.error('Failed to fetch profile');
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (values: any) => {
    try {
      await apiClient.put('/api/profile/', values);
      setProfile(prev => ({ ...prev!, ...values }));
      setEditMode(false);
      message.success('Profile updated successfully');
    } catch (error) {
      message.error('Failed to update profile');
    }
  };

  const handlePasswordChange = async (values: any) => {
    try {
      await apiClient.post('/api/change-password/', values);
      setPasswordModalVisible(false);
      passwordForm.resetFields();
      message.success('Password changed successfully');
    } catch (error) {
      message.error('Failed to change password');
    }
  };

  const handleAvatarUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('avatar', file);

    try {
      await apiClient.post('/api/profile/upload-avatar/', formData);
      message.success('Avatar updated successfully');
      fetchProfile();
    } catch (error) {
      message.error('Failed to upload avatar');
    }
  };

  const getRoleColor = (role: string) => {
    const roleColors: { [key: string]: string } = {
      ADMIN: 'red',
      MANAGER: 'blue',
      DEVELOPER: 'green',
      DESIGNER: 'purple',
      QA: 'orange',
    };
    return roleColors[role] || 'default';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  if (!profile) {
    return (
    <AppLayout>
        <div style={{ padding: '24px' }}>
          <Card loading={true} />
        </div>
    </AppLayout>
    );
  }

  return (
    <DashboardLayout>
      <div style={{ padding: '24px' }}>
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={8}>
            <Card loading={loading}>
              <div style={{ textAlign: 'center' }}>
                <Avatar
                  size={120}
                  src={profile.avatar}
                  icon={<UserOutlined />}
                  style={{ marginBottom: '16px' }}
                />
                <Title level={3}>{profile.first_name} {profile.last_name}</Title>
                <Tag color={getRoleColor(profile.role)} style={{ marginBottom: '8px' }}>
                  {profile.role}
                </Tag>
                <Paragraph type="secondary">@{profile.username}</Paragraph>
                
                <Space direction="vertical" style={{ width: '100%', marginTop: '16px' }}>
                  <Upload
                    accept="image/*"
                    showUploadList={false}
                    beforeUpload={(file) => {
                      handleAvatarUpload(file);
                      return false;
                    }}
                  >
                    <Button icon={<UploadOutlined />} block>
                      Change Avatar
                    </Button>
                  </Upload>
                  <Button
                    icon={<LockOutlined />}
                    block
                    onClick={() => setPasswordModalVisible(true)}
                  >
                    Change Password
                  </Button>
                </Space>
              </div>
            </Card>

            <Card title="Quick Stats" style={{ marginTop: '16px' }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <Statistic
                  title="Tasks Completed"
                  value={profile.stats.tasks_completed}
                  prefix={<TrophyOutlined />}
                />
                <Statistic
                  title="Projects"
                  value={profile.stats.projects_count}
                  prefix={<TeamOutlined />}
                />
                <Statistic
                  title="Hours Logged"
                  value={profile.stats.hours_logged}
                  suffix="hrs"
                />
                <div>
                  <Text strong>Efficiency Score</Text>
                  <Progress
                    percent={profile.stats.efficiency_score}
                    size="small"
                    status={profile.stats.efficiency_score >= 80 ? 'success' : 'active'}
                  />
                </div>
              </Space>
            </Card>
          </Col>

          <Col xs={24} lg={16}>
            <Tabs defaultActiveKey="profile">
              <TabPane tab="Profile Information" key="profile">
                <Card
                  title="Personal Information"
                  extra={
                    <Button
                      icon={<EditOutlined />}
                      onClick={() => setEditMode(!editMode)}
                    >
                      {editMode ? 'Cancel' : 'Edit'}
                    </Button>
                  }
                >
                  {editMode ? (
                    <Form
                      form={form}
                      layout="vertical"
                      onFinish={handleProfileUpdate}
                    >
                      <Row gutter={16}>
                        <Col xs={24} md={12}>
                          <Form.Item
                            label="First Name"
                            name="first_name"
                            rules={[{ required: true, message: 'Please input your first name!' }]}
                          >
                            <Input />
                          </Form.Item>
                        </Col>
                        <Col xs={24} md={12}>
                          <Form.Item
                            label="Last Name"
                            name="last_name"
                            rules={[{ required: true, message: 'Please input your last name!' }]}
                          >
                            <Input />
                          </Form.Item>
                        </Col>
                      </Row>
                      
                      <Form.Item
                        label="Email"
                        name="email"
                        rules={[
                          { required: true, message: 'Please input your email!' },
                          { type: 'email', message: 'Please enter a valid email!' }
                        ]}
                      >
                        <Input prefix={<MailOutlined />} />
                      </Form.Item>
                      
                      <Form.Item
                        label="Phone"
                        name="phone"
                      >
                        <Input prefix={<PhoneOutlined />} />
                      </Form.Item>
                      
                      <Form.Item
                        label="Bio"
                        name="bio"
                      >
                        <TextArea rows={4} />
                      </Form.Item>
                      
                      <Form.Item>
                        <Button type="primary" htmlType="submit">
                          Save Changes
                        </Button>
                      </Form.Item>
                    </Form>
                  ) : (
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <div>
                        <Text strong>Full Name:</Text>
                        <Paragraph>{profile.first_name} {profile.last_name}</Paragraph>
                      </div>
                      <div>
                        <Text strong>Email:</Text>
                        <Paragraph>{profile.email}</Paragraph>
                      </div>
                      <div>
                        <Text strong>Phone:</Text>
                        <Paragraph>{profile.phone || 'Not provided'}</Paragraph>
                      </div>
                      <div>
                        <Text strong>Bio:</Text>
                        <Paragraph>{profile.bio || 'No bio provided'}</Paragraph>
                      </div>
                    </Space>
                  )}
                </Card>

                {profile.employee_profile && (
                  <Card title="Employee Information" style={{ marginTop: '16px' }}>
                    <Row gutter={16}>
                      <Col xs={24} md={12}>
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <div>
                            <Text strong>Employee ID:</Text>
                            <Paragraph>{profile.employee_profile.employee_id}</Paragraph>
                          </div>
                          <div>
                            <Text strong>Department:</Text>
                            <Paragraph>{profile.employee_profile.department}</Paragraph>
                          </div>
                          <div>
                            <Text strong>Position:</Text>
                            <Paragraph>{profile.employee_profile.position}</Paragraph>
                          </div>
                        </Space>
                      </Col>
                      <Col xs={24} md={12}>
                        <Space direction="vertical" style={{ width: '100%' }}>
                          <div>
                            <Text strong>Hire Date:</Text>
                            <Paragraph>{formatDate(profile.employee_profile.hire_date)}</Paragraph>
                          </div>
                          <div>
                            <Text strong>Years of Service:</Text>
                            <Paragraph>{profile.employee_profile.years_of_service.toFixed(1)} years</Paragraph>
                          </div>
                          <div>
                            <Text strong>Employment Status:</Text>
                            <Tag color="green">{profile.employee_profile.employment_status}</Tag>
                          </div>
                        </Space>
                      </Col>
                    </Row>
                  </Card>
                )}
              </TabPane>

              <TabPane tab={<span><BookOutlined />Skills</span>} key="skills">
                <Card title="Technical Skills">
                  <List
                    dataSource={profile.skills}
                    renderItem={(skill: any) => (
                      <List.Item>
                        <List.Item.Meta
                          title={skill.skill_name}
                          description={`${skill.skill_category} • ${skill.years_experience} years experience`}
                        />
                        <div style={{ textAlign: 'right' }}>
                          <Tag color={skill.proficiency >= 4 ? 'green' : skill.proficiency >= 3 ? 'blue' : 'orange'}>
                            {skill.proficiency_display}
                          </Tag>
                          <div style={{ marginTop: '4px' }}>
                            <Progress
                              percent={(skill.proficiency / 5) * 100}
                              size="small"
                              showInfo={false}
                            />
                          </div>
                        </div>
                      </List.Item>
                    )}
                  />
                </Card>
              </TabPane>

              <TabPane tab={<span><FileTextOutlined />Activity</span>} key="activity">
                <Card title="Recent Activity">
                  <List
                    dataSource={profile.recent_activities}
                    renderItem={(activity: any) => (
                      <List.Item>
                        <List.Item.Meta
                          avatar={<Avatar icon={<UserOutlined />} />}
                          title={activity.title}
                          description={
                            <div>
                              <Paragraph>{activity.description}</Paragraph>
                              <Text type="secondary" style={{ fontSize: '12px' }}>
                                {formatDate(activity.created_at)}
                              </Text>
                            </div>
                          }
                        />
                        <Tag color={activity.type === 'task' ? 'blue' : activity.type === 'project' ? 'green' : 'orange'}>
                          {activity.type}
                        </Tag>
                      </List.Item>
                    )}
                  />
                </Card>
              </TabPane>

              <TabPane tab={<span><TrophyOutlined />Achievements</span>} key="achievements">
                <Card title="Achievements & Awards">
                  <List
                    dataSource={profile.achievements}
                    renderItem={(achievement: any) => (
                      <List.Item>
                        <List.Item.Meta
                          avatar={<Avatar icon={<TrophyOutlined />} />}
                          title={achievement.title}
                          description={
                            <div>
                              <Paragraph>{achievement.description}</Paragraph>
                              <Text type="secondary">
                                Earned on {formatDate(achievement.earned_date)}
                              </Text>
                            </div>
                          }
                        />
                        <Tag color="gold">{achievement.category}</Tag>
                      </List.Item>
                    )}
                  />
                </Card>
              </TabPane>
            </Tabs>
          </Col>
        </Row>

        <Modal
          title="Change Password"
          open={passwordModalVisible}
          onCancel={() => setPasswordModalVisible(false)}
          footer={null}
        >
          <Form
            form={passwordForm}
            layout="vertical"
            onFinish={handlePasswordChange}
          >
            <Form.Item
              label="Current Password"
              name="current_password"
              rules={[{ required: true, message: 'Please input your current password!' }]}
            >
              <Input.Password prefix={<LockOutlined />} />
            </Form.Item>
            
            <Form.Item
              label="New Password"
              name="new_password"
              rules={[
                { required: true, message: 'Please input your new password!' },
                { min: 8, message: 'Password must be at least 8 characters long!' }
              ]}
            >
              <Input.Password prefix={<SafetyOutlined />} />
            </Form.Item>
            
            <Form.Item
              label="Confirm New Password"
              name="confirm_password"
              dependencies={['new_password']}
              rules={[
                { required: true, message: 'Please confirm your new password!' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('new_password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('The two passwords do not match!'));
                  },
                }),
              ]}
            >
              <Input.Password prefix={<SafetyOutlined />} />
            </Form.Item>
            
            <Form.Item>
              <Button type="primary" htmlType="submit" block>
                Change Password
              </Button>
            </Form.Item>
          </Form>
        </Modal>
      </div>
    </DashboardLayout>
  );
};

export default ProfilePage;