'use client';

import React from 'react';
import { CriterionEvaluation } from '../types/api';

interface RuleTraceModalProps {
  isOpen: boolean;
  schemeName: string;
  schemeCode: string;
  criteria: CriterionEvaluation[];
  onClose: () => void;
}

export const RuleTraceModal: React.FC<RuleTraceModalProps> = ({
  isOpen,
  schemeName,
  schemeCode,
  criteria,
  onClose
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#0F2C59]/60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl max-w-xl w-full max-h-[85vh] flex flex-col shadow-2xl animate-in fade-in zoom-in-95">
        {/* Header */}
        <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-[#E8EEF5] rounded-t-2xl">
          <div>
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              पात्रता नियम विश्लेषण (Traceable Rule Audit)
            </span>
            <h3 className="text-base font-bold text-[#0F2C59]">{schemeName}</h3>
            <span className="text-xs text-slate-600">{schemeCode}</span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-slate-400 hover:text-slate-700 text-lg font-bold"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="p-5 overflow-y-auto space-y-4">
          {/* Zero Hallucination Guarantee Badge */}
          <div className="bg-[#E6F4EA] border border-[#0B6E4F] rounded-xl p-3 flex items-center gap-3 text-xs text-[#074D37]">
            <span className="text-xl">🛡️</span>
            <div>
              <strong className="font-bold">शून्य-भ्रम गारंटी (Deterministic Rule Engine):</strong>
              <p className="mt-0.5 text-[11px]">
                यह मूल्यांकन MoSJE राजपत्र एवं NBCFDC वैधानिक दिशा-निर्देशों के कोड-सत्यापित नियमों के आधार पर तैयार किया गया है।
              </p>
            </div>
          </div>

          {/* Criteria Checklist */}
          <div className="space-y-2.5">
            {criteria.map((c, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border text-xs ${
                  c.passed
                    ? 'border-l-4 border-l-[#0B6E4F] border-slate-200 bg-slate-50'
                    : 'border-l-4 border-l-red-500 border-slate-200 bg-red-50/50'
                }`}
              >
                <div className="flex justify-between items-center font-bold text-slate-900 mb-1">
                  <span>{c.criterion_name}</span>
                  <span
                    className={`font-black ${
                      c.passed ? 'text-[#0B6E4F]' : 'text-red-600'
                    }`}
                  >
                    {c.passed ? '✓ PASSED (सत्यापित)' : '✗ FAILED (अपात्र)'}
                  </span>
                </div>
                {c.official_citation && (
                  <div className="text-[11px] text-slate-500 italic mb-1">
                    वैधानिक संदर्भ: {c.official_citation}
                  </div>
                )}
                <div className="text-slate-700">{c.explanation}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 text-right bg-slate-50 rounded-b-2xl">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-full text-xs font-bold bg-[#0F2C59] text-white hover:bg-[#0A1C38] transition"
          >
            समझ गया (Understood)
          </button>
        </div>
      </div>
    </div>
  );
};
