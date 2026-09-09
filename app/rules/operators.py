"""Deterministic comparison operators for the Eligibility Engine."""
from typing import Any, Tuple


def _to_numeric(val: Any) -> float:
    """Safely convert value to float, handling strings with currency symbols or commas."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        cleaned = val.replace("₹", "").replace(",", "").replace("L", "00000").replace("lakh", "00000").strip()
        return float(cleaned)
    raise ValueError(f"Cannot convert {val} of type {type(val)} to numeric")


def evaluate_operator(operator: str, user_value: Any, expected_value: Any) -> Tuple[bool, str]:
    """
    Evaluates whether user_value satisfies operator against expected_value.
    Returns (is_satisfied: bool, reason: str).
    """
    op = operator.strip().lower()
    
    # 1. Less than or equal to
    if op in ["<=", "lte", "less_than_or_equal"]:
        try:
            u_num = _to_numeric(user_value)
            e_num = _to_numeric(expected_value)
            passed = u_num <= e_num
            reason = f"User value ({u_num}) is {'<=' if passed else '>'} threshold ({e_num})"
            return passed, reason
        except Exception as e:
            return False, f"Numeric conversion failed: {str(e)}"

    # 2. Greater than or equal to
    if op in [">=", "gte", "greater_than_or_equal"]:
        try:
            u_num = _to_numeric(user_value)
            e_num = _to_numeric(expected_value)
            passed = u_num >= e_num
            reason = f"User value ({u_num}) is {'>=' if passed else '<'} required minimum ({e_num})"
            return passed, reason
        except Exception as e:
            return False, f"Numeric conversion failed: {str(e)}"

    # 3. Less than
    if op in ["<", "lt", "less_than"]:
        try:
            u_num = _to_numeric(user_value)
            e_num = _to_numeric(expected_value)
            passed = u_num < e_num
            reason = f"User value ({u_num}) is {'<' if passed else '>='} threshold ({e_num})"
            return passed, reason
        except Exception as e:
            return False, f"Numeric conversion failed: {str(e)}"

    # 4. Greater than
    if op in [">", "gt", "greater_than"]:
        try:
            u_num = _to_numeric(user_value)
            e_num = _to_numeric(expected_value)
            passed = u_num > e_num
            reason = f"User value ({u_num}) is {'>' if passed else '<='} required ({e_num})"
            return passed, reason
        except Exception as e:
            return False, f"Numeric conversion failed: {str(e)}"

    # 5. Equality
    if op in ["==", "eq", "equal", "="]:
        # If both can be numbers, compare numerically
        try:
            u_num = _to_numeric(user_value)
            e_num = _to_numeric(expected_value)
            passed = u_num == e_num
            return passed, f"Numeric match: {u_num} == {e_num}"
        except Exception:
            pass
        
        # String case-insensitive comparison
        u_str = str(user_value).strip().lower()
        e_str = str(expected_value).strip().lower()
        passed = (u_str == e_str)
        reason = f"Match check: '{user_value}' {'matches' if passed else 'does not match'} '{expected_value}'"
        return passed, reason

    # 6. Inequality
    if op in ["!=", "neq", "not_equal"]:
        u_str = str(user_value).strip().lower()
        e_str = str(expected_value).strip().lower()
        passed = (u_str != e_str)
        return passed, f"Inequality check: '{user_value}' != '{expected_value}'"

    # 7. IN (Membership in comma-separated list or collection)
    if op in ["in", "one_of"]:
        if isinstance(expected_value, str):
            allowed_items = [item.strip().lower() for item in expected_value.split(",")]
        elif isinstance(expected_value, (list, set, tuple)):
            allowed_items = [str(item).strip().lower() for item in expected_value]
        else:
            allowed_items = [str(expected_value).strip().lower()]

        u_str = str(user_value).strip().lower()
        passed = u_str in allowed_items
        reason = f"'{user_value}' {'is allowed in' if passed else 'is not among'} {allowed_items}"
        return passed, reason

    # 8. CONTAINS
    if op in ["contains", "includes"]:
        u_str = str(user_value).strip().lower()
        e_str = str(expected_value).strip().lower()
        passed = (e_str in u_str)
        reason = f"'{expected_value}' {'found in' if passed else 'missing from'} '{user_value}'"
        return passed, reason

    return False, f"Unsupported operator: {operator}"
