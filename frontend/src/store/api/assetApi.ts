import { baseApi } from './baseApi';

export const assetApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAssets: builder.query<Record<string, any>[], Record<string, any>>({
      query: (params) => ({
        url: 'assets/',
        params,
      }),
      providesTags: ['Asset'],
    }),
    createAsset: builder.mutation<Record<string, any>, Record<string, any>>({
      query: (data) => ({
        url: 'assets/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Asset'],
    }),
    addAssetVersion: builder.mutation<Record<string, any>, { assetId: number; data: Record<string, any> }>({
      query: ({ assetId, data }) => ({
        url: `assets/${assetId}/add_version/`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Asset'],
    }),
  }),
});

export const {
  useGetAssetsQuery,
  useCreateAssetMutation,
  useAddAssetVersionMutation,
} = assetApi;
