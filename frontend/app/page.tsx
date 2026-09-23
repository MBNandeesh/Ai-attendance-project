"use client";

import Link from "next/link";
import dynamic from "next/dynamic";
import { motion } from "framer-motion";
import { useReveal, useCardGlow } from "@/components/use-reveal";

const BackgroundCanvas = dynamic(() => import("@/components/background-canvas"), { ssr: false });

/* ---------- inline SVG icons (stroke style, no emoji) ---------- */
const IconFace = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
    <path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2" />
    <circle cx="9" cy="10" r="1" /><circle cx="15" cy="10" r="1" />
    <path d="M9 15c.9.7 2 1 3 1s2.1-.3 3-1" />
  </svg>
);
const IconWave = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" className="h-5 w-5">
    <path d="M12 3v18M8 7v10M16 7v10M4 10v4M20 10v4" />
  </svg>
);
const IconShield = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
    <path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z" />
    <path d="M9.5 12l2 2 3.5-4" />
  </svg>
);
const IconChart = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" className="h-5 w-5">
    <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
  </svg>
);
const IconLock = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
    <rect x="5" y="11" width="14" height="9" rx="2" />
    <path d="M8 11V8a4 4 0 0 1 8 0v3" />
  </svg>
);
const IconDevices = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
    <rect x="3" y="5" width="13" height="10" rx="1.5" />
    <rect x="17" y="9" width="4" height="9" rx="1" />
    <path d="M7 19h5" />
  </svg>
);

const FEATURES = [
  {
    icon: <IconFace />,
    title: "Face Recognition",
    copy: "Passwordless login and attendance from 128-dimension dlib embeddings. No cards, no queues, no proxy attendance.",
  },
  {
    icon: <IconWave />,
    title: "Voice Attendance",
    copy: "Bulk classroom audio is segmented and identified per speaker with Resemblyzer voice embeddings.",
  },
  {
    icon: <IconShield />,
    title: "Liveness Detection",
    copy: "Blink dynamics and randomized head-pose challenges render photo and screen spoofing ineffective.",
  },
  {
    icon: <IconChart />,
    title: "Analytics & Reports",
    copy: "Live sessions, per-subject trends, defaulter lists and one-click PDF or CSV exports for records.",
  },
  {
    icon: <IconLock />,
    title: "Secure by Design",
    copy: "JWT authentication with refresh rotation, bcrypt credentials, and a fully audited override trail.",
  },
  {
    icon: <IconDevices />,
    title: "Runs on Anything",
    copy: "A browser and a webcam are the only requirements — responsive on laptops, tablets and phones.",
  },
];

const STATS = [
  { value: "< 2s", label: "per recognition" },
  { value: "128-D", label: "face descriptors" },
  { value: "2", label: "biometric modalities" },
  { value: "0", label: "photos accepted (W5)" },
];

const STEPS = [
  { n: "01", t: "Capture", d: "The student looks into the webcam. Thirty to sixty frames are captured in seconds." },
  { n: "02", t: "Verify liveness", d: "A blink is detected and a random head-turn challenge is issued. Photos fail here." },
  { n: "03", t: "Recognise", d: "The face embedding is matched against enrolled classmates in milliseconds." },
  { n: "04", t: "Confirm", d: "The teacher reviews the session, overrides if needed, and saves the record." },
];

const MARQUEE = [
  "Face ID Login", "Voice Roll-Call", "Liveness Challenge", "QR Join Codes",
  "Session Dedup", "Audit Trail", "PDF Reports", "Live Analytics",
];

function Reveal({ children, className = "", delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  const ref = useReveal<HTMLDivElement>();
  return (
    <div ref={ref} className={`reveal ${className}`} style={{ animationDelay: `${delay}s` }}>
      {children}
    </div>
  );
}

function FeatureCard({ icon, title, copy }: { icon: React.ReactNode; title: string; copy: string }) {
  const ref = useCardGlow();
  return (
    <div ref={ref} className="feature-card glass relative overflow-hidden p-7">
      <div className="card-glow" />
      <div className="icon-tile">{icon}</div>
      <h3 className="mt-5 text-[15px] font-semibold tracking-tight text-white">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-[var(--ink-dim)]">{copy}</p>
    </div>
  );
}

export default function LandingPage() {
  return (
    <main className="relative">
      <div className="bg-layers" aria-hidden>
        <div className="bg-base" />
        <div className="bg-aurora" />
      </div>
      <BackgroundCanvas />
      <div className="bg-grain" aria-hidden />

      {/* ============================= NAV ============================= */}
      <nav className="fixed inset-x-0 top-0 z-50 border-b border-white/[0.06] bg-[rgba(5,7,13,0.65)] backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="grid h-8 w-8 place-items-center rounded-[10px] bg-gradient-to-b from-[#6d8bff] to-[#4a63d8] shadow-lg shadow-indigo-950">
              <IconFace />
            </div>
            <span className="text-[15px] font-semibold tracking-tight">AI Attendance</span>
          </Link>
          <div className="hidden items-center gap-8 text-sm text-[var(--ink-dim)] md:flex">
            <a href="#features" className="transition hover:text-white">Features</a>
            <a href="#metrics" className="transition hover:text-white">Metrics</a>
            <a href="#how" className="transition hover:text-white">How it works</a>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/student" className="btn-ghost !px-4 !py-2 text-sm">
              Student Portal
            </Link>
            <Link href="/login" className="btn-primary !px-4 !py-2 text-sm">
              Teacher Portal
            </Link>
          </div>
        </div>
      </nav>

      {/* ============================ HERO ============================ */}
      <section className="relative flex min-h-[100svh] flex-col items-center justify-center px-6 pt-16 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          className="eyebrow"
        >
          <span className="pulse-dot" />
          FACE + VOICE + LIVENESS
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 26 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.08, ease: [0.16, 1, 0.3, 1] }}
          className="mt-7 max-w-3xl text-balance text-5xl font-semibold leading-[1.06] tracking-[-0.03em] sm:text-6xl md:text-[76px]"
        >
          Attendance that
          <br />
          <span className="text-gradient">marks itself.</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 26 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.18, ease: [0.16, 1, 0.3, 1] }}
          className="mx-auto mt-6 max-w-xl text-pretty text-lg leading-relaxed text-[var(--ink-dim)]"
        >
          A passwordless classroom attendance platform. Faces are recognised, voices are
          verified — and photographs can&apos;t fake it.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 26 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.28, ease: [0.16, 1, 0.3, 1] }}
          className="mt-9 flex flex-wrap items-center justify-center gap-3.5"
        >
          <Link href="/student" className="btn-ghost">Student Face ID Login</Link>
          <Link href="/login" className="btn-primary">
            Launch Teacher Portal
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </Link>
          <a href="#how" className="btn-ghost">See how it works</a>
        </motion.div>

        {/* product screenshot frame */}
        <motion.div
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.45, ease: [0.16, 1, 0.3, 1] }}
          className="mt-16 w-full max-w-5xl"
        >
          <div className="glass overflow-hidden rounded-2xl p-1.5 shadow-[0_40px_120px_rgba(0,0,0,0.5)]">
            <div className="flex items-center gap-1.5 px-3 py-2">
              <span className="h-2.5 w-2.5 rounded-full bg-[#2a3147]" />
              <span className="h-2.5 w-2.5 rounded-full bg-[#2a3147]" />
              <span className="h-2.5 w-2.5 rounded-full bg-[#2a3147]" />
              <span className="ml-3 text-xs text-[var(--ink-faint)]">app.aiattendance.dev / dashboard</span>
            </div>
            <div className="rounded-xl border border-white/[0.05] bg-[var(--abyss)] p-6">
              <div className="grid grid-cols-3 gap-4">
                {[["Class attendance", "92%", "w-[92%]"], ["Sessions this week", "14", "w-[58%]"], ["Defaulters", "3", "w-[24%]"]].map(
                  ([label, value, bar]) => (
                    <div key={label} className="rounded-lg border border-white/[0.05] bg-white/[0.02] p-4 text-left">
                      <div className="text-xs text-[var(--ink-faint)]">{label}</div>
                      <div className="mt-1 text-2xl font-semibold tracking-tight">{value}</div>
                      <div className="mt-3 h-1 overflow-hidden rounded-full bg-white/[0.06]">
                        <div className={`h-full rounded-full bg-gradient-to-r from-[#5b7cfa] to-[#4cc9f0] ${bar}`} />
                      </div>
                    </div>
                  ),
                )}
              </div>
              <div className="mt-4 space-y-2">
                {[
                  ["Ananya S.", "Present · face", "text-[var(--mint)]"],
                  ["Rohan K.", "Present · voice", "text-[var(--mint)]"],
                  ["Meghna T.", "Absent", "text-[var(--ink-faint)]"],
                ].map(([name, status, color], i) => (
                  <motion.div
                    key={name}
                    initial={{ opacity: 0, x: -14 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.9 + i * 0.18, duration: 0.5 }}
                    className="flex items-center justify-between rounded-lg border border-white/[0.04] bg-white/[0.015] px-4 py-2.5 text-sm"
                  >
                    <span className="text-[var(--ink-dim)]">{name}</span>
                    <span className={`text-xs font-medium ${color}`}>{status}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* ========================== MARQUEE =========================== */}
      <section className="marquee-mask border-y border-white/[0.05] py-5">
        <div className="marquee-track">
          {[...MARQUEE, ...MARQUEE].map((item, i) => (
            <span key={i} className="flex items-center gap-3 whitespace-nowrap text-[13px] font-medium tracking-wide text-[var(--ink-faint)]">
              <span className="h-1 w-1 rounded-full bg-[#4cc9f0]" />
              {item}
            </span>
          ))}
        </div>
      </section>

      {/* ========================== FEATURES ========================== */}
      <section id="features" className="mx-auto max-w-6xl px-6 py-28">
        <Reveal>
          <p className="eyebrow">CAPABILITIES</p>
          <h2 className="mt-5 max-w-xl text-balance text-4xl font-semibold tracking-[-0.02em] sm:text-[44px] sm:leading-[1.1]">
            Everything a classroom needs. Nothing it doesn&apos;t.
          </h2>
        </Reveal>

        <div className="mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f, i) => (
            <Reveal key={f.title} delay={i * 0.07}>
              <FeatureCard {...f} />
            </Reveal>
          ))}
        </div>
      </section>

      {/* =========================== STATS ============================ */}
      <section id="metrics" className="mx-auto max-w-6xl px-6 pb-28">
        <Reveal>
          <div className="glass grid grid-cols-2 gap-px overflow-hidden rounded-2xl lg:grid-cols-4">
            {STATS.map((s) => (
              <div key={s.label} className="bg-white/[0.015] px-6 py-10 text-center transition hover:bg-white/[0.04]">
                <div className="text-gradient text-4xl font-semibold tracking-tight">{s.value}</div>
                <div className="mt-2 text-sm text-[var(--ink-dim)]">{s.label}</div>
              </div>
            ))}
          </div>
        </Reveal>
      </section>

      {/* ========================== PIPELINE ========================== */}
      <section id="how" className="mx-auto max-w-6xl px-6 pb-28">
        <Reveal>
          <p className="eyebrow">HOW IT WORKS</p>
          <h2 className="mt-5 max-w-xl text-balance text-4xl font-semibold tracking-[-0.02em] sm:text-[44px] sm:leading-[1.1]">
            From camera to confirmed, in four steps.
          </h2>
        </Reveal>

        <div className="mt-14 grid gap-4 md:grid-cols-4">
          {STEPS.map((step, i) => (
            <Reveal key={step.n} delay={i * 0.09}>
              <div className="group relative h-full rounded-2xl border border-white/[0.06] bg-white/[0.02] p-7 transition duration-300 hover:border-[rgba(91,124,250,0.4)] hover:bg-white/[0.045]">
                <div className="font-mono text-xs text-[#4cc9f0]">{step.n}</div>
                <h3 className="mt-4 text-[15px] font-semibold">{step.t}</h3>
                <p className="mt-2 text-sm leading-relaxed text-[var(--ink-dim)]">{step.d}</p>
                {i < 3 && (
                  <div className="absolute -right-2.5 top-1/2 hidden h-5 w-5 -translate-y-1/2 place-items-center rounded-full border border-white/10 bg-[var(--void)] text-[10px] text-[var(--ink-faint)] md:grid">
                    →
                  </div>
                )}
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ============================ CTA ============================= */}
      <section className="mx-auto max-w-6xl px-6 pb-32">
        <Reveal>
          <div className="glass relative overflow-hidden px-8 py-16 text-center sm:py-20">
            <div
              className="pointer-events-none absolute inset-0"
              style={{ background: "radial-gradient(640px circle at 50% 130%, rgba(91,124,250,0.18), transparent 60%)" }}
            />
            <h2 className="relative mx-auto max-w-lg text-balance text-4xl font-semibold tracking-[-0.02em] sm:text-[44px]">
              Never take roll call again.
            </h2>
            <p className="relative mx-auto mt-4 max-w-md text-[var(--ink-dim)]">
              Create a teacher account, share a join code, and let the AI handle attendance.
            </p>
            <div className="relative mt-9">
              <Link href="/login" className="btn-primary">Get started — it&apos;s free</Link>
            </div>
          </div>
        </Reveal>
      </section>

      {/* =========================== FOOTER =========================== */}
      <footer className="border-t border-white/[0.05] py-10">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 text-sm text-[var(--ink-faint)] sm:flex-row">
          <span>© 2026 AI Attendance System — Major Project</span>
          <span>Next.js · FastAPI · dlib · Resemblyzer</span>
        </div>
      </footer>
    </main>
  );
}
