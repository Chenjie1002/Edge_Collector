import "../styles/globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Edge MES Dashboard",
  description: "Read-only accepted station-event facts dashboard"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
