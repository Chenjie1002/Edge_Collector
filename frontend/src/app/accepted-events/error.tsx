"use client";

import { AcceptedEventsPageView } from "./page";

export default function Error() {
  return <AcceptedEventsPageView state={{ kind: "error", message: "Accepted events could not be rendered." }} />;
}
