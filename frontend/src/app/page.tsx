'use client';

import React, { useState } from 'react';
import { Header } from '../components/Header';
import { SchemeCard } from '../components/SchemeCard';
import { EmiCalculator } from '../components/EmiCalculator';
import { RuleTraceModal } from '../components/RuleTraceModal';
import { Language, SchemeMatchResult, CriterionEvaluation } from '../types/api';

const MOCK_SCHEMES: SchemeMatchResult[] = [
  {
    scheme: {
      id: 'NBCFDC-GTL-001',
      scheme_code: 'NBCFDC-GTL-001',
      scheme_name: 'NBCFDC General Term Loan Scheme (सामान्य सावधि ऋण योजना)',
      ministry: 'Ministry of Social Justice and Empowerment',
      description: 'रियायती ब्याज दर पर ₹15 लाख तक का सावधि ऋण स्वरोजगार, उपकरण क्रय एवं कार्यशाला विस्तार हेतु।',
      scheme_type: 'CREDIT',
      target_group: 'OBC',
      max_loan_amount: 1500000,
      concessional_interest_rate_pct: 5.0,
      moratorium_months: 6,
      max_tenure_months: 60,
      application_url: 'https://nbcfdc.gov.in',
      status: 'ACTIVE'
    },
    match_score: 0.96,
    match_percentage: 96.0,
    is_eligible: true,
    rejection_reasons: [],
    factor_scores: {
      target_group: 1.0,
      income_fit: 1.0,
      project_type_fit: 0.95,
      location_fit: 1.0,
      education_fit: 1.0,
      age_fit: 1.0
    }
  },
  {
    scheme: {
      id: 'STANDUP-INDIA-001',
      scheme_code: 'STANDUP-INDIA-001',
      scheme_name: 'Stand-Up India Scheme (स्टैंड-अप इंडिया योजना)',
      ministry: 'Ministry of Finance / MoSJE',
      description: 'अनुसूचित जाति, जनजाति एवं महिला उद्यमियों हेतु ₹10 लाख से ₹1 करोड़ तक का बैंक ऋण।',
      scheme_type: 'CREDIT',
      target_group: 'SC/ST/WOMEN',
      max_loan_amount: 10000000,
      concessional_interest_rate_pct: 7.5,
      moratorium_months: 18,
      max_tenure_months: 84,
      application_url: 'https://www.standupmitra.in',
      status: 'ACTIVE'
    },
    match_score: 0.88,
    match_percentage: 88.0,
    is_eligible: true,
    rejection_reasons: [],
    factor_scores: {
      target_group: 0.8,
      income_fit: 1.0,
      project_type_fit: 1.0,
      location_fit: 1.0,
      education_fit: 1.0,
      age_fit: 1.0
    }
  }
];

const DEFAULT_CRITERIA: CriterionEvaluation[] = [
  {
    criterion_name: 'सामाजिक श्रेणी / लक्षित समूह (Target Group OBC)',
    passed: true,
    explanation: 'आवेदक अन्य पिछड़ा वर्ग (OBC) से हैं, जो योजना के लक्षित लाभार्थियों में शामिल है।',
    official_citation: 'NBCFDC General Term Loan Guidelines, Clause 3(a)'
  },
  {
    criterion_name: 'पारिवारिक वार्षिक आय सीमा (Income Cap <= ₹3,00,000)',
    passed: true,
    explanation: 'आवेदक की वार्षिक आय ₹1,80,000 MoSJE राजपत्र में उल्लिखित अधिकतम सीमा ₹3,00,000 के अंतर्गत है।',
    official_citation: 'MoSJE Statutory Notification 2023, Section 4.1'
  },
  {
    criterion_name: 'प्रस्तावित परियोजना लागत (Project Cost <= ₹15,00,000)',
    passed: true,
    explanation: 'प्रस्तावित लकड़ी कार्यशाला लागत ₹5,00,000 योजना की अधिकतम ऋण सीमा ₹15,00,000 के अंतर्गत है।',
    official_citation: 'NBCFDC Lending Policy, Section 5.2'
  },
  {
    criterion_name: 'आवेदक आयु पात्रता (Age 18 to 55 years)',
    passed: true,
    explanation: 'आवेदक की आयु 32 वर्ष अनिवार्य सीमा (18 से 55) के मध्य है।',
    official_citation: 'MoSJE General Credit Rules, Rule 2'
  }
];

export default function HomePage() {
  const [language, setLanguage] = useState<Language>('hi');
  const [highContrast, setHighContrast] = useState(false);
  const [selectedScheme, setSelectedScheme] = useState<{ id: string; name: string; code: string } | null>(null);

  const handleLoadRamesh = () => {
    alert('👤 रमेश कुमार (बिजनौर, बढ़ई - OBC) का प्रोफ़ाइल सफलतापूर्वक लोड हुआ!');
  };

  return (
    <div className={`min-h-screen ${highContrast ? 'bg-black text-white' : 'bg-slate-50 text-slate-900'}`}>
      <Header
        language={language}
        onLanguageToggle={() => setLanguage(language === 'hi' ? 'en' : 'hi')}
        onLoadRamesh={handleLoadRamesh}
        highContrast={highContrast}
        onContrastToggle={() => setHighContrast(!highContrast)}
      />

      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {/* Anti-Scam Advisory */}
        <div className="bg-[#FEF3C7] border border-[#D97706] text-[#78350F] text-xs p-3.5 rounded-xl flex items-center gap-3">
          <span className="text-xl">🛡️</span>
          <div>
            <strong className="font-bold">सचेत रहें (Official Anti-Scam Advisory):</strong> सरकारी योजनाओं के आवेदन हेतु कभी भी किसी दलाल या बिचौलिए को कोई शुल्क न दें और न ही OTP साझा करें। समस्त MoSJE / NBCFDC सेवाएं पूर्णतः निःशुल्क हैं।
          </div>
        </div>

        {/* Hero Section */}
        <div className="bg-gradient-to-br from-[#0F2C59] to-[#0A1C38] text-white p-8 rounded-2xl shadow-md">
          <span className="bg-white/15 px-3 py-1 rounded-full text-xs font-bold tracking-wider inline-flex items-center gap-1.5 mb-3">
            <span>✨</span> आवाज़-आधारित AI सहायक
          </span>
          <h2 className="text-2xl md:text-3xl font-black leading-tight mb-2">
            अपनी मातृभाषा में बोलें,<br />सटीक सरकारी योजना पाएं
          </h2>
          <p className="text-sm text-slate-300 max-w-2xl mb-6">
            वंचित वर्ग के उद्यमियों के लिए शून्य-भ्रम (Zero-Hallucination) आधारित रियायती ऋण, ब्याज अनुदान एवं कौशल विकास योजनाएं।
          </p>
          <div className="flex flex-wrap gap-3">
            <a
              href="http://127.0.0.1:8000/"
              className="px-6 py-3 rounded-full font-bold text-sm bg-[#E85D04] text-white hover:bg-[#C44D00] transition flex items-center gap-2 shadow-lg"
            >
              <span>🎙️</span>
              <span>लाइव वेब ऐप खोलें (Open Live PWA)</span>
            </a>
          </div>
        </div>

        {/* Schemes Section */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <div>
              <h2 className="text-xl font-black text-[#0F2C59]">स्मार्ट योजना अनुशंसाएं (Recommendations)</h2>
              <p className="text-xs text-slate-500">6-कारकीय पारदर्शी वेटेज मॉडल द्वारा जांची गई आधिकारिक योजनाएं</p>
            </div>
          </div>

          <div className="space-y-4">
            {MOCK_SCHEMES.map((m, idx) => (
              <SchemeCard
                key={m.scheme.id}
                match={m}
                isTopRecommendation={idx === 0}
                language={language}
                onWhyEligible={(id, name, code) => setSelectedScheme({ id, name, code })}
                onCalculateEmi={() => {}}
                onLocatePartners={() => {}}
              />
            ))}
          </div>
        </div>

        {/* Calculator */}
        <EmiCalculator language={language} />
      </main>

      {/* Rule Trace Modal */}
      <RuleTraceModal
        isOpen={!!selectedScheme}
        schemeName={selectedScheme?.name || ''}
        schemeCode={selectedScheme?.code || ''}
        criteria={DEFAULT_CRITERIA}
        onClose={() => setSelectedScheme(null)}
      />
    </div>
  );
}
