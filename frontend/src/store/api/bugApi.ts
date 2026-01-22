import { baseApi } from './baseApi';

export const bugApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getBugs: builder.query<Record<string, any>[], Record<string, any>>({
      query: (params) => ({
        url: 'bugs/',
        params,
      }),
      providesTags: ['Bug'],
    }),
    createBug: builder.mutation<Record<string, any>, Record<string, any>>({
      query: (data) => ({
        url: 'bugs/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Bug'],
    }),
    updateBug: builder.mutation<Record<string, any>, { id: number; data: Record<string, any> }>({
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
