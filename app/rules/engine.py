"""Deterministic, traceable Eligibility Evaluation Engine."""
from typing import Dict, Any, List, Optional
from app.models.scheme import Scheme, SchemeRule
from app.schemas.eligibility import CriterionResult, SchemeEligibilityResult
from app.rules.operators import evaluate_operator


def evaluate_single_rule(rule: SchemeRule, profile_attributes: Dict[str, Any]) -> CriterionResult:
    """
    Evaluates a single rule against user profile attributes.
    Traceable, deterministic, zero LLM dependency.
    """
    field = rule.field_name
    
    # Check if field exists in user's profile
    if field not in profile_attributes or profile_attributes[field] is None:
        return CriterionResult(
            rule_id=rule.rule_id,
            field_name=field,
            operator=rule.operator,
            expected_value=rule.expected_value,
            user_value=None,
            result="UNKNOWN",
            rule_type=rule.rule_type,
            reason=f"Field '{field}' has not been provided in profile yet.",
            source_id=rule.source_reference_id
        )

    user_val = profile_attributes[field]
    
    # Evaluate operator
    passed, reason = evaluate_operator(rule.operator, user_val, rule.expected_value)
    
    return CriterionResult(
        rule_id=rule.rule_id,
        field_name=field,
        operator=rule.operator,
        expected_value=rule.expected_value,
        user_value=user_val,
        result="PASS" if passed else "FAIL",
        rule_type=rule.rule_type,
        reason=reason,
        source_id=rule.source_reference_id
    )


def evaluate_scheme_rules(scheme: Scheme, profile_attributes: Dict[str, Any]) -> SchemeEligibilityResult:
    """
    Evaluates all rules of a scheme against user profile attributes.
    Categorizes into hard, soft, and unknown conditions.
    """
    criteria_results: List[CriterionResult] = []
    matched_rules: List[str] = []
    failed_rules: List[str] = []
    missing_info: List[str] = []
    passed_labels: List[str] = []

    hard_failed = False
    hard_unknown = False

    for rule in scheme.rules:
        res = evaluate_single_rule(rule, profile_attributes)
        criteria_results.append(res)

        if res.result == "PASS":
            matched_rules.append(res.rule_id)
            passed_labels.append(rule.field_name)
        elif res.result == "FAIL":
            failed_rules.append(res.rule_id)
            if rule.rule_type == "hard":
                hard_failed = True
        elif res.result == "UNKNOWN":
            missing_info.append(rule.field_name)
            if rule.rule_type == "hard":
                hard_unknown = True

    # Deterministic State Resolution
    if hard_failed:
        status = "NOT_ELIGIBLE"
        summary = f"Does not satisfy mandatory requirements: {', '.join(failed_rules)}"
    elif hard_unknown:
        status = "INSUFFICIENT_INFORMATION"
        summary = f"Missing required information to verify eligibility: {', '.join(missing_info)}"
    elif failed_rules:
        # Only soft rules failed
        status = "PARTIALLY_ELIGIBLE"
        summary = f"Satisfies core criteria but misses soft requirements: {', '.join(failed_rules)}"
    elif missing_info:
        status = "NEEDS_VERIFICATION"
        summary = f"Core criteria satisfied; pending documents or details: {', '.join(missing_info)}"
    else:
        status = "ELIGIBLE"
        summary = "All published scheme criteria are fully satisfied."

    return SchemeEligibilityResult(
        scheme_id=scheme.scheme_id,
        scheme_name=scheme.name,
        status=status,
        criteria=criteria_results,
        matched_rules=matched_rules,
        failed_rules=failed_rules,
        missing_information=missing_info,
        passed=passed_labels,
        missing=missing_info,
        summary_explanation=summary
    )


def evaluate_all_schemes(schemes: List[Scheme], profile_attributes: Dict[str, Any]) -> List[SchemeEligibilityResult]:
    """Evaluates multiple schemes."""
    return [evaluate_scheme_rules(s, profile_attributes) for s in schemes]
