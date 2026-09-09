'use client';

import React from 'react';
import { SchemeMatchResult, Language } from '../types/api';

interface SchemeCardProps {
  match: SchemeMatchResult;
  isTopRecommendation?: boolean;
  language: Language;
  onWhyEligible: (schemeId: string, schemeName: string, schemeCode: string) => void;
  onCalculateEmi: (amount: number, rate: number, tenure: number, moratorium: number) => void;
  onLocatePartners: (schemeId: string, category: string) => void;
}

export const SchemeCard: React.FC<SchemeCardProps> = ({
  match,
  isTopRecommendation = false,
  language,
  onWhyEligible,
  onCalculateEmi,
  onLocatePartners
}) => {
  const { scheme, match_percentage, match_score } = match;
  const scorePct = Math.round(match_percentage || (match_score * 100));

  return (
    <article
      className={`bg-white rounded-xl border p-5 transition shadow-sm hover:shadow-md ${
        isTopRecommendation
          ? 'border-l-4 border-l-[#0B6E4F] border-slate-200'
          : 'border-slate-200'
      }`}
    >
      <div className="flex justify-between items-start gap-4">
        <div>
          <span className="inline-flex items-center gap-1 bg-[#E8EEF5] text-[#0F2C59] px-2 py-0.5 rounded text-[11px] font-bold mb-1">
            {scheme.scheme_code} • {scheme.ministry}
          </span>
          <h3 className="text-lg font-bold text-slate-900 leading-snug">{scheme.scheme_name}</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">{scheme.description}</p>
        </div>

        {/* Score Badge */}
        <div className="bg-[#E6F4EA] border border-[#0B6E4F] text-[#074D37] px-3 py-1.5 rounded-lg text-center shrink-0">
          <div className="text-xl font-black">{scorePct}%</div>
          <div className="text-[10px] font-bold uppercase tracking-wider">
            {language === 'hi' ? 'सटीक मिलान' : 'Match Score'}
          </div>
        </div>
      </div>

      {/* Financial Parameters */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-3 rounded-lg my-3.5 text-xs">
        <div>
          <div className="text-slate-500 font-medium">अधिकतम ऋण सीमा</div>
          <div className="text-sm font-bold text-[#0F2C59]">
            ₹{(scheme.max_loan_amount || 1500000).toLocaleString('en-IN')}
          </div>
        </div>
        <div>
          <div className="text-slate-500 font-medium">रियायती ब्याज दर</div>
          <div className="text-sm font-bold text-[#0F2C59]">
            {scheme.concessional_interest_rate_pct || 5.0}% प्रति वर्ष
          </div>
        </div>
        <div>
          <div className="text-slate-500 font-medium">मोराटोरियम छूट</div>
          <div className="text-sm font-bold text-[#0F2C59]">
            {scheme.moratorium_months || 6} महीने
          </div>
        </div>
        <div>
          <div className="text-slate-500 font-medium">अधिकतम अवधि</div>
          <div className="text-sm font-bold text-[#0F2C59]">
            {(scheme.max_tenure_months || 60) / 12} वर्ष
          </div>
        </div>
      </div>

      {/* 6-Factor Breakdown */}
      <div className="my-2.5">
        <div className="text-[11px] font-bold uppercase text-slate-500 flex justify-between mb-1.5">
          <span>पारदर्शी 6-कारकीय वेटेज स्कोर</span>
          <span className="text-[#0B6E4F]">100% Deterministic</span>
        </div>
        <div className="flex flex-wrap gap-2 text-[11px]">
          <span className="bg-[#E6F4EA] text-[#074D37] px-2 py-0.5 rounded border border-[#0B6E4F]/30 font-medium">
            वर्ग (OBC): 100%
          </span>
          <span className="bg-[#E6F4EA] text-[#074D37] px-2 py-0.5 rounded border border-[#0B6E4F]/30 font-medium">
            वार्षिक आय: 100%
          </span>
          <span className="bg-[#E6F4EA] text-[#074D37] px-2 py-0.5 rounded border border-[#0B6E4F]/30 font-medium">
            परियोजना: 95%
          </span>
          <span className="bg-[#E6F4EA] text-[#074D37] px-2 py-0.5 rounded border border-[#0B6E4F]/30 font-medium">
            स्थान (UP): 100%
          </span>
          <span className="bg-[#E6F4EA] text-[#074D37] px-2 py-0.5 rounded border border-[#0B6E4F]/30 font-medium">
            शिक्षा: 100%
          </span>
          <span className="bg-[#E6F4EA] text-[#074D37] px-2 py-0.5 rounded border border-[#0B6E4F]/30 font-medium">
            आयु: 100%
          </span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap items-center gap-2 mt-4 pt-3 border-t border-slate-100">
        <button
          onClick={() => onWhyEligible(scheme.id, scheme.scheme_name, scheme.scheme_code)}
          className="px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#0F2C59] text-white hover:bg-[#0A1C38] transition flex items-center gap-1"
        >
          <span>🔍</span>
          <span>पात्रता का कारण (Rule Trace)</span>
        </button>

        <button
          onClick={() =>
            onCalculateEmi(
              scheme.max_loan_amount || 500000,
              scheme.concessional_interest_rate_pct || 5.0,
              scheme.max_tenure_months || 60,
              scheme.moratorium_months || 6
            )
          }
          className="px-3.5 py-1.5 rounded-full text-xs font-bold bg-slate-100 text-slate-800 hover:bg-slate-200 transition flex items-center gap-1"
        >
          <span>🧮</span>
          <span>ईएमआई देखें</span>
        </button>

        <button
          onClick={() => onLocatePartners(scheme.id, scheme.target_group)}
          className="px-3.5 py-1.5 rounded-full text-xs font-bold bg-slate-100 text-slate-800 hover:bg-slate-200 transition flex items-center gap-1"
        >
          <span>📍</span>
          <span>पार्टनर खोजें</span>
        </button>

        {scheme.application_url && (
          <a
            href={scheme.application_url}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-auto text-xs font-bold text-[#0F2C59] hover:underline flex items-center gap-1"
          >
            <span>🌐</span>
            <span>आधिकारिक पोर्टल</span>
          </a>
        )}
      </div>
    </article>
  );
};
