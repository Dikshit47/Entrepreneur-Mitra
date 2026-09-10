/**
 * API Types and Data Contracts for Entrepreneur Mitra
 * Single Source of Truth matching FastAPI Backend OpenAPI Specs
 */

export type Language = 'hi' | 'en' | 'hinglish';

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: ApiError | null;
  meta: ApiMeta;
}

export interface ApiError {
  code: string;
  message: string;
  user_message?: string;
  retryable: boolean;
  details?: any;
}

export interface ApiMeta {
  request_id: string;
  timestamp: string;
  version: string;
}

export interface EntrepreneurAttributes {
  name?: string;
  age?: number;
  gender?: 'MALE' | 'FEMALE' | 'OTHER';
  caste_category?: 'OBC' | 'SC' | 'ST' | 'DNT' | 'GENERAL';
  annual_income?: number;
  business_type?: string;
  estimated_project_cost?: number;
  state?: string;
  district?: string;
  education?: string;
  prior_training?: boolean;
}

export interface ProfileOut {
  id: string;
  user_id?: string;
  language: Language;
  attributes: EntrepreneurAttributes;
  created_at: string;
  updated_at: string;
}

export interface SchemeOut {
  id: string;
  scheme_code: string;
  scheme_name: string;
  ministry: string;
  description: string;
  scheme_type: string;
  target_group: string;
  max_loan_amount?: number;
  concessional_interest_rate_pct?: number;
  moratorium_months?: number;
  max_tenure_months?: number;
  application_url?: string;
  status: string;
}

export interface SchemeFactorScores {
  target_group: number;
  income_fit: number;
  project_type_fit: number;
  location_fit: number;
  education_fit: number;
  age_fit: number;
}

export interface SchemeMatchResult {
  scheme: SchemeOut;
  match_score: number;
  match_percentage: number;
  is_eligible: boolean;
  rejection_reasons: string[];
  factor_scores: SchemeFactorScores;
}

export interface MatchResponse {
  profile_id: string;
  matches: SchemeMatchResult[];
  evaluated_count: number;
}

export interface CriterionEvaluation {
  criterion_name: string;
  passed: boolean;
  explanation: string;
  official_citation?: string;
}

export interface MatchExplanationOut {
  scheme_id: string;
  scheme_name: string;
  is_eligible: boolean;
  match_score: number;
  criteria_evaluation: CriterionEvaluation[];
  summary: string;
}

export interface EMICalculatorRequest {
  loan_amount: number;
  annual_interest_rate_pct: number;
  tenure_months: number;
  moratorium_months?: number;
  promoter_contribution_pct?: number;
}

export interface EMICalculatorResponse {
  loan_amount: number;
  projected_monthly_emi: number;
  total_interest_payable: number;
  total_repayment_amount: number;
  moratorium_months: number;
  moratorium_simple_interest: number;
  promoter_margin_money: number;
  effective_borrowing_rate: number;
}

export interface PartnerLocationOut {
  id: string;
  name: string;
  partner_type: 'STATE_CHANNELISING_AGENCY' | 'PUBLIC_SECTOR_BANK' | 'REGIONAL_RURAL_BANK' | 'CSC';
  category: string;
  address: string;
  latitude: number;
  longitude: number;
  contact_phone?: string;
  contact_person?: string;
  distance_km?: number;
  is_channel_active: boolean;
}

export interface InterviewTurnRequest {
  user_utterance: string;
  session_id?: string;
  language?: Language;
}

export interface InterviewTurnResponse {
  question_text: string;
  extracted_attributes?: Partial<EntrepreneurAttributes>;
  confidence_scores?: Record<string, number>;
  next_field_target?: string;
  is_complete: boolean;
}
