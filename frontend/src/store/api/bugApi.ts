import { baseApi } from './baseApi';
import { Bug } from '@/types/models';

export const bugApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getBugs: builder.query<Bug[], Partial<Bug>>({
      query: (params) => ({
        url: 'bugs/',
        params,
      }),
      providesTags: ['Bug'],
    }),
    createBug: builder.mutation<Bug, Partial<Bug>>({
      query: (data) => ({
        url: 'bugs/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Bug'],
    }),
    updateBug: builder.mutation<Bug, { id: number; data: Partial<Bug> }>({
      query: ({ id, data }) => ({
        url: `bugs/${id}/`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: ['Bug'],
    }),
  }),
});

export const {
  useGetBugsQuery,
  useCreateBugMutation,
  useUpdateBugMutation,
} = bugApi;
