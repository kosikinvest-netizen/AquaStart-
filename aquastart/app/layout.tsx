import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AquaStart Premium | System Masterpiece",
  description: "Pierwszy w Polsce inżynieryjny algorytm prowadzenia akwarium High-Tech.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pl" suppressHydrationWarning className="scroll-smooth">
      <body className="antialiased bg-[#040814] text-slate-200 min-h-screen">
        {children}
      </body>
    </html>
  );
}