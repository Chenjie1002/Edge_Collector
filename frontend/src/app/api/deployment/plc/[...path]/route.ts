import { NextRequest, NextResponse } from "next/server";

import { resolveDeploymentApiOrigin } from "../../../../../lib/deploymentPlc/apiOrigin";

type RouteContext = { params: Promise<{ path: string[] }> };

function isAllowedPath(method: string, path: string[]): boolean {
  if (method === "GET") {
    return path.length === 1 && (path[0] === "active" || path[0] === "line-options") ||
      path.length === 2 && path[0] === "candidates" && /^[A-Za-z0-9_-]{1,64}$/.test(path[1]);
  }
  return method === "POST" && (
    path.length === 1 && ["validate", "test-connection", "candidates"].includes(path[0]) ||
    path.length === 3 && path[0] === "candidates" && path[2] === "activate" && /^[A-Za-z0-9_-]{1,64}$/.test(path[1]) ||
    path.length === 3 && path[0] === "activations" && path[2] === "rollback" && /^[A-Za-z0-9_-]{1,64}$/.test(path[1])
  );
}

async function proxy(request: NextRequest, context: RouteContext): Promise<NextResponse> {
  const { path } = await context.params;
  if (!isAllowedPath(request.method, path)) return NextResponse.json({ detail: "Not found" }, { status: 404 });

  const origin = resolveDeploymentApiOrigin();
  if (!origin.ok) return NextResponse.json({ detail: "Deployment API is not configured." }, { status: 503 });

  const upstream = new URL(`/api/v2/deployment/plc/${path.join("/")}`, origin.origin);
  const headers = new Headers();
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);
  const response = await fetch(upstream, {
    method: request.method,
    headers,
    body: request.method === "POST" ? await request.text() : undefined,
    cache: "no-store"
  });
  return new NextResponse(response.body, {
    status: response.status,
    headers: { "content-type": response.headers.get("content-type") ?? "application/json" }
  });
}

export async function GET(request: NextRequest, context: RouteContext) {
  return proxy(request, context);
}

export async function POST(request: NextRequest, context: RouteContext) {
  return proxy(request, context);
}
