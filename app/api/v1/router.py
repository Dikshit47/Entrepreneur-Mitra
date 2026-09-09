"""Consolidated API v1 Router."""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.interviews import router as interviews_router
from app.api.v1.schemes import router as schemes_router
from app.api.v1.eligibility import router as eligibility_router
from app.api.v1.matching import router as matching_router
from app.api.v1.calculator import router as calculator_router
from app.api.v1.partners import router as partners_router
from app.api.v1.documents import router as documents_router
from app.api.v1.applications import router as applications_router
from app.api.v1.saved_schemes import router as saved_schemes_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.voice import router as voice_router
from app.api.v1.ai import router as ai_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(profiles_router)
api_v1_router.include_router(interviews_router)
api_v1_router.include_router(schemes_router)
api_v1_router.include_router(eligibility_router)
api_v1_router.include_router(matching_router)
api_v1_router.include_router(calculator_router)
api_v1_router.include_router(partners_router)
api_v1_router.include_router(documents_router)
api_v1_router.include_router(applications_router)
api_v1_router.include_router(saved_schemes_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(voice_router)
api_v1_router.include_router(ai_router)
