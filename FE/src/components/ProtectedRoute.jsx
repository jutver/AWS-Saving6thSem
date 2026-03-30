import React, { useEffect, useState } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { getCurrentUser, fetchAuthSession } from "aws-amplify/auth";

export default function ProtectedRoute({ children }) {
  const [status, setStatus] = useState("checking");
  const location = useLocation();

  useEffect(() => {
    let mounted = true;

    async function checkAuth() {
      try {
        await getCurrentUser();
        const session = await fetchAuthSession();

        const hasToken = Boolean(
          session?.tokens?.accessToken || session?.tokens?.idToken,
        );

        if (!mounted) return;
        setStatus(hasToken ? "authenticated" : "unauthenticated");
      } catch (err) {
        if (!mounted) return;
        setStatus("unauthenticated");
      }
    }

    checkAuth();

    return () => {
      mounted = false;
    };
  }, []);

  if (status === "checking") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-100">
        <div className="text-sm text-slate-600">Checking authentication...</div>
      </div>
    );
  }

  if (status === "unauthenticated") {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return children;
}
