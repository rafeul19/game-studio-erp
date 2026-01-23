import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { StoreProvider } from "@/components/providers/StoreProvider";
import { AntdProvider } from "@/components/providers/AntdProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Game Studio ERP",
  description: "Enterprise Resource Planning for modern game studios",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <StoreProvider>
          <AntdProvider>
            {children}
          </AntdProvider>
        </StoreProvider>
      </body>
    </html>
  );
}
