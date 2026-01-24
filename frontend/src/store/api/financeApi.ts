import { baseApi } from './baseApi';

// Finance Types
export interface Payroll {
  id: number;
  employee: number;
  employee_name: string;
  employee_id: string;
  month: string;
  month_display: string;
  base_salary: number;
  bonuses: number;
  deductions: number;
  overtime_hours: number;
  overtime_rate: number;
  net_salary: number;
  paid_date?: string;
  status: string;
  status_display: string;
  payment_method: string;
  payment_method_display: string;
  bank_account: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface Invoice {
  id: number;
  project: number;
  project_name: string;
  invoice_number: string;
  client_name: string;
  client_email: string;
  client_address: string;
  amount: number;
  tax_rate: number;
  tax_amount: number;
  total_amount: number;
  issue_date: string;
  due_date: string;
  paid_date?: string;
  status: string;
  status_display: string;
  payment_terms: string;
  notes: string;
  days_overdue: number;
  is_overdue: boolean;
  amount_paid?: number;
  created_at: string;
  updated_at: string;
}

export interface Expense {
  id: number;
  project: number;
  project_name: string;
  category: string;
  category_display: string;
  amount: number;
  date: string;
  description: string;
  vendor: string;
  receipt?: string;
  receipt_url?: string;
  receipt_number: string;
  tax_deductible: boolean;
  approved: boolean;
  approved_by?: number;
  approved_by_name?: string;
  approval_date?: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface Revenue {
  id: number;
  project: number;
  project_name: string;
  revenue_type: string;
  revenue_type_display: string;
  amount: number;
  date: string;
  client_name: string;
  invoice?: number;
  invoice_number?: string;
  payment_method: string;
  payment_method_display: string;
  transaction_id: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface Budget {
  id: number;
  name: string;
  budget_type: string;
  budget_type_display: string;
  project: number;
  project_name: string;
  department: string;
  allocated_amount: number;
  spent_amount: number;
  remaining_amount: number;
  utilization_percentage: number;
  is_over_budget: boolean;
  status_color: string;
  start_date: string;
  end_date: string;
  currency: string;
  owner?: number;
  owner_name?: string;
  notes: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface FinancialReport {
  id: number;
  report_type: string;
  report_type_display: string;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  generated_date: string;
  generated_by?: number;
  generated_by_name?: string;
  file_path: string;
  file_url?: string;
  data_summary: Record<string, any>;
  is_public: boolean;
  created_at: string;
  updated_at: string;
}

export interface FinanceAnalytics {
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
  monthly_trends: Array<{
    month: string;
    revenue: number;
    expenses: number;
    profit: number;
  }>;
  period: {
    start_date: string;
    end_date: string;
  };
}

export interface ProjectBurnRate {
  project_id: number;
  project_name: string;
  total_budget: number;
  total_spent: number;
  remaining_budget: number;
  burn_rate: number;
  daily_burn_rate: number;
  days_remaining: number;
  projected_end_date: string;
  status: 'ON_TRACK' | 'AT_RISK' | 'OVER_BUDGET';
}

export const financeApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Payroll
    getPayroll: builder.query<Payroll[], Partial<Payroll>>({
      query: (params) => ({
        url: 'payroll/',
        params,
      }),
      providesTags: ['Payroll'],
    }),
    createPayroll: builder.mutation<Payroll, Partial<Payroll>>({
      query: (data) => ({
        url: 'payroll/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Payroll'],
    }),
    approvePayroll: builder.mutation<Payroll, number>({
      query: (id) => ({
        url: `payroll/${id}/approve/`,
        method: 'POST',
      }),
      invalidatesTags: ['Payroll'],
    }),
    markPayrollPaid: builder.mutation<Payroll, { id: number; paid_date: string }>({
      query: ({ id, paid_date }) => ({
        url: `payroll/${id}/mark_paid/`,
        method: 'POST',
        body: { paid_date },
      }),
      invalidatesTags: ['Payroll'],
    }),
    getPayrollSummary: builder.query<any, { start_date: string; end_date: string }>({
      query: ({ start_date, end_date }) => ({
        url: 'payroll/summary/',
        params: { start_date, end_date },
      }),
      providesTags: ['Payroll'],
    }),

    // Invoices
    getInvoices: builder.query<Invoice[], Partial<Invoice>>({
      query: (params) => ({
        url: 'invoices/',
        params,
      }),
      providesTags: ['Invoice'],
    }),
    createInvoice: builder.mutation<Invoice, Partial<Invoice>>({
      query: (data) => ({
        url: 'invoices/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Invoice'],
    }),
    markInvoicePaid: builder.mutation<Invoice, { id: number; paid_date: string }>({
      query: ({ id, paid_date }) => ({
        url: `invoices/${id}/mark_paid/`,
        method: 'POST',
        body: { paid_date },
      }),
      invalidatesTags: ['Invoice'],
    }),
    sendInvoice: builder.mutation<Invoice, number>({
      query: (id) => ({
        url: `invoices/${id}/send/`,
        method: 'POST',
      }),
      invalidatesTags: ['Invoice'],
    }),
    getOverdueInvoices: builder.query<Invoice[], void>({
      query: () => 'invoices/overdue/',
      providesTags: ['Invoice'],
    }),

    // Expenses
    getExpenses: builder.query<Expense[], Partial<Expense>>({
      query: (params) => ({
        url: 'expenses/',
        params,
      }),
      providesTags: ['Expense'],
    }),
    createExpense: builder.mutation<Expense, Partial<Expense>>({
      query: (data) => ({
        url: 'expenses/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Expense'],
    }),
    approveExpense: builder.mutation<Expense, number>({
      query: (id) => ({
        url: `expenses/${id}/approve/`,
        method: 'POST',
      }),
      invalidatesTags: ['Expense'],
    }),
    getExpenseSummary: builder.query<any[], { start_date?: string; end_date?: string }>({
      query: ({ start_date, end_date }) => ({
        url: 'expenses/summary/',
        params: { start_date, end_date },
      }),
      providesTags: ['Expense'],
    }),

    // Revenue
    getRevenue: builder.query<Revenue[], Partial<Revenue>>({
      query: (params) => ({
        url: 'revenue/',
        params,
      }),
      providesTags: ['Revenue'],
    }),
    createRevenue: builder.mutation<Revenue, Partial<Revenue>>({
      query: (data) => ({
        url: 'revenue/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Revenue'],
    }),
    getRevenueSummary: builder.query<any[], { start_date?: string; end_date?: string }>({
      query: ({ start_date, end_date }) => ({
        url: 'revenue/summary/',
        params: { start_date, end_date },
      }),
      providesTags: ['Revenue'],
    }),

    // Budgets
    getBudgets: builder.query<Budget[], Partial<Budget>>({
      query: (params) => ({
        url: 'budgets/',
        params,
      }),
      providesTags: ['Budget'],
    }),
    createBudget: builder.mutation<Budget, Partial<Budget>>({
      query: (data) => ({
        url: 'budgets/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Budget'],
    }),
    updateBudgetSpent: builder.mutation<Budget, { id: number; amount: number }>({
      query: ({ id, amount }) => ({
        url: `budgets/${id}/update_spent/`,
        method: 'POST',
        body: { amount },
      }),
      invalidatesTags: ['Budget'],
    }),
    getBudgetUtilization: builder.query<any[], void>({
      query: () => 'budgets/utilization/',
      providesTags: ['Budget'],
    }),

    // Financial Reports
    getFinancialReports: builder.query<FinancialReport[], Partial<FinancialReport>>({
      query: (params) => ({
        url: 'reports/',
        params,
      }),
      providesTags: ['FinancialReport'],
    }),
    createFinancialReport: builder.mutation<FinancialReport, Partial<FinancialReport>>({
      query: (data) => ({
        url: 'reports/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['FinancialReport'],
    }),
    exportFinancialReport: builder.mutation<any, number>({
      query: (id) => ({
        url: `reports/${id}/export/`,
        method: 'GET',
        responseHandler: 'text',
      }),
    }),

    // Analytics
    getFinanceAnalytics: builder.query<FinanceAnalytics, { start_date?: string; end_date?: string }>({
      query: ({ start_date, end_date }) => ({
        url: 'reports/analytics/',
        params: { start_date, end_date },
      }),
      providesTags: ['Payroll', 'Invoice', 'Expense', 'Revenue', 'Budget'],
    }),
    getProjectBurnRates: builder.query<ProjectBurnRate[], void>({
      query: () => 'reports/project_burn_rate/',
      providesTags: ['Budget', 'Expense'],
    }),
  }),
});

export const {
  useGetPayrollQuery,
  useCreatePayrollMutation,
  useApprovePayrollMutation,
  useMarkPayrollPaidMutation,
  useGetPayrollSummaryQuery,
  useGetInvoicesQuery,
  useCreateInvoiceMutation,
  useMarkInvoicePaidMutation,
  useSendInvoiceMutation,
  useGetOverdueInvoicesQuery,
  useGetExpensesQuery,
  useCreateExpenseMutation,
  useApproveExpenseMutation,
  useGetExpenseSummaryQuery,
  useGetRevenueQuery,
  useCreateRevenueMutation,
  useGetRevenueSummaryQuery,
  useGetBudgetsQuery,
  useCreateBudgetMutation,
  useUpdateBudgetSpentMutation,
  useGetBudgetUtilizationQuery,
  useGetFinancialReportsQuery,
  useCreateFinancialReportMutation,
  useExportFinancialReportMutation,
  useGetFinanceAnalyticsQuery,
  useGetProjectBurnRatesQuery,
} = financeApi;