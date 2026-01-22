import { baseApi } from './baseApi';

export const bugApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getBugs: builder.query<any[], any>({
      query: (params) => ({
        url: 'bugs/',
        params,
      }),
      providesTags: ['Bug'],
    }),
    createBug: builder.mutation<any, any>({
      query: (data) => ({
        url: 'bugs/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Bug'],
    }),
    updateBug: builder.mutation<any, { id: number; data: any }>({
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
