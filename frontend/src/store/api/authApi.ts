import { baseApi } from "@/store/api/baseApi";

export const authApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (credentials) => ({
        url: "token/",
        method: "POST",
        body: credentials,
      }),
    }),
    getProfile: builder.query({
      query: () => "profile/",
      providesTags: ["Auth"],
    }),
  }),
});

export const { useLoginMutation, useLazyGetProfileQuery } = authApi;
