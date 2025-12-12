import { createContext, useContext, useState, ReactNode } from "react";

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  email: string | null;
}

interface AuthContextType extends AuthState {
  setTokens: (access: string, refresh: string, email: string) => void;
  clear: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState<AuthState>({ accessToken: null, refreshToken: null, email: null });

  const setTokens = (access: string, refresh: string, email: string) => {
    setAuth({ accessToken: access, refreshToken: refresh, email });
  };

  const clear = () => setAuth({ accessToken: null, refreshToken: null, email: null });

  return <AuthContext.Provider value={{ ...auth, setTokens, clear }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
