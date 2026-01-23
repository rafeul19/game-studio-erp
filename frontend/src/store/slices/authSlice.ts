import { createSlice, PayloadAction } from "@reduxjs/toolkit"

interface AuthState {
  user: any | null
  isAuthenticated: boolean
  access: string | null
  refresh: string | null
}

const getInitialState = (): AuthState => {
  if (typeof window !== "undefined") {
    const access = localStorage.getItem("access")
    const refresh = localStorage.getItem("refresh")
    const userStr = localStorage.getItem("user")
    return {
      access,
      refresh,
      user: userStr ? JSON.parse(userStr) : null,
      isAuthenticated: !!access,
    }
  }
  return {
    user: null,
    isAuthenticated: false,
    access: null,
    refresh: null,
  }
}

const authSlice = createSlice({
  name: "auth",
  initialState: getInitialState(),
  reducers: {
    setCredentials: (
      state,
      action: PayloadAction<{ user: any; access: string; refresh: string }>
    ) => {
      const { user, access, refresh } = action.payload
      state.user = user
      state.access = access
      state.refresh = refresh
      state.isAuthenticated = true
      localStorage.setItem("access", access)
      localStorage.setItem("refresh", refresh)
      localStorage.setItem("user", JSON.stringify(user))
    },
    logout: (state) => {
      state.user = null
      state.access = null
      state.refresh = null
      state.isAuthenticated = false
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      localStorage.removeItem("user")
    },
  },
})

export const { setCredentials, logout } = authSlice.actions
export default authSlice.reducer
