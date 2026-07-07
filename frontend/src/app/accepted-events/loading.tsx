import { AcceptedEventsPageView } from "./page";

export default function Loading() {
  return (
    <AcceptedEventsPageView
      state={{
        kind: "loading",
        message: "Loading accepted station-event facts.",
        priorDataNotice: "Prior accepted facts are hidden while this request is loading."
      }}
    />
  );
}
