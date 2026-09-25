/**
 * Typed API client — extended for students, attendance, liveness.
 */

/**
 * Resilient API base resolution.
 *
 * Strategy:
 * 1. Probe same-origin `/api/health` — when the same-origin proxy (Vercel
 *    route handler / rewrites) is active, this returns JSON and we use
 *    relative URLs for everything (no CORS involved).
 * 2. Otherwise, fall back to calling the backend directly using the
 *    NEXT_PUBLIC_API_URL env var (requires CORS_ORIGINS on the backend).
 *
 * The probe runs once per page load and the result is cached.
 */
let apiBasePromise: Promise<string> | null = null;

async function probeApiBase(): Promise<string> {
  try {
    const res = await fetch("/api/health", { cache: "no-store" });
    const ct = res.headers.get("content-type") ?? "";
    if (res.ok && ct.includes("application/json")) {
      const body = (await res.json()) as { status?: string };
      if (body.status === "ok") return ""; // same-origin proxy works
    }
  } catch {
    // probe failed — try direct fallback below
  }
  const direct = process.env.NEXT_PUBLIC_API_URL;
  if (direct) return direct.replace(/\/$/, "");
  return ""; // no fallback configured; same-origin requests will surface errors
}

export function getApiBase(): Promise<string> {
  if (!apiBasePromise) apiBasePromise = probeApiBase();
  return apiBasePromise;
}

export type TokenPair = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

export type AuthResult = TokenPair & {
  role: string;
  user_id: number;
  name: string;
};

export type Me = {
  user_id: number;
  role: string;
  name: string;
};

export type Subject = {
  subject_id: number;
  subject_code: string;
  name: string;
  section: string;
  join_code: string;
  total_students: number;
};

export type AttendanceEntry = {
  student_id: number;
  name: string;
  is_present: boolean;
  method: string | null;
};

export type AttendanceMarkResult = {
  session_id: number;
  total_students: number;
  present_count: number;
  entries: AttendanceEntry[];
};

export type AttendanceRecord = {
  attendance_id: number;
  session_id: number;
  subject_id: number;
  subject_name: string;
  subject_code: string;
  student_id: number;
  student_name: string;
  is_present: boolean;
  method: string;
  started_at: string;
};

export type LivenessChallenge = {
  session_token: string;
  challenge: string;
  instruction: string;
};

export type LivenessResult = {
  passed: boolean;
  score: number;
  reason: string;
  blink_detected: boolean;
  pose_verified: boolean;
};

const STORAGE_KEY = "ai-attendance.tokens";
const ROLE_KEY = "ai-attendance.role";

type StoredTokens = { access_token: string; refresh_token: string };

export function getStoredTokens(): StoredTokens | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as StoredTokens) : null;
  } catch {
    return null;
  }
}

export function storeSession(auth: AuthResult): void {
  window.localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ access_token: auth.access_token, refresh_token: auth.refresh_token })
  );
  window.localStorage.setItem(ROLE_KEY, auth.role);
}

export function getStoredRole(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(ROLE_KEY);
}

export function clearTokens(): void {
  window.localStorage.removeItem(STORAGE_KEY);
  window.localStorage.removeItem(ROLE_KEY);
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

function refreshPath(role: string | null): string {
  return role === "student"
    ? "/api/v1/auth/student/refresh"
    : "/api/v1/auth/teacher/refresh";
}

async function refreshAccessToken(): Promise<boolean> {
  const tokens = getStoredTokens();
  if (!tokens?.refresh_token) return false;

  const base = await getApiBase();
  const res = await fetch(`${base}${refreshPath(getStoredRole())}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: tokens.refresh_token }),
  });

  if (!res.ok) {
    clearTokens();
    return false;
  }

  const pair = (await res.json()) as TokenPair;
  window.localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ access_token: pair.access_token, refresh_token: pair.refresh_token })
  );
  return true;
}

export async function apiFetch<T>(path: string, init: RequestInit = {}, retry = true): Promise<T> {
  const tokens = getStoredTokens();
  const headers = new Headers(init.headers);
  if (tokens?.access_token) headers.set("Authorization", `Bearer ${tokens.access_token}`);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");

  const base = await getApiBase();
  const res = await fetch(`${base}${path}`, { ...init, headers });

  if (res.status === 401 && retry) {
    const refreshed = await refreshAccessToken();
    if (refreshed) return apiFetch<T>(path, init, false);
  }

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = (await res.json()) as { detail?: string };
      if (body.detail) detail = body.detail;
    } catch {
      // keep statusText
    }
    throw new ApiError(res.status, detail);
  }

  return (await res.json()) as T;
}

// ---------- Auth ----------

export function loginTeacher(username: string, password: string): Promise<AuthResult> {
  return apiFetch<AuthResult>("/api/v1/auth/teacher/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function registerTeacher(username: string, name: string, password: string): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/api/v1/auth/teacher/register", {
    method: "POST",
    body: JSON.stringify({ username, name, password }),
  });
}

export function faceLogin(faceImageB64: string): Promise<AuthResult> {
  return apiFetch<AuthResult>("/api/v1/students/face-login", {
    method: "POST",
    body: JSON.stringify({ face_image: faceImageB64 }),
  });
}

export function registerStudent(name: string, faceImageB64: string): Promise<AuthResult> {
  return apiFetch<AuthResult>("/api/v1/students/register", {
    method: "POST",
    body: JSON.stringify({ name, face_image: faceImageB64 }),
  });
}

export function fetchMe(role: string): Promise<Me> {
  return apiFetch<Me>(role === "student" ? "/api/v1/auth/student/me" : "/api/v1/auth/teacher/me");
}

// ---------- Subjects ----------

export function listTeacherSubjects(): Promise<Subject[]> {
  return apiFetch<Subject[]>("/api/v1/subjects");
}

export function createSubject(subject_code: string, name: string, section: string): Promise<Subject> {
  return apiFetch<Subject>("/api/v1/subjects", {
    method: "POST",
    body: JSON.stringify({ subject_code, name, section }),
  });
}

export function joinByCode(code: string): Promise<Subject> {
  return apiFetch<Subject>(`/api/v1/join/${encodeURIComponent(code.toUpperCase())}`, {
    method: "POST",
  });
}

export function mySubjects(): Promise<Subject[]> {
  return apiFetch<Subject[]>("/api/v1/auth/student/me/subjects");
}

// ---------- Attendance ----------

export function createSession(subjectId: number, method: string): Promise<{ session_id: number }> {
  return apiFetch<{ session_id: number }>("/api/v1/attendance/sessions", {
    method: "POST",
    body: JSON.stringify({ subject_id: subjectId, method }),
  });
}

export function submitFaceAttendance(
  sessionId: number,
  images: string[],
  livenessScore?: number
): Promise<AttendanceMarkResult> {
  return apiFetch<AttendanceMarkResult>("/api/v1/attendance/face", {
    method: "POST",
    body: JSON.stringify({ session_id: sessionId, images, liveness_score: livenessScore }),
  });
}

export function submitVoiceAttendance(sessionId: number, audioB64: string): Promise<AttendanceMarkResult> {
  return apiFetch<AttendanceMarkResult>("/api/v1/attendance/voice", {
    method: "POST",
    body: JSON.stringify({ session_id: sessionId, audio_base64: audioB64 }),
  });
}

export function teacherRecords(): Promise<AttendanceRecord[]> {
  return apiFetch<AttendanceRecord[]>("/api/v1/attendance/records");
}

export function studentRecords(): Promise<AttendanceRecord[]> {
  return apiFetch<AttendanceRecord[]>("/api/v1/attendance/me");
}

export function attendanceCsvUrl(): string {
  // Callers await getApiBase() when they need the absolute URL.
  return "/api/v1/attendance/records/export";
}

export async function attendanceCsvAbsoluteUrl(): Promise<string> {
  const base = await getApiBase();
  return `${base}/api/v1/attendance/records/export`;
}

// ---------- Liveness ----------

export function getLivenessChallenge(): Promise<LivenessChallenge> {
  return apiFetch<LivenessChallenge>("/api/v1/liveness/challenge");
}

export function verifyLiveness(sessionToken: string, frames: string[]): Promise<LivenessResult> {
  return apiFetch<LivenessResult>("/api/v1/liveness/verify", {
    method: "POST",
    body: JSON.stringify({ session_token: sessionToken, frames }),
  });
}

// ---------- Voice ----------

export function enrollVoice(audioB64: string): Promise<{ samples: number; message: string }> {
  return apiFetch<{ samples: number; message: string }>("/api/v1/voice/enroll", {
    method: "POST",
    body: JSON.stringify({ audio_base64: audioB64 }),
  });
}

// ---------- Helpers ----------

export function fileToBase64(file: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      resolve(result.includes(",") ? result.split(",")[1] : result);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
