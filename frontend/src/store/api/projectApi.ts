import { baseApi } from "@/store/api/baseApi";

export const projectApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getProjects: builder.query({
      query: () => "projects/my/",
      providesTags: ["Project"],
    }),
    createProject: builder.mutation({
      query: (project) => ({
        url: "projects/create/",
        method: "POST",
        body: project,
      }),
      invalidatesTags: ["Project"],
    }),
    getProjectProgress: builder.query({
      query: (id) => `projects/${id}/progress/`,
    }),
  }),
});

export const {
  useGetProjectsQuery,
  useCreateProjectMutation,
  useGetProjectProgressQuery,
} = projectApi;
