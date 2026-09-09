"""Eligibility Service coordinating the rule evaluation and what-if simulation."""
from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from app.models.scheme import Scheme
from app.models.audit import EligibilityEvaluation
from app.schemas.eligibility import SchemeEligibilityResult, WhatIfResultOut
from app.services.profile_service import ProfileService
from app.rules.engine import evaluate_scheme_rules
from app.utils.exceptions import NotFoundException


class EligibilityService:
    @staticmethod
    def evaluate_schemes_for_profile(
        db: Session,
        profile_id: str,
        scheme_ids: Optional[List[str]] = None
    ) -> List[SchemeEligibilityResult]:
        # 1. Fetch profile
        profile = ProfileService.get_profile(db, profile_id)
        attributes = profile.attributes

        # 2. Fetch schemes with rules
        query = db.query(Scheme).options(joinedload(Scheme.rules)).filter(Scheme.status == "ACTIVE")
        if scheme_ids:
            query = query.filter(Scheme.scheme_id.in_(scheme_ids))
        schemes = query.all()

        results = []
        for scheme in schemes:
            eval_res = evaluate_scheme_rules(scheme, attributes)
            results.append(eval_res)

            # Store audit record
            trace = EligibilityEvaluation(
                profile_id=profile_id,
                scheme_id=scheme.scheme_id,
                decision=eval_res.status,
                rule_trace_json=json.dumps([c.model_dump() for c in eval_res.criteria]),
                engine_version="v1.0"
            )
            db.add(trace)
        
        db.commit()
        return results

    @classmethod
    def simulate_what_if(
        cls,
        db: Session,
        profile_id: str,
        hypothetical_changes: Dict[str, Any],
        scheme_id: Optional[str] = None
    ) -> WhatIfResultOut:
        # Fetch current profile
        profile = ProfileService.get_profile(db, profile_id)
        original_attributes = profile.attributes.copy()

        # Build hypothetical attributes without altering database!
        simulated_attributes = original_attributes.copy()
        simulated_attributes.update(hypothetical_changes)

        # Target scheme: if not specified, pick the first active scheme
        query = db.query(Scheme).options(joinedload(Scheme.rules)).filter(Scheme.status == "ACTIVE")
        if scheme_id:
            scheme = query.filter(Scheme.scheme_id == scheme_id).first()
        else:
            scheme = query.first()

        if not scheme:
            raise NotFoundException(resource="Scheme", identifier=scheme_id or "default")

        # Evaluate original vs simulated
        original_res = evaluate_scheme_rules(scheme, original_attributes)
        simulated_res = evaluate_scheme_rules(scheme, simulated_attributes)

        # Detect changed rules
        changed_rules = []
        orig_map = {c.rule_id: c.result for c in original_res.criteria}
        for sim_crit in simulated_res.criteria:
            orig_result = orig_map.get(sim_crit.rule_id)
            if orig_result != sim_crit.result:
                changed_rules.append(sim_crit.rule_id)

        # Build plain language explanation
        if original_res.status != simulated_res.status:
            explanation = (
                f"Agar aapki details badalti hain, to eligibility status '{original_res.status}' se badalkar "
                f"'{simulated_res.status}' ho jayega. Badle huye rules: {', '.join(changed_rules) if changed_rules else 'None'}."
            )
        else:
            explanation = (
                f"Diye gaye badlav se status '{original_res.status}' par koi prabhav nahi pada. "
                "Kripya anya eligibility shartein jaanchein."
            )

        return WhatIfResultOut(
            is_hypothetical=True,
            profile_id=profile_id,
            scheme_id=scheme.scheme_id,
            original={"decision": original_res.status, "passed": original_res.passed, "missing": original_res.missing},
            simulated={"decision": simulated_res.status, "passed": simulated_res.passed, "missing": simulated_res.missing},
            changed_rules=changed_rules,
            explanation=explanation
        )
