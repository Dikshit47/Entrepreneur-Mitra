'use client';

import React, { useState, useEffect } from 'react';
import { Language } from '../types/api';

interface EmiCalculatorProps {
  initialAmount?: number;
  initialRate?: number;
  initialTenure?: number;
  initialMoratorium?: number;
  language: Language;
}

export const EmiCalculator: React.FC<EmiCalculatorProps> = ({
  initialAmount = 500000,
  initialRate = 5.0,
  initialTenure = 60,
  initialMoratorium = 6,
  language
}) => {
  const [loanAmount, setLoanAmount] = useState(initialAmount);
  const [interestRate, setInterestRate] = useState(initialRate);
  const [tenure, setTenure] = useState(initialTenure);
  const [moratorium, setMoratorium] = useState(initialMoratorium);
  const [monthlyIncome, setMonthlyIncome] = useState(20000);

  // EMI and Affordability calculations
  const monthlyRate = interestRate / 100 / 12;
  const repaymentMonths = Math.max(1, tenure - moratorium);
  const moratoriumInterest = loanAmount * (interestRate / 100) * (moratorium / 12);
  const effectivePrincipal = loanAmount + moratoriumInterest * 0.5;

  const emi =
    (effectivePrincipal * monthlyRate * Math.pow(1 + monthlyRate, repaymentMonths)) /
    (Math.pow(1 + monthlyRate, repaymentMonths) - 1);

  const totalInterest = Math.max(0, emi * repaymentMonths - loanAmount);
  const totalRepayment = emi * repaymentMonths + loanAmount * 0.05;
  const marginMoney = loanAmount * 0.05;
  const dti = Math.round((emi / monthlyIncome) * 100);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-xl font-black text-[#0F2C59]">
          {language === 'hi' ? 'वित्तीय सामर्थ्य एवं ईएमआई कैलकुलेटर' : 'Financial Affordability & EMI Calculator'}
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          {language === 'hi'
            ? 'मोराटोरियम, मार्जिन मनी एवं रियायती ब्याज दर के आधार पर वास्तविक गणना'
            : 'Projected monthly installment considering government concessional terms'}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Sliders */}
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-xs font-bold mb-1">
              <label>ऋण राशि (Loan Amount)</label>
              <span className="text-[#0F2C59] font-black">₹{loanAmount.toLocaleString('en-IN')}</span>
            </div>
            <input
              type="range"
              min={25000}
              max={2500000}
              step={25000}
              value={loanAmount}
              onChange={(e) => setLoanAmount(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#E85D04]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold mb-1">
              <label>रियायती ब्याज दर (% p.a.)</label>
              <span className="text-[#0F2C59] font-black">{interestRate.toFixed(1)}%</span>
            </div>
            <input
              type="range"
              min={3.0}
              max={14.0}
              step={0.5}
              value={interestRate}
              onChange={(e) => setInterestRate(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#E85D04]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold mb-1">
              <label>पुनर्भुगतान अवधि (Tenure)</label>
              <span className="text-[#0F2C59] font-black">{tenure} महीने ({(tenure / 12).toFixed(1)} वर्ष)</span>
            </div>
            <input
              type="range"
              min={12}
              max={120}
              step={6}
              value={tenure}
              onChange={(e) => setTenure(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#E85D04]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold mb-1">
              <label>मोराटोरियम छूट अवधि (Moratorium)</label>
              <span className="text-[#0F2C59] font-black">{moratorium} महीने</span>
            </div>
            <input
              type="range"
              min={0}
              max={18}
              step={1}
              value={moratorium}
              onChange={(e) => setMoratorium(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#E85D04]"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold mb-1">
              <label>आवेदक की अनुमानित मासिक आय</label>
              <span className="text-[#0F2C59] font-black">₹{monthlyIncome.toLocaleString('en-IN')}</span>
            </div>
            <input
              type="range"
              min={5000}
              max={100000}
              step={5000}
              value={monthlyIncome}
              onChange={(e) => setMonthlyIncome(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#E85D04]"
            />
          </div>
        </div>

        {/* Results Card */}
        <div className="bg-gradient-to-br from-[#0F2C59] to-[#0A1C38] text-white rounded-xl p-5 flex flex-col justify-between shadow-md">
          <div className="text-center pb-4 border-b border-white/10">
            <span className="text-[11px] uppercase tracking-wider text-slate-300 font-bold">
              प्रक्षेपित मासिक ईएमआई (Monthly EMI)
            </span>
            <div className="text-3xl font-black mt-1">₹{Math.round(emi).toLocaleString('en-IN')}</div>
            <span className="text-[11px] text-slate-400">*मोराटोरियम अवधि समाप्त होने के बाद लागू</span>
          </div>

          <div className="grid grid-cols-2 gap-3 my-4 text-xs">
            <div className="bg-white/10 p-2.5 rounded-lg">
              <div className="text-slate-300">कुल देय ब्याज</div>
              <div className="text-base font-bold mt-0.5">₹{Math.round(totalInterest).toLocaleString('en-IN')}</div>
            </div>
            <div className="bg-white/10 p-2.5 rounded-lg">
              <div className="text-slate-300">कुल पुनर्भुगतान</div>
              <div className="text-base font-bold mt-0.5">₹{Math.round(totalRepayment).toLocaleString('en-IN')}</div>
            </div>
            <div className="bg-white/10 p-2.5 rounded-lg">
              <div className="text-slate-300">उद्यमी अंशदान (5%)</div>
              <div className="text-base font-bold mt-0.5">₹{Math.round(marginMoney).toLocaleString('en-IN')}</div>
            </div>
            <div className="bg-white/10 p-2.5 rounded-lg">
              <div className="text-slate-300">सामर्थ्य अनुपात (DTI)</div>
              <div
                className={`text-base font-bold mt-0.5 ${
                  dti <= 35 ? 'text-emerald-400' : dti <= 50 ? 'text-yellow-400' : 'text-red-400'
                }`}
              >
                {dti}% {dti <= 35 ? '(सुरक्षित)' : '(मध्यम)'}
              </div>
            </div>
          </div>

          <div className="bg-white/10 p-2.5 rounded-lg text-[11px] text-slate-300">
            ℹ️ MoSJE रियायती ब्याज दर के माध्यम से वाणिज्यिक बैंकों की तुलना में लगभग ₹1,20,000 की शुद्ध ब्याज बचत संभव है।
          </div>
        </div>
      </div>
    </div>
  );
};
