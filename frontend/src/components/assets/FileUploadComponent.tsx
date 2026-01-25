'use client';

import React, { useState } from 'react';
import { Upload, Button, message, Progress, Typography, Space, Image, Tag } from 'antd';
import { UploadOutlined, FileImageOutlined, CustomerServiceOutlined, VideoCameraOutlined, FileTextOutlined } from '@ant-design/icons';
import type { UploadProps, UploadFile } from 'antd/es/upload/interface';

const { Text } = Typography;

interface FileUploadComponentProps {
  onUploadComplete: (fileData: any) => void;
  maxFileSize?: number; // in MB
  acceptedFileTypes?: string[];
  disabled?: boolean;
}

export const FileUploadComponent: React.FC<FileUploadComponentProps> = ({
  onUploadComplete,
  maxFileSize = 100,
  acceptedFileTypes = [
    'image/*',
    'video/*',
    'audio/*',
    'application/zip',
    'application/x-zip-compressed',
    'model/*',
    '.fbx',
    '.obj',
    '.blend',
    '.ma',
    '.mb',
    '.max',
    '.c4d',
    '.dae',
    '.3ds',
    '.gltf',
    '.glb'
  ],
  disabled = false,
}) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileInfo, setFileInfo] = useState<UploadFile | null>(null);

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(extension || '')) {
      return <FileImageOutlined className="text-blue-500" />;
    } else if (['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'].includes(extension || '')) {
      return <VideoCameraOutlined className="text-purple-500" />;
    } else if (['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'].includes(extension || '')) {
      return <CustomerServiceOutlined className="text-green-500" />;
    } else {
      return <FileTextOutlined className="text-gray-500" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const isImageFile = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(extension || '');
  };

  const getPreviewImage = (file: File) => {
    return new Promise<string>((resolve) => {
      if (isImageFile(file.name)) {
        const reader = new FileReader();
        reader.onload = (e) => {
          resolve(e.target?.result as string);
        };
        reader.readAsDataURL(file);
      } else {
        resolve('');
      }
    });
  };

  const customRequest = async (options: any) => {
    const { file, onProgress, onSuccess, onError } = options;
    
    setUploading(true);
    setUploadProgress(0);

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', file);
      formData.append('note', `Uploaded file: ${file.name}`);

      // Simulate upload progress (in real implementation, this would be from the actual upload)
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Get auth token
      const token = localStorage.getItem('access');
      
      // Upload file (this would be your actual API call)
      const response = await fetch('/api/assets/upload/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();
      onSuccess(result);
      onUploadComplete(result);
      message.success('File uploaded successfully!');
      
    } catch (error) {
      console.error('Upload error:', error);
      onError(error);
      message.error('File upload failed. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const beforeUpload = (file: File) => {
    // Check file size
    const isSizeValid = file.size / 1024 / 1024 < maxFileSize;
    if (!isSizeValid) {
      message.error(`File size must be smaller than ${maxFileSize}MB!`);
      return false;
    }

    // Set file info and preview
    setFileInfo(file);
    getPreviewImage(file).then((preview) => {
      setPreviewUrl(preview);
    });

    return true;
  };

  const handleChange: UploadProps['onChange'] = ({ file }) => {
    if (file.status === 'done') {
      setFileInfo(file);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    customRequest,
    beforeUpload,
    onChange: handleChange,
    showUploadList: false,
    disabled: disabled || uploading,
    accept: acceptedFileTypes.join(','),
  };

  return (
    <div className="space-y-4">
      <Upload.Dragger {...uploadProps} className="border-dashed border-2 border-gray-300 hover:border-blue-400 transition-colors">
        <p className="ant-upload-drag-icon">
          <UploadOutlined className="text-4xl text-gray-400" />
        </p>
        <p className="ant-upload-text">
          Click or drag file to this area to upload
        </p>
        <p className="ant-upload-hint text-xs text-gray-500">
          Support for: Images, Videos, Audio, 3D Models (FBX, OBJ, Blend), ZIP files
          <br />
          Maximum file size: {maxFileSize}MB
        </p>
      </Upload.Dragger>

      {uploading && (
        <div className="text-center">
          <Progress percent={uploadProgress} status="active" />
          <Text type="secondary" className="text-sm">Uploading file...</Text>
        </div>
      )}

      {fileInfo && (
        <div className="border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              {previewUrl ? (
                <Image
                  src={previewUrl}
                  alt={fileInfo.name}
                  width={60}
                  height={60}
                  className="rounded object-cover"
                  preview={false}
                />
              ) : (
                <div className="w-14 h-14 bg-gray-200 dark:bg-gray-700 rounded flex items-center justify-center">
                  {getFileIcon(fileInfo.name)}
                </div>
              )}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <Text strong className="truncate">{fileInfo.name}</Text>
                <Tag color={fileInfo.status === 'done' ? 'green' : 'blue'}>
                  {fileInfo.status === 'done' ? 'Uploaded' : 'Processing'}
                </Tag>
              </div>
              
              <Space className="mt-1" size="small">
                <Text type="secondary" className="text-xs">
                  {formatFileSize(fileInfo.size || 0)}
                </Text>
                {fileInfo.type && (
                  <Text type="secondary" className="text-xs">
                    • {fileInfo.type}
                  </Text>
                )}
              </Space>
              
              {fileInfo.status === 'error' && (
                <Text type="danger" className="text-xs mt-1 block">
                  Upload failed. Please try again.
                </Text>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};