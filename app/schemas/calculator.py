"""Financial Calculator schemas."""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class EMICalculatorRequest(BaseModel):
    loan_amount: float = Field(..., gt=0, description="Requested principal amount in INR")
    annual_interest_rate: float = Field(..., ge=0, le=30, description="Annual concessional interest rate in %")
    tenure_months: int = Field(..., gt=0, le=240, description="Loan repayment tenure in months")
    moratorium_months: int = Field(default=0, ge=0, le=36, description="Repayment holiday / moratorium in months")
    promoter_contribution_pct: float = Field(default=5.0, ge=0, le=50, description="Promoter own contribution margin %")


class AmortizationScheduleItem(BaseModel):
    month: int
    opening_balance: float
    emi: float
    principal_component: float
    interest_component: float
    closing_balance: float


class EMICalculatorResponse(BaseModel):
    loan_amount: float
    annual_interest_rate: float
    tenure_months: int
    moratorium_months: int
    promoter_contribution_amount: float
    effective_repayment_tenure_months: int
    monthly_emi: float
    total_interest: float
    total_payment: float
    moratorium_interest: float
    disclaimer: str = "Estimated EMI is for guidance only. Final sanction and terms depend on channel partner evaluation."
