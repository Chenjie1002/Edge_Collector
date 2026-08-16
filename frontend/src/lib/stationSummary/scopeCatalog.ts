export type ScopeStation = Readonly<{
  stationId: string;
  name: string;
  stationOrder: number;
}>;

export type ScopeLine = Readonly<{
  lineId: string;
  name: string;
  stations: readonly ScopeStation[];
}>;

export type TrustedScopeCatalog = Readonly<{
  contractVersion: "production-scope-options/v1";
  timezone: "Asia/Shanghai";
  utcOffset: "+08:00";
  lines: readonly ScopeLine[];
}>;

export type ScopeCatalogResult =
  | { ok: true; catalog: TrustedScopeCatalog }
  | { ok: false; kind: "unavailable" | "invalid-response"; message: string };

const SCOPE_CATALOG_MESSAGE = "Scope catalog unavailable";

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function exactKeys(value: Record<string, unknown>, required: readonly string[], label: string): void {
  const allowed = new Set(required);
  if (Object.keys(value).some((key) => !allowed.has(key))) throw new Error(`invalid ${label}`);
  if (required.some((key) => !Object.prototype.hasOwnProperty.call(value, key))) throw new Error(`invalid ${label}`);
}

function nonBlankString(value: unknown, label: string): string {
  if (typeof value !== "string" || value.trim() === "") throw new Error(`invalid ${label}`);
  return value;
}

function positiveSafeInteger(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value <= 0) throw new Error(`invalid ${label}`);
  return value;
}

function parseCatalog(value: unknown): TrustedScopeCatalog {
  if (!isPlainObject(value)) throw new Error("invalid scope catalog");
  exactKeys(value, ["contract_version", "authority", "timezone", "utc_offset", "lines"], "scope catalog");
  if (value.contract_version !== "production-scope-options/v1") throw new Error("invalid scope catalog contract");
  if (value.timezone !== "Asia/Shanghai" || value.utc_offset !== "+08:00") throw new Error("invalid scope catalog timezone");

  if (!isPlainObject(value.authority)) throw new Error("invalid scope catalog authority");
  exactKeys(value.authority, ["kind", "source", "config_version", "content_sha256"], "scope catalog authority");
  if (
    value.authority.kind !== "active_runtime_mapping" ||
    !["config/mapping.yaml", "active/mapping.yaml"].includes(String(value.authority.source))
  ) {
    throw new Error("invalid scope catalog authority source");
  }
  const configVersion = nonBlankString(value.authority.config_version, "scope catalog config_version");
  const contentSha256 = nonBlankString(value.authority.content_sha256, "scope catalog content_sha256");
  if (!/^sha256:[0-9a-f]{64}$/.test(contentSha256)) throw new Error("invalid scope catalog content_sha256");

  if (!Array.isArray(value.lines) || value.lines.length === 0) throw new Error("invalid scope catalog lines");
  const lineIds = new Set<string>();
  const lines: ScopeLine[] = value.lines.map((rawLine, lineIndex) => {
    if (!isPlainObject(rawLine)) throw new Error(`invalid scope line ${lineIndex}`);
    exactKeys(rawLine, ["line_id", "name", "stations"], `scope line ${lineIndex}`);
    const lineId = nonBlankString(rawLine.line_id, `scope line ${lineIndex}.line_id`);
    const lineName = nonBlankString(rawLine.name, `scope line ${lineIndex}.name`);
    if (lineIds.has(lineId)) throw new Error("duplicate scope line");
    lineIds.add(lineId);
    if (!Array.isArray(rawLine.stations) || rawLine.stations.length === 0) throw new Error("invalid scope stations");

    const stationIds = new Set<string>();
    let previousStationOrder = 0;
    const stations: ScopeStation[] = rawLine.stations.map((rawStation, stationIndex) => {
      if (!isPlainObject(rawStation)) throw new Error(`invalid scope station ${stationIndex}`);
      exactKeys(rawStation, ["station_id", "name", "station_order"], `scope station ${stationIndex}`);
      const stationId = nonBlankString(rawStation.station_id, `scope station ${stationIndex}.station_id`);
      const stationName = nonBlankString(rawStation.name, `scope station ${stationIndex}.name`);
      const stationOrder = positiveSafeInteger(rawStation.station_order, `scope station ${stationIndex}.station_order`);
      if (stationIds.has(stationId) || stationOrder <= previousStationOrder) throw new Error("invalid scope station order");
      stationIds.add(stationId);
      previousStationOrder = stationOrder;
      return { stationId, name: stationName, stationOrder };
    });

    return { lineId, name: lineName, stations };
  });

  return {
    contractVersion: "production-scope-options/v1",
    timezone: "Asia/Shanghai",
    utcOffset: "+08:00",
    lines,
  };
}

export async function fetchTrustedScopeCatalog(
  trustedApiOrigin: string | URL,
  fetchImpl: typeof fetch = fetch,
): Promise<ScopeCatalogResult> {
  try {
    const endpoint = new URL("/api/v2/production/scope-options", trustedApiOrigin);
    const response = await fetchImpl(endpoint, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      redirect: "error",
    });
    if (!response.ok) return { ok: false, kind: "unavailable", message: SCOPE_CATALOG_MESSAGE };
    const payload: unknown = JSON.parse(await response.text());
    return { ok: true, catalog: parseCatalog(payload) };
  } catch {
    return { ok: false, kind: "invalid-response", message: SCOPE_CATALOG_MESSAGE };
  }
}
