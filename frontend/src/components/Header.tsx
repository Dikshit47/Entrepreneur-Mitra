'use client';

import React from 'react';
import { Language } from '../types/api';

interface HeaderProps {
  language: Language;
  onLanguageToggle: () => void;
  onLoadRamesh: () => void;
  highContrast: boolean;
  onContrastToggle: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  language,
  onLanguageToggle,
  onLoadRamesh,
  highContrast,
  onContrastToggle
}) => {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
      {/* Top Tricolor Strip */}
      <div
        className="h-1 w-full"
        style={{
          background: 'linear-gradient(90deg, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%)'
        }}
        aria-hidden="true"
      />

      {/* Official Government Bar */}
      <div className="bg-[#0A1C38] text-[#E8EEF5] text-xs px-4 py-1.5 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span>🇮🇳</span>
          <span className="font-medium">
            {language === 'hi'
              ? 'सामाजिक न्याय और अधिकारिता मंत्रालय | MoSJE'
              : 'Ministry of Social Justice and Empowerment | MoSJE'}
          </span>
        </div>
        <span className="bg-white/20 text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded">
          {language === 'hi' ? 'भारत सरकार' : 'Govt of India'}
        </span>
      </div>

      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E8EEF5] text-[#0F2C59] border border-[#0F2C59] flex items-center justify-center text-xl font-bold">
            🏛️
          </div>
          <div>
            <h1 className="text-lg md:text-xl font-black text-[#0F2C59] leading-tight">
              {language === 'hi' ? 'उद्यमी मित्र (Entrepreneur Mitra)' : 'Entrepreneur Mitra'}
            </h1>
            <p className="text-xs text-slate-500 font-medium">
              SIH26092 • AI-Driven Scheme Matching for Marginalized Entrepreneurs
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* 1-Click SIH Persona Demo */}
          <button
            onClick={onLoadRamesh}
            className="px-3 py-1.5 rounded-full text-xs font-bold bg-[#FFF3EB] text-[#E85D04] border border-[#E85D04] hover:bg-[#E85D04] hover:text-white transition flex items-center gap-1.5 shadow-sm"
            title="Load SIH Demo Persona (Ramesh Kumar - OBC Carpenter)"
          >
            <span>👤</span>
            <span>{language === 'hi' ? 'डेमो: रमेश कुमार' : 'Demo: Ramesh Kumar'}</span>
          </button>

          {/* High Contrast */}
          <button
            onClick={onContrastToggle}
            className={`p-2 rounded-full text-xs font-bold border transition ${
              highContrast ? 'bg-black text-white border-white' : 'bg-slate-50 border-slate-300 text-slate-700'
            }`}
            title="Toggle High Contrast AAA"
            aria-label="High contrast mode toggle"
          >
            👁️ AAA
          </button>

          {/* Language Switch */}
          <button
            onClick={onLanguageToggle}
            className="px-3 py-1.5 rounded-full text-xs font-bold bg-white border border-slate-300 hover:border-[#0F2C59] text-slate-800 transition"
          >
            {language === 'hi' ? 'हिंदी / EN' : 'EN / हिंदी'}
          </button>
        </div>
      </div>
    </header>
  );
};
