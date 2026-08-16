import "../styles/globals.css";
import type { ReactNode } from "react";
import { ProductNavigation } from "../components/product/ProductNavigation";

export const metadata = {
  title: "Edge MES Dashboard",
  description: "Read-only accepted station-event facts dashboard"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ProductNavigation />
        {children}
      </body>
    </html>
  );
}
