import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Entrepreneur Mitra | उद्यमी मित्र - MoSJE',
  description: 'AI-Driven Scheme Matching for Marginalized Entrepreneurs (Ministry of Social Justice and Empowerment)',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="hi">
      <body className="bg-slate-50 text-slate-900 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
