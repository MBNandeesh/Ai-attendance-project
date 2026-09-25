import type { NextConfig } from "next";

/**
 * Same-origin API proxy.
 *
 * The browser always calls `/api/v1/...` on its own origin. In production
 * (Vercel) these requests are proxied to the FastAPI backend on Render via
 * the rewrites below — no CORS, no NEXT_PUBLIC_API_URL needed.
 * In local dev with no backend URL configured, they go to localhost:8000.
 */
const API_UPSTREAM =
  process.env.API_PROXY_URL ?? // server-only env var (Vercel), never exposed to the browser
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/v1/:path*", destination: `${API_UPSTREAM}/api/v1/:path*` },
      { source: "/api/health", destination: `${API_UPSTREAM}/api/health` },
      { source: "/api/health/:path*", destination: `${API_UPSTREAM}/api/health/:path*` },
      { source: "/api/docs", destination: `${API_UPSTREAM}/api/docs` },
      { source: "/api/openapi.json", destination: `${API_UPSTREAM}/api/openapi.json` },
    ];
  },
};

export default nextConfig;
