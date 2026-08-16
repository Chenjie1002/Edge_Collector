import { NextRequest, NextResponse } from "next/server";
import { resolveTrustedAcceptedEventsApiOrigin } from "../../../../lib/acceptedStationEvents/apiOrigin";

type RouteContext = { params: Promise<{ path: string[] }> };

const ALLOWED_UPSTREAM_PATHS = new Set([
  "/api/v2/production/line-summary",
  "/api/v2/production/quality",
  "/api/v2/process-metrics",
]);

export async function GET(request: NextRequest, context: RouteContext): Promise<NextResponse> {
  const { path } = await context.params;
  const upstreamPath = `/api/v2/${path.join("/")}`;
  if (!ALLOWED_UPSTREAM_PATHS.has(upstreamPath)) {
    return NextResponse.json({ detail: "Not found" }, { status: 404 });
  }

  const origin = resolveTrustedAcceptedEventsApiOrigin();
  if (!origin.ok) {
    return NextResponse.json({ detail: "Station summary API is not configured." }, { status: 503 });
  }

  const upstream = new URL(upstreamPath, origin.origin);
  upstream.search = request.nextUrl.search;
  let response: Response;
  try {
    response = await fetch(upstream, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      redirect: "error",
    });
  } catch {
    return NextResponse.json({ detail: "Station summary source unavailable." }, { status: 503 });
  }

  return new NextResponse(response.body, {
    status: response.status,
    headers: {
      "cache-control": "no-store",
      "content-type": response.headers.get("content-type") ?? "application/json",
    },
  });
}
