import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DecoraAI",
  description: "Your interior design helper at your fingertips",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        data-new-gr-c-s-check-loaded="14.1256.0"
        data-gr-ext-installed=""
      >
        {children}
      </body>
    </html>
  );
}
