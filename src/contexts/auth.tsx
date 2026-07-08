import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import type { Role } from "@/data/mock";
import { toast } from "sonner";

export interface AuthUser {
  id: string;
  display_id: string;
  name: string;
  email: string;
  role: Role;
  avatar: string;
  must_change_password: boolean;
}

interface AuthCtx {
  user: AuthUser | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  forceChangePassword: (password: string) => Promise<void>;
  refreshProfile: () => Promise<void>;
}

const Ctx = createContext<AuthCtx | null>(null);

const API_BASE = "http://localhost:8000/api";

export function getAuthHeaders() {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("itsm.token");
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshProfile = async () => {
    const token = localStorage.getItem("itsm.token");
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: getAuthHeaders(),
      });
      const result = await response.json();
      if (result.success && result.data) {
        setUser(result.data);
      } else {
        // Token invalid or expired
        logout();
      }
    } catch (error) {
      console.error("Failed to load user profile:", error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshProfile();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      
      const result = await response.json();
      
      if (result.success && result.data) {
        const { access_token, user: profile } = result.data;
        localStorage.setItem("itsm.token", access_token);
        setUser(profile);
        toast.success(`Welcome back, ${profile.name}`);
      } else {
        const errorMsg = result.message || "Invalid credentials";
        toast.error(errorMsg);
        throw new Error(errorMsg);
      }
    } catch (error: any) {
      console.error("Login failed:", error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("itsm.token");
    toast.info("Signed out of session");
  };

  const forceChangePassword = async (password: string) => {
    try {
      const response = await fetch(`${API_BASE}/auth/force-change-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders(),
        },
        body: JSON.stringify({ new_password: password }),
      });
      
      const result = await response.json();
      if (result.success) {
        toast.success("Password changed successfully!");
        if (user) {
          setUser({ ...user, must_change_password: false });
        }
      } else {
        toast.error(result.message || "Failed to update password");
      }
    } catch (error) {
      console.error("Password update error:", error);
      toast.error("An error occurred during password change.");
    }
  };

  return (
    <Ctx.Provider value={{ user, loading, login, logout, forceChangePassword, refreshProfile }}>
      {!loading && children}
    </Ctx.Provider>
  );
}

export function useAuth() {
  const c = useContext(Ctx);
  if (!c) throw new Error("useAuth outside provider");
  return c;
}
