import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getCurrentUser, signIn } from "aws-amplify/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkExistingSession = async () => {
      try {
        await getCurrentUser();
        navigate("/dashboard", { replace: true });
      } catch {
        // Chưa đăng nhập, cho ở lại trang login
      } finally {
        setCheckingSession(false);
      }
    };

    checkExistingSession();
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setMsg("");

    const normalizedEmail = email.trim().toLowerCase();

    if (!normalizedEmail) {
      setMsg("Email is required");
      return;
    }

    if (!password) {
      setMsg("Password is required");
      return;
    }

    setLoading(true);

    try {
      const result = await signIn({
        username: normalizedEmail,
        password,
      });

      console.log("signIn result:", result);

      if (result?.isSignedIn) {
        window.__toast?.("Logging in successful 🎉", "success");
        navigate("/dashboard");
        return;
      }

      const step = result?.nextStep?.signInStep;

      if (
        step === "CONFIRM_SIGN_UP" ||
        step === "CONFIRM_SIGN_IN_WITH_EMAIL_CODE" ||
        step === "CONFIRM_SIGN_IN_WITH_SMS_CODE"
      ) {
        window.__toast?.("Please confirm your account first", "warn");
        navigate(`/confirm?email=${encodeURIComponent(normalizedEmail)}`);
        return;
      }

      setMsg(`Additional auth step required: ${step || "unknown step"}`);
      window.__toast?.("Additional auth step required", "warn");
    } catch (err) {
      console.error(err);

      if (err?.name === "UserAlreadyAuthenticatedException") {
        window.__toast?.("You are already signed in", "warn");
        navigate("/dashboard", { replace: true });
        return;
      }

      const errorMessage = err?.message || "Logging in failed";
      setMsg(errorMessage);
      window.__toast?.(errorMessage, "error");
    } finally {
      setLoading(false);
    }
  };

  if (checkingSession) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f5f6fa]">
        <div className="rounded-2xl bg-white px-6 py-4 text-sm text-slate-600 shadow">
          Checking session...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f5f6fa] p-4 md:p-8 flex items-center justify-center">
      <div className="mx-auto grid w-full max-w-6xl overflow-hidden rounded-[28px] bg-white shadow-xl lg:grid-cols-[1.15fr_0.85fr]">
        <div className="relative hidden min-h-[520px] overflow-hidden bg-gradient-to-br from-indigo-500 to-indigo-700 lg:block">
          <div className="absolute left-10 top-10 z-10 text-4xl font-black text-white">
            Sound Capture
          </div>

          <div className="relative z-10 max-w-lg px-10 pt-28 text-white">
            <h1 className="text-6xl font-black leading-[0.95]">
              The Exquisite
              <br />
              Archivist.
            </h1>
            <p className="mt-6 text-lg leading-8 text-white/80">
              Transforming the fluid nature of audio into high-fidelity
              intelligence with editorial precision.
            </p>
          </div>

          <div className="absolute bottom-0 left-[30%] h-[60%] w-[80%] rounded-tl-[40px] bg-[linear-gradient(180deg,rgba(30,58,138,0.25),rgba(147,197,253,0.28))]" />
        </div>

        <div className="flex items-center justify-center bg-slate-100 p-6 md:p-8">
          <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow">
            <h1 className="text-3xl font-bold text-slate-900">Login</h1>

            <form onSubmit={handleLogin} className="mt-6 space-y-4">
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-12 w-full rounded-xl border border-slate-200 px-4 outline-none"
              />

              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-12 w-full rounded-xl border border-slate-200 px-4 outline-none"
              />

              <button
                type="submit"
                disabled={loading}
                className="h-12 w-full rounded-xl bg-indigo-600 font-semibold text-white hover:bg-indigo-700 disabled:opacity-60"
              >
                {loading ? "Logging in..." : "Login"}
              </button>
            </form>

            {msg && (
              <div className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-600">
                {msg}
              </div>
            )}

            <p className="mt-5 text-sm text-slate-500">
              Register?{" "}
              <Link to="/register" className="font-semibold text-indigo-600">
                Register
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
