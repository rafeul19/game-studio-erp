import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export const baseApi = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000/api/",
    prepareHeaders: (headers) => {
      // Check if window is defined (browser-side)
      if (typeof window !== "undefined") {
        const token = localStorage.getItem("access")
        if (token) {
          headers.set("Authorization", `Bearer ${token}`)
        }
      }
      return headers
    },
  }),
  tagTypes: ["Project", "Task", "Sprint", "Auth"],
  endpoints: () => ({}),
})
