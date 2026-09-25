/**
 * Same-origin API proxy (catch-all).
 *
 * Every /api/* request to this site is forwarded server-side to the FastAPI
 * backend (Render). The browser never makes cross-origin calls, so no CORS
 * and no public backend URL are involved. Works even if next.config.ts
 * rewrites are ignored — this is real server code, not config.
 */

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const UPSTREAM =
  process.env.API_PROXY_URL ?? // server-only env var set in Vercel
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";

const HOP_BY_HOP = new Set([
  "host",
  "connection",
  "keep-alive",
  "transfer-encoding",
  "upgrade",
  "content-length", // fetch recomputes it
]);

async function proxy(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const upstreamUrl = `${UPSTREAM.replace(/\/$/, "")}${url.pathname}${url.search}`;

  const headers = new Headers();
  req.headers.forEach((value, key) => {
    if (!HOP_BY_HOP.has(key.toLowerCase())) headers.set(key, value);
  });

  const hasBody = req.method !== "GET" && req.method !== "HEAD";
  const body = hasBody ? await req.arrayBuffer() : undefined;

  let res: Response;
  try {
    res = await fetch(upstreamUrl, {
      method: req.method,
      headers,
      body,
      redirect: "manual",
    });
  } catch {
    return Response.json(
      { detail: "API upstream unreachable — check API_PROXY_URL on the server" },
      { status: 502 }
    );
  }

  const resHeaders = new Headers();
  res.headers.forEach((value, key) => {
    if (!HOP_BY_HOP.has(key.toLowerCase()) && key.toLowerCase() !== "content-encoding") {
      resHeaders.set(key, value);
    }
  });

  return new Response(res.body, { status: res.status, headers: resHeaders });
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
export const OPTIONS = proxy;
export const HEAD = proxy;
