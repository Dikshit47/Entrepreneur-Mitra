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
