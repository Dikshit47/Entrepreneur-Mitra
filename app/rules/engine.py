"""Deterministic, traceable Eligibility Evaluation Engine."""
from typing import Dict, Any, List, Optional
from app.models.scheme import Scheme, SchemeRule
from app.schemas.eligibility import CriterionResult, SchemeEligibilityResult
from app.rules.operators import evaluate_operator


def evaluate_single_rule(
    rule: SchemeRule,
    profile_attributes: Dict[str, Any],
    attribute_sources: Optional[Dict[str, str]] = None
) -> CriterionResult:
    """
    Evaluates a single rule against user profile attributes.
    Traceable, deterministic, zero LLM dependency.
    Distinguishes data trust level: VERIFIED vs USER_PROVIDED.
    """
    field = rule.field_name
    sources = attribute_sources or profile_attributes.get("_attribute_sources", {})
    source_trust = sources.get(field, "USER_PROVIDED")
    
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
            source_id=rule.source_reference_id,
            trust_level="UNKNOWN"
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
        source_id=rule.source_reference_id,
        trust_level=source_trust if source_trust in ["VERIFIED", "USER_PROVIDED", "CONFLICTING"] else "USER_PROVIDED"
    )


def evaluate_scheme_rules(
    scheme: Scheme,
    profile_attributes: Dict[str, Any],
    lang: str = "en"
) -> SchemeEligibilityResult:
    """
    Evaluates all rules of a scheme against user profile attributes.
    Categorizes into hard, soft, and unknown conditions.
    Supports multilingual summary generation: en, hi, hinglish.
    """
    criteria_results: List[CriterionResult] = []
    matched_rules: List[str] = []
    failed_rules: List[str] = []
    missing_info: List[str] = []
    passed_labels: List[str] = []

    hard_failed = False
    hard_unknown = False

    attribute_sources = profile_attributes.get("_attribute_sources", {})

    for rule in scheme.rules:
        res = evaluate_single_rule(rule, profile_attributes, attribute_sources)
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
    norm_lang = (lang or "en").lower()
    if hard_failed:
        status = "NOT_ELIGIBLE"
        if norm_lang == "hi":
            summary = f"अनिवार्य पात्रता शर्तों को पूरा नहीं करता: {', '.join(failed_rules)}"
        elif norm_lang == "hinglish":
            summary = f"Mandatory eligibility requirements poore nahi hue: {', '.join(failed_rules)}"
        else:
            summary = f"Does not satisfy mandatory requirements: {', '.join(failed_rules)}"
    elif hard_unknown:
        status = "INSUFFICIENT_INFORMATION"
        if norm_lang == "hi":
            summary = f"पात्रता सत्यापन के लिए आवश्यक जानकारी अनुपलब्ध है: {', '.join(missing_info)}"
        elif norm_lang == "hinglish":
            summary = f"Eligibility verify karne ke liye zaroori jaankari missing hai: {', '.join(missing_info)}"
        else:
            summary = f"Missing required information to verify eligibility: {', '.join(missing_info)}"
    elif failed_rules:
        # Only soft rules failed
        status = "PARTIALLY_ELIGIBLE"
        if norm_lang == "hi":
            summary = f"मुख्य शर्तें पूरी हैं किंतु कुछ नरम आवश्यकताएं शेष हैं: {', '.join(failed_rules)}"
        elif norm_lang == "hinglish":
            summary = f"Core criteria satisfied hai par soft conditions baaki hain: {', '.join(failed_rules)}"
        else:
            summary = f"Satisfies core criteria but misses soft requirements: {', '.join(failed_rules)}"
    elif missing_info:
        status = "NEEDS_VERIFICATION"
        if norm_lang == "hi":
            summary = f"मुख्य मानदंड पूर्ण हैं; दस्तावेज़ सत्यापन प्रतीक्षित: {', '.join(missing_info)}"
        elif norm_lang == "hinglish":
            summary = f"Core criteria poore hain; documents ya details verify hona baaki hai: {', '.join(missing_info)}"
        else:
            summary = f"Core criteria satisfied; pending documents or details: {', '.join(missing_info)}"
    else:
        status = "ELIGIBLE"
        if norm_lang == "hi":
            summary = "योजना के सभी निर्धारित पात्रता मानदंड पूर्णतः संतुष्ट हैं।"
        elif norm_lang == "hinglish":
            summary = "Scheme ke sabhi official criteria fully satisfy ho gaye hain."
        else:
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
