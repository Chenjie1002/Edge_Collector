import type {
  AcceptedProductionResult,
  AcceptedStationEventItem,
  AcceptedStationEventType,
  AcceptedStationEventsEnvelope
} from "./schema";

export type DisplayKind = "value" | "empty-string" | "null" | "not-applicable";

export type DisplayValue<T extends string | number | null> = {
  raw: T;
  text: string;
  kind: DisplayKind;
};

export type TimestampDisplay = DisplayValue<string> & {
  label: "Event time" | "Accepted fact timestamp";
};

export type AcceptedEventRow = {
  sourceItem: AcceptedStationEventItem;
  factKey: string;
  lineId: DisplayValue<string>;
  stationId: DisplayValue<string>;
  stationType: DisplayValue<string>;
  eventType: DisplayValue<AcceptedStationEventType>;
  productionResult: DisplayValue<AcceptedProductionResult | null>;
  eventTs: TimestampDisplay;
  acceptedAt: TimestampDisplay;
  unitId: DisplayValue<string | null>;
  dmc: DisplayValue<string | null>;
};

export type PageSummary = {
  label: "Current page only";
  totalAcceptedFacts: number;
  byResult: Record<string, number>;
  byStation: Record<string, number>;
};

export type AcceptedEventRowRole = "station_result outcome" | "station_nok detail companion" | "cycle event";

export type NokDetailEvidence = {
  sourceItem: AcceptedStationEventItem;
  rowRole: AcceptedEventRowRole;
  eventType: DisplayValue<AcceptedStationEventType>;
  productionResult: DisplayValue<AcceptedProductionResult | null>;
  nokCode: DisplayValue<number | null>;
  nokOrigin: DisplayValue<string | null>;
  nokDetailCode: DisplayValue<number | null>;
  nokDetailSourceEventId: DisplayValue<string | null>;
  nokDetailEvidenceFactKey: DisplayValue<string | null>;
  factKey: string;
  sourceEventId: DisplayValue<string>;
};

export type TraceReference = {
  sourceItem: AcceptedStationEventItem;
  unitId: DisplayValue<string | null>;
  dmc: DisplayValue<string | null>;
  cycleCounter: DisplayValue<number>;
  sourceEventId: DisplayValue<string>;
  eventTs: TimestampDisplay;
  acceptedAt: TimestampDisplay;
  factKey: string;
  factKeyDisplay: DisplayValue<string>;
  contentFingerprint: DisplayValue<string>;
  lineId: DisplayValue<string>;
  plcId: DisplayValue<string>;
  stationId: DisplayValue<string>;
  profileId: DisplayValue<string>;
  configHash: DisplayValue<string>;
  configVersion: DisplayValue<string>;
};

export type AcceptedEventsViewModel = {
  rows: AcceptedEventRow[];
  summary: PageSummary;
  selectedEvidence: NokDetailEvidence | null;
  selectedReference: TraceReference | null;
  hasNextPage: boolean;
  nextCursor: string | null;
};

function displayString<T extends string | null>(raw: T): DisplayValue<T> {
  if (raw === null) return { raw, text: "—", kind: "null" };
  if (raw === "") return { raw, text: "Empty string", kind: "empty-string" };
  return { raw, text: raw, kind: "value" };
}

function displayNumber<T extends number | null>(raw: T): DisplayValue<T> {
  if (raw === null) return { raw, text: "—", kind: "null" };
  return { raw, text: String(raw), kind: "value" };
}

function displayTimestamp(raw: string, label: TimestampDisplay["label"]): TimestampDisplay {
  return { ...displayString(raw), label };
}

function displayProductionResult(item: AcceptedStationEventItem): DisplayValue<AcceptedProductionResult | null> {
  if (item.event_type === "station_nok") {
    return {
      raw: item.production_result,
      text: "Not applicable — NOK detail companion",
      kind: "not-applicable"
    };
  }

  if (item.event_type === "station_cycle_start" || item.event_type === "station_cycle_complete") {
    return {
      raw: item.production_result,
      text: "Not applicable — cycle event",
      kind: "not-applicable"
    };
  }

  return displayString(item.production_result);
}

function rowRole(eventType: AcceptedStationEventType): AcceptedEventRowRole {
  if (eventType === "station_result") return "station_result outcome";
  if (eventType === "station_nok") return "station_nok detail companion";
  return "cycle event";
}

function copyAcceptedItem(item: AcceptedStationEventItem): AcceptedStationEventItem {
  return {
    line_id: item.line_id,
    plc_id: item.plc_id,
    station_id: item.station_id,
    station_type: item.station_type,
    profile_id: item.profile_id,
    config_hash: item.config_hash,
    config_version: item.config_version,
    event_type: item.event_type,
    production_result: item.production_result,
    unit_id: item.unit_id,
    dmc: item.dmc,
    cycle_counter: item.cycle_counter,
    source_event_id: item.source_event_id,
    event_ts: item.event_ts,
    accepted_at: item.accepted_at,
    fact_key: item.fact_key,
    content_fingerprint: item.content_fingerprint,
    nok_code: item.nok_code,
    nok_origin: item.nok_origin,
    nok_detail_code: item.nok_detail_code,
    nok_detail_source_event_id: item.nok_detail_source_event_id,
    nok_detail_evidence_fact_key: item.nok_detail_evidence_fact_key
  };
}

function buildRow(item: AcceptedStationEventItem): AcceptedEventRow {
  return {
    sourceItem: item,
    factKey: item.fact_key,
    lineId: displayString(item.line_id),
    stationId: displayString(item.station_id),
    stationType: displayString(item.station_type),
    eventType: displayString(item.event_type),
    productionResult: displayProductionResult(item),
    eventTs: displayTimestamp(item.event_ts, "Event time"),
    acceptedAt: displayTimestamp(item.accepted_at, "Accepted fact timestamp"),
    unitId: displayString(item.unit_id),
    dmc: displayString(item.dmc)
  };
}

function buildEvidence(item: AcceptedStationEventItem): NokDetailEvidence {
  return {
    sourceItem: item,
    rowRole: rowRole(item.event_type),
    eventType: displayString(item.event_type),
    productionResult: displayProductionResult(item),
    nokCode: displayNumber(item.nok_code),
    nokOrigin: displayString(item.nok_origin),
    nokDetailCode: displayNumber(item.nok_detail_code),
    nokDetailSourceEventId: displayString(item.nok_detail_source_event_id),
    nokDetailEvidenceFactKey: displayString(item.nok_detail_evidence_fact_key),
    factKey: item.fact_key,
    sourceEventId: displayString(item.source_event_id)
  };
}

function buildReference(item: AcceptedStationEventItem): TraceReference {
  return {
    sourceItem: item,
    unitId: displayString(item.unit_id),
    dmc: displayString(item.dmc),
    cycleCounter: displayNumber(item.cycle_counter),
    sourceEventId: displayString(item.source_event_id),
    eventTs: displayTimestamp(item.event_ts, "Event time"),
    acceptedAt: displayTimestamp(item.accepted_at, "Accepted fact timestamp"),
    factKey: item.fact_key,
    factKeyDisplay: displayString(item.fact_key),
    contentFingerprint: displayString(item.content_fingerprint),
    lineId: displayString(item.line_id),
    plcId: displayString(item.plc_id),
    stationId: displayString(item.station_id),
    profileId: displayString(item.profile_id),
    configHash: displayString(item.config_hash),
    configVersion: displayString(item.config_version)
  };
}

export function toAcceptedEventsViewModel(
  envelope: AcceptedStationEventsEnvelope,
  selectedFactKey?: string
): AcceptedEventsViewModel {
  const byResult: Record<string, number> = {};
  const byStation: Record<string, number> = {};
  const sourceItems = envelope.items.map(copyAcceptedItem);

  const rows = sourceItems.map((item) => {
    byStation[item.station_id] = (byStation[item.station_id] ?? 0) + 1;
    if (item.event_type === "station_result" && item.production_result !== null) {
      byResult[item.production_result] = (byResult[item.production_result] ?? 0) + 1;
    }
    return buildRow(item);
  });

  const selectedItem = sourceItems.find((item) => item.fact_key === selectedFactKey) ?? sourceItems[0] ?? null;

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
