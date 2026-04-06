import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://www.ocr-extraction.com"),
  title: {
    default: "Free OCR to Text | Convert Image to Text & Excel | 100% Accurate",
    template: "%s | OCR Extraction",
  },
  description: "Global AI platform specializing in AI workflow orchestration, AI-powered tools, and hiring top 1% AI engineers.",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://www.ocr-extraction.com",
    siteName: "OCR Extraction",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${outfit.variable} h-full`}
    >
      <body className="min-h-full flex flex-col bg-background font-sans">
        {process.env.NEXT_PUBLIC_BASE_PATH === "/v2" && (
          <div className="fixed top-0 left-0 right-0 z-[9999] bg-amber-500 text-white text-[10px] font-bold text-center py-0.5 uppercase tracking-widest shadow-sm">
            Staging Environment (/V2) • Internal Review Only
          </div>
        )}
        {/* Navigation Wrapper */}
        <div className="flex h-full flex-col">
          {children}
        </div>
      </body>
    </html>
  );
}
