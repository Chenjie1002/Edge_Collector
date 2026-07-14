export type AcceptedEventsApiOriginEnvironment = Readonly<{
  EDGE_MES_DASHBOARD_API_ORIGIN?: string;
  EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE?: string;
}>;

declare const trustedAcceptedEventsApiOriginBrand: unique symbol;

export type TrustedAcceptedEventsApiOrigin = string & {
  readonly [trustedAcceptedEventsApiOriginBrand]: "TrustedAcceptedEventsApiOrigin";
};

export type OriginConfigurationErrorCode =
  | "ORIGIN_MISSING"
  | "PROFILE_MISSING"
  | "ORIGIN_EMPTY"
  | "PROFILE_EMPTY"
  | "PROFILE_UNSUPPORTED"
  | "ORIGIN_NON_CANONICAL"
  | "ORIGIN_PROFILE_MISMATCH"
  | "ORIGIN_MALFORMED";

export type AcceptedEventsApiOriginResolution =
  | { readonly ok: true; readonly origin: TrustedAcceptedEventsApiOrigin }
  | {
      readonly ok: false;
      readonly code: OriginConfigurationErrorCode;
      readonly message: "Accepted events service is not configured.";
    };

type AcceptedEventsApiOriginProfile = "local" | "container" | "production";

const safeFailureMessage = "Accepted events service is not configured." as const;
const attemptedLogCodes = new Set<OriginConfigurationErrorCode>();
const localOrigins = new Set([
  "http://127.0.0.1:8000",
  "http://127.0.0.1:3100",
  "http://localhost:8000",
  "http://localhost:3100",
  "http://[::1]:8000",
  "http://[::1]:3100"
]);
const productionHostname = /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$/;
const productionIpLikeLabel = /^(?:0x[0-9a-f]+|0[0-7]*|[0-9]+)$/;

function isKnownProfile(profile: string): profile is AcceptedEventsApiOriginProfile {
  return profile === "local" || profile === "container" || profile === "production";
}

function isProductionIpLikeHostname(hostname: string): boolean {
  if (hostname.startsWith("[") && hostname.endsWith("]")) return true;

  const labels = hostname.split(".");
  return labels.length >= 2 && labels.length <= 4 && labels.every((label) => productionIpLikeLabel.test(label));
}

function hasProductionRawSyntax(origin: string): boolean {
  if (!origin.startsWith("https://") || origin.endsWith("//")) return false;
  const authorityAndPath = origin.slice("https://".length);
  const hostname = authorityAndPath.endsWith("/") ? authorityAndPath.slice(0, -1) : authorityAndPath;
  if (hostname.length > 253 || hostname !== authorityAndPath && authorityAndPath !== `${hostname}/`) return false;
  if (isProductionIpLikeHostname(hostname)) return false;
  return productionHostname.test(hostname);
}

function hasRawSyntaxForProfile(origin: string, profile: AcceptedEventsApiOriginProfile): boolean {
  if (profile === "local") {
    const withoutOptionalRootSlash = origin.endsWith("/") ? origin.slice(0, -1) : origin;
    return localOrigins.has(withoutOptionalRootSlash) && (origin === withoutOptionalRootSlash || origin === `${withoutOptionalRootSlash}/`);
  }
  if (profile === "container") return origin === "http://api:8000" || origin === "http://api:8000/";
  return hasProductionRawSyntax(origin);
}

function hasAnyKnownRawSyntax(origin: string): boolean {
  return (
    hasRawSyntaxForProfile(origin, "local") ||
    hasRawSyntaxForProfile(origin, "container") ||
    hasRawSyntaxForProfile(origin, "production")
  );
}

function hasExpectedParsedComponents(url: URL, profile: AcceptedEventsApiOriginProfile, rawOrigin: string): boolean {
  if (
    url.pathname !== "/" ||
    url.username !== "" ||
    url.password !== "" ||
    url.search !== "" ||
    url.hash !== "" ||
    url.origin !== rawOrigin.replace(/\/$/, "")
  ) {
    return false;
  }

  if (profile === "local") {
    return url.protocol === "http:" && localOrigins.has(url.origin) && url.port !== "";
  }
  if (profile === "container") {
    return url.protocol === "http:" && url.hostname === "api" && url.port === "8000" && url.origin === "http://api:8000";
  }
  return url.protocol === "https:" && url.port === "" && productionHostname.test(url.hostname) && url.origin === `https://${url.hostname}`;
}

function logConfigurationFailure(code: OriginConfigurationErrorCode) {
  if (attemptedLogCodes.has(code)) return;
  attemptedLogCodes.add(code);
  try {
    console.error("DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR", code);
  } catch {
    // Configuration logging must never change the safe resolver result.
  }
}

function failure(code: OriginConfigurationErrorCode): AcceptedEventsApiOriginResolution {
  logConfigurationFailure(code);
  return { ok: false, code, message: safeFailureMessage };
}

export function resolveTrustedAcceptedEventsApiOrigin(
  environment?: AcceptedEventsApiOriginEnvironment
): AcceptedEventsApiOriginResolution {
  const source = environment ?? process.env;
  const snapshot = {
    origin: source.EDGE_MES_DASHBOARD_API_ORIGIN,
    profile: source.EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE
  } as const;

  if (snapshot.origin === undefined) return failure("ORIGIN_MISSING");
  if (snapshot.profile === undefined) return failure("PROFILE_MISSING");
  if (snapshot.origin === "") return failure("ORIGIN_EMPTY");
  if (snapshot.profile === "") return failure("PROFILE_EMPTY");
  if (!isKnownProfile(snapshot.profile)) return failure("PROFILE_UNSUPPORTED");

  if (!hasRawSyntaxForProfile(snapshot.origin, snapshot.profile)) {
    return failure(hasAnyKnownRawSyntax(snapshot.origin) ? "ORIGIN_PROFILE_MISMATCH" : "ORIGIN_NON_CANONICAL");
  }

  let parsedUrl: URL;
  try {
    parsedUrl = new URL(snapshot.origin);
  } catch {
    return failure("ORIGIN_MALFORMED");
  }

  if (!hasExpectedParsedComponents(parsedUrl, snapshot.profile, snapshot.origin)) {
    return failure("ORIGIN_PROFILE_MISMATCH");
  }

  return { ok: true, origin: parsedUrl.origin as TrustedAcceptedEventsApiOrigin };
}
