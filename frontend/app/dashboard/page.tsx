"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  createSubject,
  listTeacherSubjects,
  createSession,
  submitFaceAttendance,
  teacherRecords,
  attendanceCsvUrl,
  fileToBase64,
  getStoredTokens,
  ApiError,
  type Subject,
  type AttendanceRecord,
  type AttendanceMarkResult,
} from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

type Tab = "attendance" | "subjects" | "records";

export default function DashboardPage() {
  const { me, loading, logout } = useAuth();
  const router = useRouter();
  const [tab, setTab] = useState<Tab>("attendance");

  useEffect(() => {
    if (!loading && !me) router.replace("/login");
  }, [loading, me, router]);

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[var(--void)] text-[var(--ink-dim)]">
        Loading your workspace…
      </main>
    );
  }
  if (!me) return null;

  return (
    <main className="relative min-h-screen px-4 py-8 sm:px-6 sm:py-10">
      <div className="aurora-bg" />
      <div className="mx-auto max-w-5xl">
        <motion.header initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-black tracking-tight sm:text-3xl">
              Welcome, <span className="text-gradient">{me.name}</span>
            </h1>
            <p className="mt-1 flex items-center gap-2 text-sm text-[var(--ink-dim)]">
              <span className="pulse-dot" /> Teacher dashboard · session active
            </p>
          </div>
          <button onClick={() => { logout(); router.replace("/login"); }} className="btn-ghost !py-2.5">
            Logout
          </button>
        </motion.header>

        <div className="mt-8 flex gap-2">
          {(
            [
              ["attendance", "Take Attendance"],
              ["subjects", "Subjects"],
              ["records", "Records"],
            ] as [Tab, string][]
          ).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={tab === key ? "btn-primary !py-2.5" : "btn-ghost !py-2.5"}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="mt-6">
          {tab === "attendance" && <TakeAttendance />}
          {tab === "subjects" && <Subjects />}
          {tab === "records" && <Records />}
        </div>
      </div>
    </main>
  );
}

/* ------------------------------- Subjects ------------------------------- */

function Subjects() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [section, setSection] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState<number | null>(null);

  const refresh = useCallback(() => {
    listTeacherSubjects().then(setSubjects).catch(() => {});
  }, []);

  useEffect(refresh, [refresh]);

  async function handleCreate() {
    setError(null);
    try {
      await createSubject(code.trim(), name.trim(), section.trim() || "-");
      setCode(""); setName(""); setSection("");
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not create subject");
    }
  }

  return (
    <div>
      <div className="glass p-5 sm:p-7">
        <h2 className="font-bold">Create Subject</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-4">
          <input value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} placeholder="Code (CS101)" className="field" />
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Subject name" className="field sm:col-span-2" />
          <input value={section} onChange={(e) => setSection(e.target.value)} placeholder="Section" className="field" />
        </div>
        {error && <p className="mt-3 text-sm text-rose-300">{error}</p>}
        <button onClick={handleCreate} disabled={!code.trim() || !name.trim()} className="btn-primary mt-4 disabled:opacity-50">
          Create
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {subjects.map((s) => (
          <div key={s.subject_id} className="glass feature-card p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-xs font-semibold tracking-widest text-[var(--ink-faint)]">{s.subject_code}</div>
                <div className="mt-1 font-bold">{s.name}</div>
                <div className="mt-1 text-sm text-[var(--ink-dim)]">{s.total_students} students</div>
              </div>
            </div>
            <div className="mt-4 flex items-center justify-between gap-3 rounded-xl border border-white/10 bg-white/5 px-3 py-2">
              <span className="font-mono text-sm tracking-widest text-[var(--accent-soft)]">{s.join_code}</span>
              <button
                onClick={() => { navigator.clipboard.writeText(s.join_code); setCopied(s.subject_id); setTimeout(() => setCopied(null), 1500); }}
                className="text-xs text-[var(--ink-dim)] transition hover:text-white"
              >
                {copied === s.subject_id ? "Copied!" : "Copy code"}
              </button>
            </div>
          </div>
        ))}
        {subjects.length === 0 && (
          <p className="text-sm text-[var(--ink-dim)]">No subjects yet — create your first one above.</p>
        )}
      </div>
    </div>
  );
}

/* ---------------------------- Take Attendance ---------------------------- */

function TakeAttendance() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [photos, setPhotos] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<AttendanceMarkResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    listTeacherSubjects()
      .then((subs) => {
        setSubjects(subs);
        if (subs.length && selected === null) setSelected(subs[0].subject_id);
      })
      .catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handlePhotos(files: FileList | null) {
    if (!files) return;
    const b64s: string[] = [];
    for (const f of Array.from(files)) b64s.push(await fileToBase64(f));
    setPhotos((p) => [...p, ...b64s]);
  }

  async function runAttendance() {
    if (selected === null || photos.length === 0) return;
    setError(null);
    setResult(null);
    setBusy(true);
    try {
      const session = await createSession(selected, "face");
      const mark = await submitFaceAttendance(session.session_id, photos);
      setResult(mark);
      setPhotos([]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Attendance failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="glass p-5 sm:p-7">
      <h2 className="font-bold">Take Attendance — Face AI</h2>

      {subjects.length === 0 ? (
        <p className="mt-3 text-sm text-[var(--ink-dim)]">Create a subject first (Subjects tab).</p>
      ) : (
        <>
          <select
            value={selected ?? ""}
            onChange={(e) => setSelected(Number(e.target.value))}
            className="field mt-4"
          >
            {subjects.map((s) => (
              <option key={s.subject_id} value={s.subject_id}>
                {s.name} ({s.subject_code}) — {s.total_students} students
              </option>
            ))}
          </select>

          <div
            onClick={() => fileRef.current?.click()}
            className="mt-4 cursor-pointer rounded-xl border border-dashed border-white/20 bg-white/[0.03] p-8 text-center transition hover:border-[var(--accent)]/50"
          >
            <p className="text-sm text-[var(--ink-dim)]">
              {photos.length ? `${photos.length} photo(s) ready` : "Click to add classroom photos"}
            </p>
            <input
              ref={fileRef}
              type="file"
              accept="image/*"
              multiple
              capture="environment"
              className="hidden"
              onChange={(e) => handlePhotos(e.target.files)}
            />
          </div>

          {photos.length > 0 && (
            <div className="mt-4 grid grid-cols-4 gap-2 sm:grid-cols-6">
              {photos.map((p, i) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img key={i} src={`data:image/jpeg;base64,${p}`} alt={`Photo ${i + 1}`} className="aspect-square w-full rounded-lg object-cover" />
              ))}
            </div>
          )}

          {error && <p className="mt-4 text-sm text-rose-300">{error}</p>}

          <button onClick={runAttendance} disabled={busy || photos.length === 0} className="btn-primary mt-4 disabled:opacity-50">
            {busy ? "Running AI analysis…" : "Run Face Attendance"}
          </button>

          {result && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6">
              <div className="flex items-center gap-3">
                <span className="text-gradient text-2xl font-black">{result.present_count}/{result.total_students}</span>
                <span className="text-sm text-[var(--ink-dim)]">present</span>
              </div>
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                {result.entries.map((e) => (
                  <div key={e.student_id} className="flex items-center justify-between rounded-lg border border-white/10 px-3 py-2 text-sm">
                    <span>{e.name}</span>
                    <span className={e.is_present ? "text-emerald-300" : "text-rose-300"}>
                      {e.is_present ? "Present" : "Absent"}
                    </span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </>
      )}
    </div>
  );
}

/* -------------------------------- Records -------------------------------- */

function Records() {
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    teacherRecords().then(setRecords).catch(() => {});
  }, []);

  async function handleExport() {
    setExporting(true);
    try {
      const tokens = getStoredTokens();
      const res = await fetch(attendanceCsvUrl(), {
        headers: tokens?.access_token
          ? { Authorization: `Bearer ${tokens.access_token}` }
          : undefined,
      });
      if (!res.ok) throw new Error(`Export failed (${res.status})`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "attendance_records.csv";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("Could not export CSV — please log in again.");
    } finally {
      setExporting(false);
    }
  }

  const sessions = new Map<number, AttendanceRecord[]>();
  for (const r of records) {
    const list = sessions.get(r.session_id) ?? [];
    list.push(r);
    sessions.set(r.session_id, list);
  }

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="font-bold">Attendance Records</h2>
        <button onClick={handleExport} disabled={exporting} className="btn-ghost !py-2 text-sm">
          {exporting ? "Exporting…" : "Export CSV"}
        </button>
      </div>

      {sessions.size === 0 ? (
        <p className="mt-3 text-sm text-[var(--ink-dim)]">No records yet.</p>
      ) : (
        <div className="mt-4 space-y-4">
          {Array.from(sessions.entries()).map(([sessionId, entries]) => {
            const present = entries.filter((e) => e.is_present).length;
            const first = entries[0];
            return (
              <div key={sessionId} className="glass p-5">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <span className="font-bold">{first.subject_name}</span>
                    <span className="ml-2 text-xs text-[var(--ink-faint)]">{first.subject_code}</span>
                  </div>
                  <div className="text-sm text-[var(--ink-dim)]">
                    {new Date(first.started_at).toLocaleString()} · <span className="text-gradient font-bold">{present}/{entries.length}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
