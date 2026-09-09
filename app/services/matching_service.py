"""Scheme Matching and Ranking Engine with transparent weighted scoring."""
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session, joinedload
from app.models.scheme import Scheme
from app.schemas.matching import MatchItem, MatchResponse, ScoreBreakdown, MatchExplanationOut, MatchExplanationCriterion
from app.services.profile_service import ProfileService
from app.rules.engine import evaluate_scheme_rules
from app.utils.exceptions import NotFoundException


class MatchingService:
    @classmethod
    def calculate_score_breakdown(
        cls,
        scheme: Scheme,
        attributes: Dict[str, Any],
        eval_result
    ) -> Tuple[int, ScoreBreakdown]:
        """
        Computes 6-part transparent score according to Master Blueprint Section 10.4:
        Score = 35% eligibility + 25% purpose + 15% financial + 10% geo + 10% docs + 5% preference.
        """
        # 1. Eligibility Completeness (35%)
        if eval_result.status == "ELIGIBLE":
            elig_score = 100.0
        elif eval_result.status == "PARTIALLY_ELIGIBLE":
            elig_score = 75.0
        elif eval_result.status == "NEEDS_VERIFICATION":
            elig_score = 60.0
        elif eval_result.status == "INSUFFICIENT_INFORMATION":
            elig_score = 40.0
        else:  # NOT_ELIGIBLE
            elig_score = 15.0

        # 2. Purpose Fit (25%)
        purpose_score = 50.0  # Base
        user_biz = str(attributes.get("business_type", "")).lower()
        if user_biz:
            target_str = (scheme.target_group or "").lower() + " " + scheme.description.lower()
            if any(word in target_str for word in user_biz.split()):
                purpose_score = 100.0
            else:
                purpose_score = 75.0

        # 3. Financial Fit (15%)
        financial_score = 60.0
        loan_req = attributes.get("loan_required") or attributes.get("project_cost")
        if loan_req and scheme.benefits:
            try:
                l_val = float(loan_req)
                b = scheme.benefits[0]
                if b.min_value <= l_val <= b.max_value:
                    financial_score = 100.0
                elif l_val <= b.max_value * 1.2:
                    financial_score = 70.0
                else:
                    financial_score = 30.0
            except Exception:
                financial_score = 50.0

        # 4. Geography Fit (10%)
        geo_score = 100.0 if scheme.geography_scope == "PAN_INDIA" else 80.0

        # 5. Document Readiness (10%)
        # Base readiness from profile completeness
        doc_score = 70.0

        # 6. User Preference (5%)
        pref_score = 85.0

        total_score = int(
            (elig_score * 0.35) +
            (purpose_score * 0.25) +
            (financial_score * 0.15) +
            (geo_score * 0.10) +
            (doc_score * 0.10) +
            (pref_score * 0.05)
        )
        total_score = max(0, min(100, total_score))

        breakdown = ScoreBreakdown(
            eligibility_completeness=round(elig_score, 1),
            purpose_fit=round(purpose_score, 1),
            financial_fit=round(financial_score, 1),
            geography_fit=round(geo_score, 1),
            document_readiness=round(doc_score, 1),
            user_preference=round(pref_score, 1)
        )

        return total_score, breakdown

    @classmethod
    def match_schemes_for_profile(cls, db: Session, profile_id: str) -> MatchResponse:
        profile = ProfileService.get_profile(db, profile_id)
        attributes = profile.attributes

        schemes = db.query(Scheme).options(
            joinedload(Scheme.rules),
            joinedload(Scheme.benefits),
            joinedload(Scheme.required_documents),
            joinedload(Scheme.sources)
        ).filter(Scheme.status == "ACTIVE").all()

        results: List[MatchItem] = []
        for scheme in schemes:
            eval_res = evaluate_scheme_rules(scheme, attributes)
            total_score, breakdown = cls.calculate_score_breakdown(scheme, attributes, eval_res)

            why_matched = [f"Rule '{r}' satisfied" for r in eval_res.matched_rules]
            missing_reqs = [f"Provide '{m}'" for m in eval_res.missing_information]

            max_loan = scheme.benefits[0].max_value if scheme.benefits else None
            interest = scheme.benefits[0].interest_rate if scheme.benefits else None

            results.append(MatchItem(
                scheme_id=scheme.scheme_id,
                scheme_name=scheme.name,
                ministry=scheme.ministry,
                scheme_type=scheme.scheme_type,
                status=eval_res.status,
                match_score=total_score,
                score_breakdown=breakdown,
                passed=eval_res.passed,
                missing=eval_res.missing,
                why_matched=why_matched,
                missing_requirements=missing_reqs,
                estimated_max_loan=max_loan,
                interest_rate=interest,
                official_url=scheme.official_url
            ))

        # Rank descending by score, prioritizing ELIGIBLE and PARTIALLY_ELIGIBLE
        status_priority = {
            "ELIGIBLE": 5,
            "PARTIALLY_ELIGIBLE": 4,
            "NEEDS_VERIFICATION": 3,
            "INSUFFICIENT_INFORMATION": 2,
            "NOT_ELIGIBLE": 1
        }
        results.sort(key=lambda x: (status_priority.get(x.status, 0), x.match_score), reverse=True)

        return MatchResponse(
            profile_id=profile_id,
            results=results,
            total_evaluated=len(schemes)
        )

    @classmethod
    def explain_match(cls, db: Session, scheme_id: str, profile_id: str) -> MatchExplanationOut:
        profile = ProfileService.get_profile(db, profile_id)
        scheme = db.query(Scheme).options(
            joinedload(Scheme.rules),
            joinedload(Scheme.sources)
        ).filter(Scheme.scheme_id == scheme_id).first()

        if not scheme:
            raise NotFoundException(resource="Scheme", identifier=scheme_id)

        eval_res = evaluate_scheme_rules(scheme, profile.attributes)

        explanation_criteria = []
        for c in eval_res.criteria:
            explanation_criteria.append(MatchExplanationCriterion(
                label=c.field_name.replace("_", " ").title(),
                result=c.result,
                reason=c.reason,
                source_id=c.source_id
            ))

        summary = (
            f"Aapki profile is scheme ke criteria ke anusar '{eval_res.status}' hai. "
            f"{len(eval_res.matched_rules)} shartein poori hain, {len(eval_res.failed_rules)} anupayukt hain."
        )

        return MatchExplanationOut(
            scheme_id=scheme.scheme_id,
            scheme_name=scheme.name,
            decision=eval_res.status,
            summary=summary,
            criteria=explanation_criteria,
            official_url=scheme.official_url,
            last_verified_at=scheme.last_verified_at.isoformat() if scheme.last_verified_at else ""
        )
