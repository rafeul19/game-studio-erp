import { baseApi } from './baseApi';
import { Asset, AssetVersion } from '@/types/models';

export const assetApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAssets: builder.query<Asset[], Partial<Asset>>({
      query: (params) => ({
        url: 'assets/',
        params,
      }),
      providesTags: ['Asset'],
    }),
    createAsset: builder.mutation<Asset, Partial<Asset>>({
      query: (data) => ({
        url: 'assets/',
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Asset'],
    }),
    addAssetVersion: builder.mutation<AssetVersion, { assetId: number; data: Partial<AssetVersion> }>({
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
