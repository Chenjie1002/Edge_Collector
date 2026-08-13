import { StationSummaryPageView } from "./page";

export default function Loading() {
  return (
    <StationSummaryPageView
      state={{
        kind: "loading",
        message: "Loading station summary.",
        priorDataNotice: "Prior station values are hidden while this request is loading."
      }}
    />
  );
}
