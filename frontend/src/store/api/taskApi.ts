import { baseApi } from "@/store/api/baseApi";

export const taskApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getTasks: builder.query({
      query: () => "tasks/my/",
      providesTags: ["Task"],
    }),
    createTask: builder.mutation({
      query: (task) => ({
        url: "tasks/create/",
        method: "POST",
        body: task,
      }),
      invalidatesTags: ["Task"],
    }),
    updateTaskStatus: builder.mutation({
      query: ({ id, status }) => ({
        url: `tasks/${id}/status/`,
        method: "PATCH",
        body: { status },
      }),
      invalidatesTags: ["Task"],
    }),
    getTaskSuggestions: builder.query({
      query: (params) => ({
        url: "tasks/suggest-points/",
        params,
      }),
    }),
  }),
});

export const {
  useGetTasksQuery,
  useCreateTaskMutation,
  useUpdateTaskStatusMutation,
  useLazyGetTaskSuggestionsQuery,
} = taskApi;
