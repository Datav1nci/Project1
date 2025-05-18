import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";       // ⬅ placé dans src/styles
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Metanova – Génie-Conseil à Montréal",
  description: "Ingénierie structurelle et développement urbain partout au Québec.",
  keywords: ["génie-conseil", "structure", "ingénierie", "Montréal", "Metanova"],
  authors: [{ name: "Metanova Experts-Conseils" }],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={`${inter.variable} scroll-smooth`}>
      <body className="antialiased bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-100">
        <Header />
        <main className="mx-auto max-w-7xl px-4">{children}</main>
        <Footer />
      
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                  navigator.serviceWorker
                    .register('/service-worker.js')
                    .then((registration) => {
                      console.log('Service Worker registered with scope:', registration.scope);
                    })
                    .catch((error) => {
                      console.error('Service Worker registration failed:', error);
                    });
                });
              }
            `,
          }}
        />      
      </body>
    </html>
  );
}
