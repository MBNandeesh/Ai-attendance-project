"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  faceLogin,
  registerStudent,
  storeSession,
  mySubjects,
  joinByCode,
  studentRecords,
  fileToBase64,
  ApiError,
  type Subject,
  type AttendanceRecord,
} from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

type View = "login" | "dashboard";

export default function StudentPortal() {
  return <StudentPortalInner />;
}

function StudentPortalInner() {
  const { me, loading, setSession, logout } = useAuth();
  const router = useRouter();
  const [view, setView] = useState<View>("login");

  useEffect(() => {
    if (!loading && me) setView("dashboard");
  }, [loading, me]);

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center text-[var(--ink-dim)]">
        Loading…
      </main>
    );
  }

  if (view === "dashboard" && me) {
    return <StudentDashboard name={me.name} onLogout={() => { logout(); setView("login"); }} />;
  }

  return <StudentAuth onAuthed={(auth) => { setSession({ user_id: auth.user_id, role: auth.role, name: auth.name }); setView("dashboard"); }} />;
}

/* ------------------------------------------------------------------ */
/* Auth: face login / register                                         */
/* ------------------------------------------------------------------ */

function StudentAuth({ onAuthed }: { onAuthed: (auth: { user_id: number; role: string; name: string }) => void }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [cameraOn, setCameraOn] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [registerName, setRegisterName] = useState("");
  const [showRegister, setShowRegister] = useState(false);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 640 } },
        audio: false,
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
        setCameraOn(true);
      }
    } catch {
      setError("Camera access denied. Allow camera to use Face ID login.");
    }
  }, []);

  useEffect(() => {
    startCamera();
    return () => {
      const stream = videoRef.current?.srcObject as MediaStream | null;
      stream?.getTracks().forEach((t) => t.stop());
    };
  }, [startCamera]);

  function capture(): string | null {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return null;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d")!.drawImage(video, 0, 0);
    return canvas.toDataURL("image/jpeg", 0.9).split(",")[1];
  }

  async function handleLogin() {
    setError(null);
    setInfo(null);
    const b64 = capture();
    if (!b64) return setError("Camera not ready");

    setBusy(true);
    try {
      const auth = await faceLogin(b64);
      onAuthed(auth);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        setShowRegister(true);
        setInfo("Face not recognized — register below to create your profile.");
      } else {
        setError(err instanceof ApiError ? err.message : "Login failed");
      }
    } finally {
      setBusy(false);
    }
  }

  async function handleRegister() {
    setError(null);
    setInfo(null);
    if (!registerName.trim()) return setError("Enter your name first");
    const b64 = capture();
    if (!b64) return setError("Camera not ready");

    setBusy(true);
    try {
      const auth = await registerStudent(registerName.trim(), b64);
      onAuthed(auth);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Registration failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center px-4">
      <div className="aurora-bg" />
      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="glass w-full max-w-lg p-8">
        <a href="/" className="text-sm text-[var(--ink-faint)] transition hover:text-white">← Back to home</a>
        <h1 className="mt-4 text-2xl font-black tracking-tight">Student Portal</h1>
        <p className="mt-1 text-sm text-[var(--ink-dim)]">Passwordless Face ID login</p>

        <div className="relative mt-6 overflow-hidden rounded-xl border border-white/10 bg-black/40">
          <video ref={videoRef} className="aspect-[4/3] w-full object-cover" muted playsInline />
          <canvas ref={canvasRef} className="hidden" />
          {!cameraOn && (
            <div className="absolute inset-0 grid place-items-center text-sm text-[var(--ink-dim)]">
              Camera starting…
            </div>
          )}
        </div>

        {error && <p className="mt-4 rounded-xl border border-rose-500/25 bg-rose-500/10 px-4 py-2.5 text-sm text-rose-300">{error}</p>}
        {info && <p className="mt-4 rounded-xl border border-cyan-500/25 bg-cyan-500/10 px-4 py-2.5 text-sm text-cyan-200">{info}</p>}

        <div className="mt-6 flex gap-3">
          <button onClick={handleLogin} disabled={busy || !cameraOn} className="btn-primary flex-1 justify-center disabled:opacity-60">
            {busy ? "Scanning…" : "Sign in with Face ID"}
          </button>
          <button onClick={startCamera} className="btn-ghost">Retry camera</button>
        </div>

        {showRegister && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 border-t border-white/10 pt-6">
            <h2 className="font-bold">Register New Profile</h2>
            <p className="mt-1 text-sm text-[var(--ink-dim)]">Look at the camera and enter your name.</p>
            <input
              value={registerName}
              onChange={(e) => setRegisterName(e.target.value)}
              placeholder="Your full name"
              className="field mt-3"
            />
            <button onClick={handleRegister} disabled={busy} className="btn-primary mt-3 w-full justify-center disabled:opacity-60">
              Create Account
            </button>
          </motion.div>
        )}
      </motion.div>
    </main>
  );
}

/* ------------------------------------------------------------------ */
/* Dashboard: subjects + join + records                                */
/* ------------------------------------------------------------------ */

function StudentDashboard({ name, onLogout }: { name: string; onLogout: () => void }) {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [joinCode, setJoinCode] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setSubjects(await mySubjects());
      setRecords(await studentRecords());
    } catch {
      // token expired and refresh failed — parent handles logout
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function handleJoin() {
    setError(null);
    setMessage(null);
    try {
      const subject = await joinByCode(joinCode.trim());
      setMessage(`Joined ${subject.name}!`);
      setJoinCode("");
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not join");
    }
  }

  const totalSessions = records.length;
  const presentCount = records.filter((r) => r.is_present).length;
  const rate = totalSessions ? Math.round((presentCount / totalSessions) * 100) : 0;

  return (
    <main className="relative min-h-screen px-4 py-10 sm:px-6">
      <div className="aurora-bg" />
      <div className="mx-auto max-w-5xl">
        <motion.header initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-black tracking-tight sm:text-3xl">
              Hi, <span className="text-gradient">{name}</span>
            </h1>
            <p className="mt-1 flex items-center gap-2 text-sm text-[var(--ink-dim)]">
              <span className="pulse-dot" /> Student workspace
            </p>
          </div>
          <button onClick={onLogout} className="btn-ghost !py-2.5">Logout</button>
        </motion.header>

        <div className="mt-8 grid grid-cols-3 gap-3 sm:gap-5">
          {[
            { label: "Subjects", value: subjects.length },
            { label: "Sessions", value: totalSessions },
            { label: "Attendance", value: `${rate}%` },
          ].map((s) => (
            <div key={s.label} className="glass p-4 sm:p-6">
              <div className="text-2xl font-black text-gradient sm:text-3xl">{s.value}</div>
              <div className="mt-1 text-xs text-[var(--ink-dim)] sm:text-sm">{s.label}</div>
            </div>
          ))}
        </div>

        <div className="mt-8 glass p-5 sm:p-7">
          <h2 className="font-bold">Join a subject</h2>
          <p className="mt-1 text-sm text-[var(--ink-dim)]">Enter the code your teacher shared.</p>
          <div className="mt-4 flex flex-col gap-3 sm:flex-row">
            <input
              value={joinCode}
              onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
              placeholder="ABCD2345"
              maxLength={8}
              className="field flex-1 font-mono tracking-widest uppercase"
            />
            <button onClick={handleJoin} disabled={joinCode.length < 6} className="btn-primary justify-center disabled:opacity-50">
              Join
            </button>
          </div>
          {message && <p className="mt-3 text-sm text-emerald-300">{message}</p>}
          {error && <p className="mt-3 text-sm text-rose-300">{error}</p>}
        </div>

        <h2 className="mt-10 text-lg font-bold">My Subjects</h2>
        {subjects.length === 0 ? (
          <p className="mt-3 text-sm text-[var(--ink-dim)]">No subjects yet — join one with a code above.</p>
        ) : (
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            {subjects.map((s) => {
              const mine = records.filter((r) => r.subject_id === s.subject_id);
              const present = mine.filter((r) => r.is_present).length;
              return (
                <div key={s.subject_id} className="glass feature-card p-5">
                  <div className="text-xs font-semibold tracking-widest text-[var(--ink-faint)]">{s.subject_code}</div>
                  <div className="mt-1 font-bold">{s.name}</div>
                  <div className="mt-3 flex items-center gap-3">
                    <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/10">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-[var(--accent)] to-[var(--cyan)]"
                        style={{ width: `${mine.length ? (present / mine.length) * 100 : 0}%` }}
                      />
                    </div>
                    <span className="text-sm text-[var(--ink-dim)]">{present}/{mine.length}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </main>
  );
}
