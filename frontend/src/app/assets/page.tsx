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
  Input,
  Select,
  Modal,
  Form,
  message,
  Empty,
  Badge,
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  FilterOutlined,
  FileImageOutlined,
  CustomerServiceOutlined,
  VideoCameraOutlined,
  FileTextOutlined,
  DownloadOutlined,
  HistoryOutlined,
} from '@ant-design/icons';
import { AppLayout } from '@/components/layout/AppLayout';
import { useGetAssetsQuery, useCreateAssetMutation } from '@/store/api/assetApi';
import { useGetProjectsQuery } from '@/store/api/projectApi';

const { Title, Text } = Typography;
const { Option } = Select;

export default function AssetsPage() {
  const { data: projects } = useGetProjectsQuery({});
  const { data: assets, isLoading } = useGetAssetsQuery({});
  const [createAsset, { isLoading: isCreating }] = useCreateAssetMutation();
  
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [filterType, setFilterType] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [form] = Form.useForm();

  const handleCreate = async (values: any) => {
    try {
      await createAsset(values).unwrap();
      message.success('Asset created successfully');
      setIsModalVisible(false);
      form.resetFields();
    } catch {
      message.error('Failed to create asset');
    }
  };

  const getAssetIcon = (type: string) => {
    switch (type) {
      case '3D': return <VideoCameraOutlined className="text-purple-500 text-2xl" />;
      case '2D': return <FileImageOutlined className="text-blue-500 text-2xl" />;
      case 'AUDIO': return <CustomerServiceOutlined className="text-green-500 text-2xl" />;
      default: return <FileTextOutlined className="text-gray-500 text-2xl" />;
    }
  };

  const filteredAssets = assets?.filter((asset: any) => {
    const matchesPath = asset.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                      asset.tags.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = filterType ? asset.asset_type === filterType : true;
    return matchesPath && matchesType;
  });

  return (
    <AppLayout>
      <div className="flex justify-between items-center mb-6">
        <div>
          <Title level={2}>Digital Assets</Title>
          <Text type="secondary">Centralized library for project components, textures, and media</Text>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          size="large"
          onClick={() => setIsModalVisible(true)}
          className="bg-blue-600"
        >
          New Asset
        </Button>
      </div>

      <Card variant="borderless" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col xs={24} sm={12} lg={16}>
            <Input
              prefix={<SearchOutlined className="text-gray-400" />}
              placeholder="Search assets by name or tags..."
              size="large"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </Col>
          <Col xs={24} sm={12} lg={8}>
            <Select
              placeholder="Filter by Type"
              className="w-full"
              size="large"
              allowClear
              onChange={(value) => setFilterType(value)}
              prefix={<FilterOutlined />}
            >
              <Option value="3D">3D Models</Option>
              <Option value="2D">2D Art</Option>
              <Option value="AUDIO">Audio/SFX</Option>
              <Option value="VFX">Visual Effects</Option>
              <Option value="OTHER">Other</Option>
            </Select>
          </Col>
        </Row>
      </Card>

      {isLoading ? (
        <div className="text-center py-20">Loading your studio library...</div>
      ) : filteredAssets?.length === 0 ? (
        <Card variant="borderless" className="py-20 shadow-sm text-center">
          <Empty description="No assets found in the library" />
        </Card>
      ) : (
        <Row gutter={[16, 16]}>
          {filteredAssets?.map((asset: any) => (
            <Col xs={24} sm={12} lg={6} xl={4} key={asset.id}>
              <Card
                hoverable
                className="overflow-hidden rounded-xl border-none shadow-sm hover:shadow-md transition-all"
                cover={
                  <div className="h-40 bg-gray-50 dark:bg-gray-800 flex items-center justify-center border-b border-gray-100 dark:border-gray-700">
                    {getAssetIcon(asset.asset_type)}
                  </div>
                }
                actions={[
                  <DownloadOutlined key="download" />,
                  <HistoryOutlined key="history" />,
                ]}
              >
                <Card.Meta
                  title={
                    <div className="flex justify-between items-start">
                      <span className="truncate">{asset.name}</span>
                      <Badge status={asset.latest_version ? 'success' : 'default'} />
                    </div>
                  }
                  description={
                    <div className="space-y-1 mt-2">
                      <Tag size="small">{asset.asset_type}</Tag>
                      <Text type="secondary" className="block text-xs truncate">
                        {asset.project_name}
                      </Text>
                      {asset.latest_version && (
                        <Text type="success" className="text-[10px] uppercase font-bold">
                          v{asset.latest_version.version_number}
                        </Text>
                      )}
                    </div>
                  }
                />
              </Card>
            </Col>
          ))}
        </Row>
      )}

      <Modal
        title="Register New Asset"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        destroyOnHidden
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreate}
          initialValues={{ asset_type: '3D' }}
        >
          <Form.Item
            name="name"
            label="Asset Name"
            rules={[{ required: true, message: 'Please enter asset name' }]}
          >
            <Input placeholder="e.g. Hero Character Mesh" />
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
                <Form.Item name="asset_type" label="Asset Type">
                  <Select>
                    <Option value="3D">3D Model</Option>
                    <Option value="2D">2D Art</Option>
                    <Option value="AUDIO">Audio/SFX</Option>
                    <Option value="VFX">Visual Effects</Option>
                    <Option value="OTHER">Other</Option>
                  </Select>
                </Form.Item>
             </Col>
          </Row>

          <Form.Item name="tags" label="Tags">
             <Input placeholder="e.g. character, high-poly, forest" />
          </Form.Item>

          <Form.Item name="description" label="Description">
             <Input.TextArea rows={3} placeholder="Functional requirements, usage guidelines..." />
          </Form.Item>

          <Form.Item className="mb-0 text-right">
            <Space>
              <Button onClick={() => setIsModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit" loading={isCreating}>
                Register Asset
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
}
