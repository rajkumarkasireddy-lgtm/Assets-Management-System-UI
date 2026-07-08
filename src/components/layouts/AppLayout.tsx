import { useEffect, useState, type ReactNode } from "react";
import { Outlet, useNavigate, useRouterState } from "@tanstack/react-router";
import { motion, AnimatePresence } from "framer-motion";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { useAuth } from "@/contexts/auth";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { KeyRound } from "lucide-react";
import { NAV } from "@/lib/nav";

export function AppLayout({ children }: { children?: ReactNode }) {
  const { user, forceChangePassword } = useAuth();
  const navigate = useNavigate();
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [collapsed, setCollapsed] = useState(false);
  const [hydrated, setHydrated] = useState(false);
  
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => { setHydrated(true); }, []);
  
  useEffect(() => {
    if (hydrated && !user) {
      navigate({ to: "/login" });
      return;
    }

    if (user) {
      // Base routes allowed for all logged-in roles
      const allowed = new Set(["/dashboard", "/profile", "/notifications", "/search", "/roles"]);
      
      // Load allowed routes configured for the user's role
      const groups = NAV[user.role] || [];
      groups.forEach((g) => {
        g.items.forEach((item) => {
          allowed.add(item.to);
        });
      });
      
      const normalizedPath = pathname.replace(/\/$/, "");
      
      // If navigating to a restricted path, redirect to dashboard with Access Denied toast
      if (
        normalizedPath.startsWith("/") &&
        normalizedPath !== "/login" &&
        normalizedPath !== "" &&
        !allowed.has(normalizedPath)
      ) {
        toast.error("Access Denied: You do not have permission to view that page.");
        navigate({ to: "/dashboard", replace: true });
      }
    }
  }, [hydrated, user, pathname, navigate]);

  if (!hydrated || !user) {
    return <div className="min-h-screen grid place-items-center text-muted-foreground text-sm">Loading…</div>;
  }

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword.length < 6) {
      toast.error("Password must be at least 6 characters long.");
      return;
    }
    if (newPassword !== confirmPassword) {
      toast.error("Passwords do not match.");
      return;
    }
    setIsSubmitting(true);
    try {
      await forceChangePassword(newPassword);
    } catch (err) {
      // Error handled in auth context
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen w-full bg-background relative">
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />
      <div className="flex-1 min-w-0 flex flex-col">
        <Topbar />
        <main className="flex-1 p-6 max-w-[1600px] w-full mx-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={pathname}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.18 }}
            >
              {children ?? <Outlet />}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* Forced Password Change Overlay */}
      {user.must_change_password && (
        <div className="fixed inset-0 z-[9999] bg-background/80 backdrop-blur-md flex items-center justify-center p-4">
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="w-full max-w-md"
          >
            <Card className="p-6 shadow-xl border-primary/20">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-10 w-10 rounded-lg bg-primary/10 text-primary grid place-items-center">
                  <KeyRound className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Update Temporary Password</h3>
                  <p className="text-xs text-muted-foreground">For security, you must update your password on first login.</p>
                </div>
              </div>

              <form onSubmit={handlePasswordSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-medium">New Password</label>
                  <Input
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Enter new password"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-medium">Confirm New Password</label>
                  <Input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter new password"
                  />
                </div>

                <Button type="submit" className="w-full" disabled={isSubmitting}>
                  {isSubmitting ? "Updating..." : "Save Password"}
                </Button>
              </form>
            </Card>
          </motion.div>
        </div>
      )}
    </div>
  );
}
