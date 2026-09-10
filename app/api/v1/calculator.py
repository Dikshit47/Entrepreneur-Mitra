"""Financial Affordability and EMI Calculator API routes."""
from fastapi import APIRouter
from app.schemas.calculator import EMICalculatorRequest, EMICalculatorResponse
from app.schemas.common import ApiResponse
from app.services.calculator_service import CalculatorService

router = APIRouter(prefix="/calculator", tags=["Financial Calculator"])


@router.post("/emi", response_model=ApiResponse[EMICalculatorResponse])
@router.post("/affordability", response_model=ApiResponse[EMICalculatorResponse])
def calculate_projected_emi(calc_in: EMICalculatorRequest):
    """
    Calculate dynamic projected monthly EMI, total interest, moratorium interest,
    and mandatory promoter contribution (margin money).
    """
    result = CalculatorService.calculate_emi(calc_in)
    return ApiResponse.success_response(result)


from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.eligibility import WhatIfSimulateRequest, WhatIfResultOut
from app.services.eligibility_service import EligibilityService


@router.post("/what-if", response_model=ApiResponse[WhatIfResultOut])
def simulate_calculator_what_if(
    req: WhatIfSimulateRequest,
    db: Session = Depends(get_db)
):
    """Simulate hypothetical financial/eligibility scenario via Calculator."""
    simulation = EligibilityService.simulate_what_if(
        db,
        profile_id=req.profile_id,
        hypothetical_changes=req.get_changes(),
        scheme_id=req.scheme_id
    )
    return ApiResponse.success_response(simulation)
