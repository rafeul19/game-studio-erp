'use client';

import React, { useState, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Statistic,
  Table,
  Button,
  DatePicker,
  Select,
  Tag,
  Modal,
  Form,
  Input,
  InputNumber,
  message,
  Tabs,
  Progress,
  Space,
  Tooltip,
} from 'antd';
import {
  DollarOutlined,
  WalletOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  PlusOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import { useAppSelector } from '@/store/hooks';
import type { RootState } from '@/store/store';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import AppLayout from '@/components/layout/AppLayout';
import { apiClient } from '@/lib/utils/api';

const { RangePicker } = DatePicker;
const { Option } = Select;

interface FinancialSummary {
  total_revenue: number;
  total_expenses: number;
  net_profit: number;
  profit_margin: number;
  total_invoices: number;
  unpaid_invoices: number;
  overdue_invoices: number;
  total_outstanding: number;
  payroll_expense: number;
  operational_expenses: number;
}

interface Invoice {
  id: number;
  invoice_number: string;
  client_name: string;
  amount: number;
  total_amount: number;
  status: string;
  status_display: string;
  issue_date: string;
  due_date: string;
  days_overdue: number;
  is_overdue: boolean;
}

interface Expense {
  id: number;
  category: string;
  category_display: string;
  amount: number;
  date: string;
  description: string;
  vendor: string;
  approved: boolean;
}

interface Budget {
  id: number;
  name: string;
  budget_type_display: string;
  allocated_amount: number;
  spent_amount: number;
  remaining_amount: number;
  utilization_percentage: number;
  is_over_budget: boolean;
  status_color: string;
}

const FinancePage: React.FC = () => {
  const { user } = useAppSelector((state: RootState) => state.auth);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [monthlyTrends, setMonthlyTrends] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dateRange, setDateRange] = useState<any>(null);

  useEffect(() => {
    fetchFinancialData();
  }, [dateRange]);

  const fetchFinancialData = async () => {
    setLoading(true);
    try {
      const params = {};
      if (dateRange) {
        params.start_date = dateRange[0].format('YYYY-MM-DD');
        params.end_date = dateRange[1].format('YYYY-MM-DD');
      }

      const [summaryRes, invoicesRes, expensesRes, budgetsRes, analyticsRes] = await Promise.all([
        apiClient.get('/api/finance/analytics/', { params }),
        apiClient.get('/api/finance/invoices/'),
        apiClient.get('/api/finance/expenses/'),
        apiClient.get('/api/finance/budgets/'),
      ]);

      setSummary(summaryRes.data);
      setInvoices(invoicesRes.data.results || invoicesRes.data);
      setExpenses(expensesRes.data.results || expensesRes.data);
      setBudgets(budgetsRes.data.results || budgetsRes.data);
      
      if (analyticsRes.data.monthly_trends) {
        setMonthlyTrends(analyticsRes.data.monthly_trends);
      }
    } catch (error) {
      message.error('Failed to fetch financial data');
    } finally {
      setLoading(false);
    }
  };

  const invoiceColumns = [
    {
      title: 'Invoice #',
      dataIndex: 'invoice_number',
      key: 'invoice_number',
      render: (text: string, record: Invoice) => `INV-${text}`,
    },
    {
      title: 'Client',
      dataIndex: 'client_name',
      key: 'client_name',
    },
    {
      title: 'Amount',
      dataIndex: 'total_amount',
      key: 'total_amount',
      render: (amount: number) => `$${amount.toLocaleString()}`,
    },
    {
      title: 'Status',
      dataIndex: 'status_display',
      key: 'status',
      render: (status: string, record: Invoice) => {
        let color = 'blue';
        if (record.is_overdue) color = 'red';
        else if (status === 'PAID') color = 'green';
        
        return <Tag color={color}>{status}</Tag>;
      },
    },
    {
      title: 'Due Date',
      dataIndex: 'due_date',
      key: 'due_date',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (text: any, record: Invoice) => (
        <Space>
          <Tooltip title="View Details">
            <Button icon={<EyeOutlined />} size="small" />
          </Tooltip>
          {record.status !== 'PAID' && (
            <Tooltip title="Mark as Paid">
              <Button icon={<DollarOutlined />} size="small" type="primary" />
            </Tooltip>
          )}
        </Space>
      ),
    },
  ];

  const expenseColumns = [
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Category',
      dataIndex: 'category_display',
      key: 'category',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Vendor',
      dataIndex: 'vendor',
      key: 'vendor',
    },
    {
      title: 'Amount',
      dataIndex: 'amount',
      key: 'amount',
      render: (amount: number) => `$${amount.toLocaleString()}`,
    },
    {
      title: 'Status',
      dataIndex: 'approved',
      key: 'approved',
      render: (approved: boolean) => (
        <Tag color={approved ? 'green' : 'orange'}>
          {approved ? 'Approved' : 'Pending'}
        </Tag>
      ),
    },
  ];

  const budgetColumns = [
    {
      title: 'Budget Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Type',
      dataIndex: 'budget_type_display',
      key: 'budget_type',
    },
    {
      title: 'Allocated',
      dataIndex: 'allocated_amount',
      key: 'allocated_amount',
      render: (amount: number) => `$${amount.toLocaleString()}`,
    },
    {
      title: 'Spent',
      dataIndex: 'spent_amount',
      key: 'spent_amount',
      render: (amount: number) => `$${amount.toLocaleString()}`,
    },
    {
      title: 'Remaining',
      dataIndex: 'remaining_amount',
      key: 'remaining_amount',
      render: (amount: number) => `$${amount.toLocaleString()}`,
    },
    {
      title: 'Utilization',
      dataIndex: 'utilization_percentage',
      key: 'utilization',
      render: (percentage: number, record: Budget) => (
        <Progress
          percent={percentage}
          status={record.is_over_budget ? 'exception' : percentage > 80 ? 'active' : 'success'}
          size="small"
        />
      ),
    },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const expenseCategories = expenses.reduce((acc: any, expense: Expense) => {
    const category = expense.category_display;
    if (!acc[category]) {
      acc[category] = 0;
    }
    acc[category] += expense.amount;
    return acc;
  }, {});

  const pieData = Object.entries(expenseCategories).map(([name, value]) => ({
    name,
    value: value as number,
  }));

  return (
    <AppLayout>
      <div style={{ padding: '24px' }}>
        <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>Finance Dashboard</h1>
          <Space>
            <RangePicker onChange={setDateRange} />
            <Button icon={<PlusOutlined />} type="primary">
              Add Transaction
            </Button>
          </Space>
        </div>

        <Tabs 
          activeKey={activeTab} 
          onChange={setActiveTab}
          items={[
            {
              key: 'dashboard',
              label: 'Dashboard',
              children: summary ? (
                <>
                <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                  <Col xs={24} sm={12} md={6}>
                    <Card>
                      <Statistic
                        title="Total Revenue"
                        value={summary.total_revenue}
                        precision={2}
                        styles={{ content: { color: '#3f8600' } }}
                        prefix={<ArrowUpOutlined />}
                        suffix="$"
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={12} md={6}>
                    <Card>
                      <Statistic
                        title="Total Expenses"
                        value={summary.total_expenses}
                        precision={2}
                        styles={{ content: { color: '#cf1322' } }}
                        prefix={<ArrowDownOutlined />}
                        suffix="$"
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={12} md={6}>
                    <Card>
                      <Statistic
                        title="Net Profit"
                        value={summary.net_profit}
                        precision={2}
                        styles={{ content: { color: summary.net_profit >= 0 ? '#3f8600' : '#cf1322' } }}
                        prefix={<WalletOutlined />}
                        suffix="$"
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={12} md={6}>
                    <Card>
                      <Statistic
                        title="Profit Margin"
                        value={summary.profit_margin}
                        precision={2}
                        suffix="%"
                        styles={{ content: { color: summary.profit_margin >= 0 ? '#3f8600' : '#cf1322' } }}
                      />
                    </Card>
                  </Col>
                </Row>

                <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                  <Col xs={24} lg={16}>
                    <Card title="Monthly Trends" loading={loading}>
                      <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={monthlyTrends}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="month" />
                          <YAxis />
                          <RechartsTooltip />
                          <Line type="monotone" dataKey="revenue" stroke="#3f8600" strokeWidth={2} />
                          <Line type="monotone" dataKey="expenses" stroke="#cf1322" strokeWidth={2} />
                          <Line type="monotone" dataKey="profit" stroke="#1890ff" strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    </Card>
                  </Col>
                  <Col xs={24} lg={8}>
                    <Card title="Expense Categories" loading={loading}>
                      <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                          <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {pieData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <RechartsTooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </Card>
                  </Col>
                </Row>

                <Row gutter={[16, 16]}>
                  <Col xs={24} lg={12}>
                    <Card title="Invoice Summary" loading={loading}>
                      <Row gutter={16}>
                        <Col span={8}>
                          <Statistic
                            title="Total Invoices"
                            value={summary.total_invoices}
                            styles={{ content: { color: '#1890ff' } }}
                          />
                        </Col>
                        <Col span={8}>
                          <Statistic
                            title="Unpaid"
                            value={summary.unpaid_invoices}
                            styles={{ content: { color: '#faad14' } }}
                          />
                        </Col>
                        <Col span={8}>
                          <Statistic
                            title="Overdue"
                            value={summary.overdue_invoices}
                            styles={{ content: { color: '#ff4d4f' } }}
                          />
                        </Col>
                      </Row>
                    </Card>
                  </Col>
                  <Col xs={24} lg={12}>
                    <Card title="Outstanding Amount" loading={loading}>
                      <Statistic
                        title="Total Outstanding"
                        value={summary.total_outstanding}
                        precision={2}
                        styles={{ content: { color: '#faad14' } }}
                        prefix={<DollarOutlined />}
                        suffix="$"
                      />
                    </Card>
                  </Col>
                </Row>
              </>
              ),
            },
            {
              key: 'invoices',
              label: 'Invoices',
              children: (
            <Card title="Invoice Management" loading={loading}>
              <Table
                columns={invoiceColumns}
                dataSource={invoices}
                rowKey="id"
                pagination={{
                  showSizeChanger: true,
                  showQuickJumper: true,
                  showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} invoices`,
                }}
              />
            </Card>
              ),
            },
            {
              key: 'expenses',
              label: 'Expenses',
              children: (
            <Card title="Expense Management" loading={loading}>
              <Table
                columns={expenseColumns}
                dataSource={expenses}
                rowKey="id"
                pagination={{
                  showSizeChanger: true,
                  showQuickJumper: true,
                  showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} expenses`,
                }}
              />
            </Card>
              ),
            },
            {
              key: 'budgets',
              label: 'Budgets',
              children: (
                <Card title="Budget Tracking" loading={loading}>
                  <Table
                    columns={budgetColumns}
                    dataSource={budgets}
                    rowKey="id"
                    pagination={{
                      showSizeChanger: true,
                      showQuickJumper: true,
                      showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} budgets`,
                    }}
                  />
                </Card>
              ),
            },
          ]}
        />
      </div>
    </AppLayout>
  );
};

export default FinancePage;