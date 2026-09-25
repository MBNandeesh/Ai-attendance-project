"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { loginTeacher, registerTeacher, storeSession, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

type Mode = "login" | "register";

export default function TeacherLoginPage() {
  const router = useRouter();
  const { setSession } = useAuth();
  const [mode, setMode] = useState<Mode>("login");
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (mode === "register") {
        await registerTeacher(username, name, password);
      }
      const auth = await loginTeacher(username, password);
      storeSession(auth);
      // Update in-memory auth state before navigating — otherwise the
      // dashboard guard sees `me === null` and bounces back to /login.
      setSession({ user_id: auth.user_id, role: auth.role, name: auth.name });
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center px-4">
      <div className="aurora-bg" />

      <motion.div
        initial={{ opacity: 0, y: 26, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] }}
        className="glass w-full max-w-md p-9"
      >
        <Link href="/" className="mb-6 inline-flex items-center gap-2 text-sm text-[var(--ink-faint)] transition hover:text-white">
          ← Back to home
        </Link>

        <h1 className="text-2xl font-black tracking-tight">
          {mode === "login" ? "Teacher Login" : "Create Teacher Account"}
        </h1>
        <p className="mt-1 text-sm text-[var(--ink-dim)]">AI Attendance System</p>

        <form onSubmit={handleSubmit} className="mt-7 space-y-4">
          {mode === "register" && (
            <div>
              <label htmlFor="name" className="mb-1.5 block text-sm font-medium text-[var(--ink-dim)]">
                Full name
              </label>
              <input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none transition focus:border-indigo-400/60 focus:bg-white/[0.07] focus:shadow-[0_0_0_4px_rgba(99,102,241,0.12)]"
                placeholder="Your name"
              />
            </div>
          )}

          <div>
            <label htmlFor="username" className="mb-1.5 block text-sm font-medium text-[var(--ink-dim)]">
              Username
            </label>
            <input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none transition focus:border-indigo-400/60 focus:bg-white/[0.07] focus:shadow-[0_0_0_4px_rgba(99,102,241,0.12)]"
              placeholder="Enter username"
            />
          </div>

          <div>
            <label htmlFor="password" className="mb-1.5 block text-sm font-medium text-[var(--ink-dim)]">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none transition focus:border-indigo-400/60 focus:bg-white/[0.07] focus:shadow-[0_0_0_4px_rgba(99,102,241,0.12)]"
              placeholder="Enter password"
            />
          </div>

          {error && (
            <motion.p
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-xl border border-rose-500/25 bg-rose-500/10 px-4 py-2.5 text-sm text-rose-300"
            >
              {error}
            </motion.p>
          )}

          <button type="submit" disabled={busy} className="btn-primary w-full justify-center disabled:opacity-60">
            {busy ? "Please wait…" : mode === "login" ? "Login →" : "Register & Login →"}
          </button>
        </form>

        <button
          onClick={() => {
            setMode(mode === "login" ? "register" : "login");
            setError(null);
          }}
          className="mt-5 w-full text-center text-sm text-[var(--ink-dim)] transition hover:text-white"
        >
          {mode === "login" ? "No account? Register instead" : "Have an account? Login"}
        </button>
      </motion.div>
    </main>
  );
}
