/**
 * Typed API Client for Next.js
 * Communicates with FastAPI backend running on http://127.0.0.1:8000/api/v1
 */

import {
  ApiResponse,
  ProfileOut,
  SchemeOut,
  MatchResponse,
  MatchExplanationOut,
  EMICalculatorRequest,
  EMICalculatorResponse,
  PartnerLocationOut,
  InterviewTurnRequest,
  InterviewTurnResponse,
  EntrepreneurAttributes,
  Language
} from '../types/api';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

async function fetchJson<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    throw new Error(`API request failed with status ${res.status} for ${endpoint}`);
  }
  const payload: ApiResponse<T> = await res.json();
  if (!payload.success && payload.error) {
    throw new Error(payload.error.user_message || payload.error.message);
  }
  return payload.data as T;
}

export const ApiClient = {
  // Profiles
  async createProfile(attributes: EntrepreneurAttributes, language: Language = 'hi'): Promise<ProfileOut> {
    return fetchJson<ProfileOut>('/profiles', {
      method: 'POST',
      body: JSON.stringify({ language, attributes })
    });
  },

  async getProfile(profileId: string): Promise<ProfileOut> {
    return fetchJson<ProfileOut>(`/profiles/${encodeURIComponent(profileId)}`);
  },

  // Schemes & Matching
  async listSchemes(): Promise<SchemeOut[]> {
    return fetchJson<SchemeOut[]>('/schemes');
  },

  async getMatches(profileId: string): Promise<MatchResponse> {
    return fetchJson<MatchResponse>(`/matching/results?profile_id=${encodeURIComponent(profileId)}`);
  },

  async getExplanation(schemeId: string, profileId: string): Promise<MatchExplanationOut> {
    return fetchJson<MatchExplanationOut>(`/matches/${encodeURIComponent(schemeId)}/explanation?profile_id=${encodeURIComponent(profileId)}`);
  },

  // Calculator
  async calculateEmi(calcData: EMICalculatorRequest): Promise<EMICalculatorResponse> {
    return fetchJson<EMICalculatorResponse>('/calculator/emi', {
      method: 'POST',
      body: JSON.stringify(calcData)
    });
  },

  // Partners
  async getNearbyPartners(lat: number, lng: number, category?: string, radiusKm: number = 100): Promise<PartnerLocationOut[]> {
    let url = `/partners/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    return fetchJson<PartnerLocationOut[]>(url);
  },

  // Interview Turns
  async sendTurn(conversationId: string, req: InterviewTurnRequest): Promise<InterviewTurnResponse> {
    return fetchJson<InterviewTurnResponse>(`/interviews/${encodeURIComponent(conversationId)}/turn`, {
      method: 'POST',
      body: JSON.stringify(req)
    });
  }
};
