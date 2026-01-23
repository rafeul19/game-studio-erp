'use client';

import React from 'react';
import { Tag, Skeleton } from 'antd';
import { RobotOutlined } from '@ant-design/icons';
import { usePredictSprintRiskQuery } from '@/store/api/projectApi';

interface RiskBadgeProps {
  sprintId: number;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ sprintId }) => {
  const { data, isLoading } = usePredictSprintRiskQuery(sprintId);

  if (isLoading) return <Skeleton.Button active size="small" style={{ width: 80 }} />;

  const riskLevel = data?.risk_level || 'UNKNOWN';
  let color = 'default';
  
  if (riskLevel.includes('HIGH')) color = 'error';
  else if (riskLevel.includes('MEDIUM')) color = 'warning';
  else if (riskLevel.includes('LOW')) color = 'success';

  return (
    <Tag icon={<RobotOutlined />} color={color}>
      {riskLevel}
    </Tag>
  );
};
