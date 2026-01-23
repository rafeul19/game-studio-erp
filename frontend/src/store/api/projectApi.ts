import { baseApi } from "@/store/api/baseApi";

export interface StoryPointsResponse {
  suggested_points: number;
}

export interface SprintRiskResponse {
  risk_level: string;
}

export interface AssetReuseSuggestion {
  type: string;
  title: string;
  id: number;
  tags?: string;
}

export interface AssetReuseResponse {
  potential_reuse: AssetReuseSuggestion[];
}

export interface CapacityResponse {
  suggested_sprint_capacity: number;
}

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
    suggestStoryPoints: builder.mutation<StoryPointsResponse, { title: string; description: string }>({
      query: (data) => ({
        url: "tasks/suggest-points/",
        method: "POST",
        body: data,
      }),
    }),
    predictSprintRisk: builder.query<SprintRiskResponse, number>({
      query: (sprintId) => `sprints/${sprintId}/risk/`,
    }),
    detectAssetReuse: builder.mutation<AssetReuseResponse, { project_id: number; title: string }>({
      query: (data) => ({
        url: "tasks/asset-reuse/",
        method: "POST",
        body: data,
      }),
    }),
    sprintCapacityPlanning: builder.query<CapacityResponse, number>({
      query: (projectId) => `projects/${projectId}/suggested-capacity/`,
    }),
  }),
});

export const {
  useGetProjectsQuery,
  useCreateProjectMutation,
  useGetProjectProgressQuery,
  useSuggestStoryPointsMutation,
  usePredictSprintRiskQuery,
  useDetectAssetReuseMutation,
  useSprintCapacityPlanningQuery,
} = projectApi;
