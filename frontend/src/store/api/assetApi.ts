import { baseApi } from './baseApi';

export const assetApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAssets: builder.query<any[], any>({
      query: (params) => ({
        url: 'assets/',
        params,
      }),
      providesTags: ['Asset'],
    }),
    createAsset: builder.mutation<any, any>({
      query: (data) => ({
        url: 'assets/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Asset'],
    }),
    addAssetVersion: builder.mutation<any, { assetId: number; data: any }>({
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
