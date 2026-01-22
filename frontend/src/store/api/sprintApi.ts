import { baseApi } from "@/store/api/baseApi";

export const sprintApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getProjectSprints: builder.query({
      query: (projectId) => `projects/${projectId}/sprints/`,
      providesTags: ["Sprint"],
    }),
    createSprint: builder.mutation({
      query: (sprint) => ({
        url: "sprints/create/",
        method: "POST",
        body: sprint,
      }),
      invalidatesTags: ["Sprint"],
    }),
    getSprintProgress: builder.query({
      query: (id) => `sprints/${id}/progress/`,
    }),
    getSprintRisk: builder.query({
      query: (id) => `sprints/${id}/risk/`,
    }),
    getSuggestedCapacity: builder.query({
      query: (projectId) => `projects/${projectId}/suggested-capacity/`,
    }),
  }),
});

export const {
  useGetProjectSprintsQuery,
  useCreateSprintMutation,
  useGetSprintProgressQuery,
  useGetSprintRiskQuery,
  useLazyGetSuggestedCapacityQuery,
} = sprintApi;
