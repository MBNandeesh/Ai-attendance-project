"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { clearTokens, fetchMe, getStoredRole, getStoredTokens, type Me } from "@/lib/api";

type AuthState = {
  me: Me | null;
  loading: boolean;
  setSession: (me: Me) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const tokens = getStoredTokens();
    const role = getStoredRole();
    if (!tokens || !role) {
      setLoading(false);
      return;
    }
    fetchMe(role)
      .then(setMe)
      .catch(() => clearTokens())
      .finally(() => setLoading(false));
  }, []);

  const logout = useCallback(() => {
    clearTokens();
    setMe(null);
  }, []);

  const value = useMemo(
    () => ({ me, loading, setSession: setMe, logout }),
    [me, loading, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
