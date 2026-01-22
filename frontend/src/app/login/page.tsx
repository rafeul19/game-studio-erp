'use client';

import React from 'react';
import { Form, Input, Button, Card, Typography, Checkbox, message } from 'antd';
import { UserOutlined, LockOutlined, DeploymentUnitOutlined } from '@ant-design/icons';
import { useRouter } from 'next/navigation';
import { useLoginMutation } from '@/store/api/authApi';
import { useAppDispatch } from '@/store/hooks';
import { setCredentials } from '@/store/slices/authSlice';

const { Title, Text } = Typography;

export default function LoginPage() {
  const [login, { isLoading }] = useLoginMutation();
  const dispatch = useAppDispatch();
  const router = useRouter();

  const onFinish = async (values: Record<string, any>) => {
    try {
      const result = await login({
        username: values.username,
        password: values.password,
      }).unwrap();
      
      dispatch(setCredentials({
        user: { username: values.username }, // Simplified user for now
        access: result.access,
        refresh: result.refresh,
      }));
      
      message.success('Welcome back!');
      router.push('/dashboard');
    } catch (error: any) {
      const errorMsg = error.data?.detail || 'Invalid username or password';
      message.error(errorMsg);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]">
      <div className="w-full max-w-md p-4">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-4 shadow-xl shadow-blue-500/20">
            <DeploymentUnitOutlined style={{ fontSize: '2rem', color: 'white' }} />
          </div>
          <Title level={2} style={{ color: 'white', margin: 0 }}>Game Studio ERP</Title>
          <Text style={{ color: '#94a3b8' }}>Enterprise-grade studio management</Text>
        </div>

        <Card variant="borderless" className="shadow-2xl rounded-2xl bg-white/10 backdrop-blur-md border border-white/10">
          <Form
            name="login"
            layout="vertical"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            size="large"
          >
            <Form.Item
              name="username"
              rules={[{ required: true, message: 'Please input your Username!' }]}
            >
              <Input 
                prefix={<UserOutlined className="text-gray-400" />} 
                placeholder="Username" 
                className="bg-white/5 border-white/10 text-white placeholder:text-gray-500 hover:border-blue-500 focus:border-blue-500"
              />
            </Form.Item>
            <Form.Item
              name="password"
              rules={[{ required: true, message: 'Please input your Password!' }]}
            >
              <Input.Password
                prefix={<LockOutlined className="text-gray-400" />}
                placeholder="Password"
                className="bg-white/5 border-white/10 text-white placeholder:text-gray-500 hover:border-blue-500 focus:border-blue-500"
              />
            </Form.Item>

            <Form.Item>
              <div className="flex justify-between items-center text-sm">
                <Form.Item name="remember" valuePropName="checked" noStyle>
                  <Checkbox className="text-gray-400">Remember me</Checkbox>
                </Form.Item>
                <a className="text-blue-400 hover:text-blue-300 transition-colors" href="">
                  Forgot password?
                </a>
              </div>
            </Form.Item>

            <Form.Item className="mb-0">
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={isLoading} 
                block 
                className="h-12 bg-blue-600 hover:bg-blue-500 border-none font-bold text-lg shadow-lg shadow-blue-500/20"
              >
                Log in
              </Button>
            </Form.Item>
          </Form>
        </Card>
        
        <div className="text-center mt-6">
          <Text style={{ color: '#94a3b8' }}>
            New to the studio? <a href="#" className="text-blue-400 hover:text-blue-300">Contact HR for an account</a>
          </Text>
        </div>
      </div>
    </div>
  );
}
