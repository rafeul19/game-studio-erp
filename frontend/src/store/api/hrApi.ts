import { baseApi } from './baseApi';

// HR Types
export interface Employee {
  id: number;
  user: number;
  user_info: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    full_name: string;
  };
  employee_id: string;
  department: string;
  department_name: string;
  position: string;
  hire_date: string;
  salary: number;
  phone: string;
  address: string;
  emergency_contact: string;
  emergency_phone: string;
  is_active: boolean;
  termination_date?: string;
  termination_reason: string;
  employment_status: string;
  years_of_service: number;
  skills: EmployeeSkill[];
  leave_requests?: LeaveRequest[];
  performance_reviews?: PerformanceReview[];
  attendance_records?: AttendanceRecord[];
  created_at: string;
  updated_at: string;
}

export interface EmployeeSkill {
  id: number;
  employee: number;
  skill: number;
  skill_name: string;
  skill_category: string;
  proficiency: number;
  proficiency_display: string;
  years_experience: number;
  certifications: string;
  last_used?: string;
  created_at: string;
  updated_at: string;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
  description: string;
  employee_count: number;
  created_at: string;
}

export interface LeaveRequest {
  id: number;
  employee: number;
  employee_name: string;
  employee_id: string;
  leave_type: string;
  leave_type_display: string;
  start_date: string;
  end_date: string;
  days_requested: number;
  reason: string;
  status: string;
  status_display: string;
  approved_by?: number;
  approved_by_name?: string;
  approval_date?: string;
  approval_comments: string;
  created_at: string;
  updated_at: string;
}

export interface PerformanceReview {
  id: number;
  employee: number;
  employee_name: string;
  review_type: string;
  review_type_display: string;
  review_date: string;
  reviewer: number;
  reviewer_name: string;
  overall_rating: number;
  overall_rating_display: string;
  strengths: string;
  areas_for_improvement: string;
  goals: string;
  technical_skills_rating: number;
  communication_rating: number;
  teamwork_rating: number;
  problem_solving_rating: number;
  leadership_rating?: number;
  average_rating: number;
  comments: string;
  created_at: string;
  updated_at: string;
}

export interface AttendanceRecord {
  id: number;
  employee: number;
  employee_name: string;
  employee_id: string;
  date: string;
  check_in?: string;
  check_out?: string;
  status: string;
  status_display: string;
  notes: string;
  overtime_hours: number;
  hours_worked: number;
  created_at: string;
  updated_at: string;
}

export interface Department {
  id: number;
  name: string;
  description: string;
  manager?: number;
  manager_name?: string;
  budget?: number;
  parent_department?: number;
  employee_count: number;
  created_at: string;
  updated_at: string;
}

export interface HRAnalytics {
  overview: {
    total_employees: number;
    total_departments: number;
    active_employees: number;
  };
  department_distribution: Array<{
    department: string;
    count: number;
  }>;
  skill_coverage: Array<{
    skill_name: string;
    employee_count: number;
  }>;
  recent_leave_requests: LeaveRequest[];
  upcoming_reviews: PerformanceReview[];
  attendance_summary: Array<{
    status: string;
    count: number;
  }>;
}

export const hrApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Employees
    getEmployees: builder.query<Employee[], Partial<Employee>>({
      query: (params) => ({
        url: 'hr/employees/',
        params,
      }),
      providesTags: ['Employee'],
    }),
    getEmployee: builder.query<Employee, number>({
      query: (id) => `hr/employees/${id}/`,
      providesTags: ['Employee'],
    }),
    createEmployee: builder.mutation<Employee, Partial<Employee>>({
      query: (data) => ({
        url: 'hr/employees/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Employee'],
    }),
    updateEmployee: builder.mutation<Employee, { id: number; data: Partial<Employee> }>({
      query: ({ id, data }) => ({
        url: `hr/employees/${id}/`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: ['Employee'],
    }),
    deleteEmployee: builder.mutation<void, number>({
      query: (id) => ({
        url: `hr/employees/${id}/`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Employee'],
    }),
    getEmployeeSkillsMatrix: builder.query<any[], void>({
      query: () => 'hr/employees/skills_matrix/',
      providesTags: ['Employee', 'Skill'],
    }),
    getHRAnalytics: builder.query<HRAnalytics, void>({
      query: () => 'hr/employees/analytics/',
      providesTags: ['Employee', 'LeaveRequest', 'PerformanceReview', 'Attendance'],
    }),
    addEmployeeSkill: builder.mutation<EmployeeSkill, { employeeId: number; data: Partial<EmployeeSkill> }>({
      query: ({ employeeId, data }) => ({
        url: `hr/employees/${employeeId}/add_skill/`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Employee'],
    }),

    // Skills
    getSkills: builder.query<Skill[], Partial<Skill>>({
      query: (params) => ({
        url: 'hr/skills/',
        params,
      }),
      providesTags: ['Skill'],
    }),
    createSkill: builder.mutation<Skill, Partial<Skill>>({
      query: (data) => ({
        url: 'hr/skills/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Skill'],
    }),

    // Departments
    getDepartments: builder.query<Department[], Partial<Department>>({
      query: (params) => ({
        url: 'hr/departments/',
        params,
      }),
      providesTags: ['Department'],
    }),
    createDepartment: builder.mutation<Department, Partial<Department>>({
      query: (data) => ({
        url: 'hr/departments/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Department'],
    }),

    // Leave Requests
    getLeaveRequests: builder.query<LeaveRequest[], Partial<LeaveRequest>>({
      query: (params) => ({
        url: 'hr/leave-requests/',
        params,
      }),
      providesTags: ['LeaveRequest'],
    }),
    createLeaveRequest: builder.mutation<LeaveRequest, Partial<LeaveRequest>>({
      query: (data) => ({
        url: 'hr/leave-requests/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['LeaveRequest'],
    }),
    approveLeaveRequest: builder.mutation<LeaveRequest, number>({
      query: (id) => ({
        url: `hr/leave-requests/${id}/approve/`,
        method: 'POST',
      }),
      invalidatesTags: ['LeaveRequest'],
    }),
    rejectLeaveRequest: builder.mutation<LeaveRequest, number>({
      query: (id) => ({
        url: `hr/leave-requests/${id}/reject/`,
        method: 'POST',
      }),
      invalidatesTags: ['LeaveRequest'],
    }),

    // Performance Reviews
    getPerformanceReviews: builder.query<PerformanceReview[], Partial<PerformanceReview>>({
      query: (params) => ({
        url: 'hr/performance-reviews/',
        params,
      }),
      providesTags: ['PerformanceReview'],
    }),
    createPerformanceReview: builder.mutation<PerformanceReview, Partial<PerformanceReview>>({
      query: (data) => ({
        url: 'hr/performance-reviews/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['PerformanceReview'],
    }),

    // Attendance
    getAttendance: builder.query<AttendanceRecord[], Partial<AttendanceRecord>>({
      query: (params) => ({
        url: 'hr/attendance/',
        params,
      }),
      providesTags: ['Attendance'],
    }),
    createAttendanceRecord: builder.mutation<AttendanceRecord, Partial<AttendanceRecord>>({
      query: (data) => ({
        url: 'hr/attendance/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Attendance'],
    }),
    getAttendanceSummary: builder.query<any[], { start_date: string; end_date: string }>({
      query: ({ start_date, end_date }) => ({
        url: 'hr/attendance/summary/',
        params: { start_date, end_date },
      }),
      providesTags: ['Attendance'],
    }),
  }),
});

export const {
  useGetEmployeesQuery,
  useGetEmployeeQuery,
  useCreateEmployeeMutation,
  useUpdateEmployeeMutation,
  useDeleteEmployeeMutation,
  useGetEmployeeSkillsMatrixQuery,
  useGetHRAnalyticsQuery,
  useAddEmployeeSkillMutation,
  useGetSkillsQuery,
  useCreateSkillMutation,
  useGetDepartmentsQuery,
  useCreateDepartmentMutation,
  useGetLeaveRequestsQuery,
  useCreateLeaveRequestMutation,
  useApproveLeaveRequestMutation,
  useRejectLeaveRequestMutation,
  useGetPerformanceReviewsQuery,
  useCreatePerformanceReviewMutation,
  useGetAttendanceQuery,
  useCreateAttendanceRecordMutation,
  useGetAttendanceSummaryQuery,
} = hrApi;