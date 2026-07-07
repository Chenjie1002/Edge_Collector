import type { AcceptedStationEventItem, AcceptedStationEventsEnvelope } from "./schema";

export type TimestampDisplay = {
  label: "Event time" | "Accepted fact timestamp";
  value: string;
};

export type AcceptedEventRow = {
  factKey: string;
  lineId: string;
  stationId: string;
  stationType: string;
  eventType: string;
  productionResult: string;
  eventTs: TimestampDisplay;
  acceptedAt: TimestampDisplay;
  unitId: string | null;
  dmc: string | null;
};

export type PageSummary = {
  label: "Current page only";
  totalAcceptedFacts: number;
  byResult: Record<string, number>;
  byStation: Record<string, number>;
};

export type NokDetailEvidence = {
  productionResult: string;
  nokCode: string | null;
  nokOrigin: string | null;
  nokDetailCode: string | null;
  nokDetailSourceEventId: string | null;
  nokDetailEvidenceFactKey: string | null;
  factKey: string;
  sourceEventId: string;
};

export type TraceReference = {
  unitId: string | null;
  dmc: string | null;
  cycleCounter: number | null;
  sourceEventId: string;
  eventTs: string;
  acceptedAt: string;
  factKey: string;
  contentFingerprint: string;
  lineId: string;
  plcId: string;
  stationId: string;
  profileId: string;
  configHash: string;
  configVersion: string;
};

export type AcceptedEventsViewModel = {
  rows: AcceptedEventRow[];
  summary: PageSummary;
  selectedEvidence: NokDetailEvidence | null;
  selectedReference: TraceReference | null;
  hasNextPage: boolean;
  nextCursor: string | null;
};

function stringOrUnknown(value: string | number | null): string {
  if (value === null || value === "") return "unknown";
  return String(value);
}

function nullableString(value: string | number | null): string | null {
  if (value === null || value === "") return null;
  return String(value);
}

function nullableNumber(value: string | number | null): number | null {
  if (typeof value === "number") return value;
  if (typeof value === "string" && value.trim()) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }
  return null;
}

function buildEvidence(item: AcceptedStationEventItem): NokDetailEvidence {
  return {
    productionResult: stringOrUnknown(item.production_result),
    nokCode: nullableString(item.nok_code),
    nokOrigin: nullableString(item.nok_origin),
    nokDetailCode: nullableString(item.nok_detail_code),
    nokDetailSourceEventId: nullableString(item.nok_detail_source_event_id),
    nokDetailEvidenceFactKey: nullableString(item.nok_detail_evidence_fact_key),
    factKey: stringOrUnknown(item.fact_key),
    sourceEventId: stringOrUnknown(item.source_event_id)
  };
}

function buildReference(item: AcceptedStationEventItem): TraceReference {
  return {
    unitId: nullableString(item.unit_id),
    dmc: nullableString(item.dmc),
    cycleCounter: nullableNumber(item.cycle_counter),
    sourceEventId: stringOrUnknown(item.source_event_id),
    eventTs: stringOrUnknown(item.event_ts),
    acceptedAt: stringOrUnknown(item.accepted_at),
    factKey: stringOrUnknown(item.fact_key),
    contentFingerprint: stringOrUnknown(item.content_fingerprint),
    lineId: stringOrUnknown(item.line_id),
    plcId: stringOrUnknown(item.plc_id),
    stationId: stringOrUnknown(item.station_id),
    profileId: stringOrUnknown(item.profile_id),
    configHash: stringOrUnknown(item.config_hash),
    configVersion: stringOrUnknown(item.config_version)
  };
}

export function toAcceptedEventsViewModel(
  envelope: AcceptedStationEventsEnvelope,
  selectedFactKey?: string
): AcceptedEventsViewModel {
  const byResult: Record<string, number> = {};
  const byStation: Record<string, number> = {};

  const rows: AcceptedEventRow[] = envelope.items.map((item) => {
    const productionResult = stringOrUnknown(item.production_result);
    const stationId = stringOrUnknown(item.station_id);
    byResult[productionResult] = (byResult[productionResult] ?? 0) + 1;
    byStation[stationId] = (byStation[stationId] ?? 0) + 1;

    return {
      factKey: stringOrUnknown(item.fact_key),
      lineId: stringOrUnknown(item.line_id),
      stationId,
      stationType: stringOrUnknown(item.station_type),
      eventType: stringOrUnknown(item.event_type),
      productionResult,
      eventTs: { label: "Event time" as const, value: stringOrUnknown(item.event_ts) },
      acceptedAt: { label: "Accepted fact timestamp" as const, value: stringOrUnknown(item.accepted_at) },
      unitId: nullableString(item.unit_id),
      dmc: nullableString(item.dmc)
    };
  });

  const selectedItem =
    envelope.items.find((item) => stringOrUnknown(item.fact_key) === selectedFactKey) ?? envelope.items[0] ?? null;

  return {
    rows,
    summary: {
      label: "Current page only",
      totalAcceptedFacts: rows.length,
      byResult,
      byStation
    },
    selectedEvidence: selectedItem ? buildEvidence(selectedItem) : null,
    selectedReference: selectedItem ? buildReference(selectedItem) : null,
    hasNextPage: envelope.page.next_cursor !== null,
    nextCursor: envelope.page.next_cursor
  };
}
