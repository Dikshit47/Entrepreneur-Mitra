"""Financial Affordability Calculator service."""
from app.schemas.calculator import EMICalculatorRequest, EMICalculatorResponse


class CalculatorService:
    @staticmethod
    def calculate_emi(req: EMICalculatorRequest) -> EMICalculatorResponse:
        P = req.loan_amount
        annual_rate = req.annual_interest_rate
        total_tenure = req.tenure_months
        moratorium = req.moratorium_months
        margin_pct = req.promoter_contribution_pct

        # Promoter margin money
        margin_amount = round((P * margin_pct) / 100.0, 2)

        # Repayment tenure
        effective_tenure = max(1, total_tenure - moratorium)

        # Monthly interest rate
        monthly_rate = (annual_rate / 12.0) / 100.0

        # Simple interest during moratorium (repayment holiday)
        moratorium_interest = round(P * monthly_rate * moratorium, 2) if moratorium > 0 else 0.0

        if monthly_rate == 0:
            monthly_emi = round(P / effective_tenure, 2)
            total_interest = 0.0
        else:
            # Standard Amortization: P * r * (1+r)^n / ((1+r)^n - 1)
            num = P * monthly_rate * ((1.0 + monthly_rate) ** effective_tenure)
            den = ((1.0 + monthly_rate) ** effective_tenure) - 1.0
            monthly_emi = round(num / den, 2)
            total_interest = round((monthly_emi * effective_tenure) - P + moratorium_interest, 2)

        total_payment = round(P + total_interest, 2)

        return EMICalculatorResponse(
            loan_amount=P,
            annual_interest_rate=annual_rate,
            tenure_months=total_tenure,
            moratorium_months=moratorium,
            promoter_contribution_amount=margin_amount,
            effective_repayment_tenure_months=effective_tenure,
            monthly_emi=monthly_emi,
            total_interest=max(0.0, total_interest),
            total_payment=total_payment,
            moratorium_interest=moratorium_interest,
            disclaimer="Estimated EMI is for guidance only. Final sanction and interest subvention depend on channel partner terms."
        )
