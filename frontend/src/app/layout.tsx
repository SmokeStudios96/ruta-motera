// frontend/src/app/layout.tsx
import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import PwaRegister from '@/components/pwa/PwaRegister';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'RutaMotera - Dark Biker Navigator',
  description: 'Navegación de alta precisión, alertas climáticas y radar de ruta para motociclistas.',
  applicationName: 'RutaMotera',
  manifest: '/manifest.json', // <-- Apuntando al archivo estático en public/
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'RutaMotera',
  },
  formatDetection: {
    telephone: false,
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#09090b',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`dark ${inter.className}`}>
      <body className="bg-[#09090b] text-zinc-100 antialiased min-h-screen overflow-hidden select-none">
        <PwaRegister />
        {children}
      </body>
    </html>
  );
}