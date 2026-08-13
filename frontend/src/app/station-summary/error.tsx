"use client";

import { StationSummaryPageView } from "./page";

export default function Error() {
  return <StationSummaryPageView state={{ kind: "error", message: "Station summary could not be rendered." }} />;
}
