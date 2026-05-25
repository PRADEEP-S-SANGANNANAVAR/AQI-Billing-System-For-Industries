"""
Industrial Air Quality Billing Estimator

This single-file Python module calculates an industry billing amount based on pollutant
measurements and returns a human-readable breakdown / reason for the charge.

Features
- Configurable pollutant thresholds and per-unit exceedance rates
- Base administrative fee
- Severity multipliers for very large exceedances
- Clear textual reasons explaining each charge

Usage example (already included in `if __name__ == "__main__"`):
- Update `attribute_name` and `value` to the live measurements
- Run the script to get `total_amount` and `reason` string

The default thresholds/rates are placeholders and should be tuned to your regulation
or company policy.
"""

from typing import List, Dict, Tuple

# Default configuration (tweak these numbers to match regulation / company policy)
DEFAULT_THRESHOLDS = {
    "no2": 100.0,     # safe limit for NO2 (units must match incoming measurements)
    "CO2": 1000.0,    # safe limit for CO2
    "temp": 20.0,      # safe limit for TEMP
    "humid": 35.0,   # safe limit for HUMID
}

# Per-unit charge for each unit above threshold
DEFAULT_RATES = {
    "co2": 0.5,    # currency units per unit concentration above threshold
    "co": 0.1,
    "temp": 2.0,
    "humid": 1.5,
}

# Base administrative fee (applies even if no exceedance occurs)
DEFAULT_BASE_FEE = 1000.0

# Severity multiplier: if exceedance is more than this factor *threshold, multiply that pollutant's fine
DEFAULT_SEVERITY_FACTOR = 2.0
DEFAULT_SEVERITY_MULTIPLIER = 2.0


def estimate_billing(attribute_name: List[str],
                     values: List[float],
                     thresholds: Dict[str, float] = None,
                     rates: Dict[str, float] = None,
                     base_fee: float = None,
                     severity_factor: float = None,
                     severity_multiplier: float = None) -> Tuple[float, str]:
    """Estimate billing amount and return (total_amount, reason_text).

    - attribute_name: list of pollutant names (must match keys in thresholds/rates)
    - values: corresponding numeric measurements
    - thresholds, rates, base_fee, severity_factor, severity_multiplier are optional overrides

    Returns:
        total_amount (float): total billing amount (rounded to 2 decimals)
        reason_text (str): detailed breakdown and reason for the billing
    """

    thresholds = thresholds or DEFAULT_THRESHOLDS
    rates = rates or DEFAULT_RATES
    base_fee = base_fee if base_fee is not None else DEFAULT_BASE_FEE
    severity_factor = severity_factor if severity_factor is not None else DEFAULT_SEVERITY_FACTOR
    severity_multiplier = severity_multiplier if severity_multiplier is not None else DEFAULT_SEVERITY_MULTIPLIER

    if len(attribute_name) != len(values):
        raise ValueError("attribute_name and values must have the same length")

    total = base_fee
    reasons = [f"Base administrative fee: {base_fee:.2f}"]

    for name, val in zip(attribute_name, values):
        key = name.lower().strip()
        thr = thresholds.get(key)
        rate = rates.get(key)

        if thr is None or rate is None:
            reasons.append(f"Skipping '{name}': no threshold/rate configured.")
            continue

        exceed = val - thr
        if exceed <= 0:
            reasons.append(f"{name}: {val} (within limit {thr}) — no charge.")
            continue

        pollutant_charge = exceed * rate
        applied_multiplier = 1.0

        # Apply severity multiplier for very large exceedances
        if exceed > severity_factor * thr:
            applied_multiplier = severity_multiplier
            pollutant_charge *= applied_multiplier

        total += pollutant_charge

        # Build human-readable reason for this pollutant
        reason_line = (f"{name}: measured {val:.2f} vs limit {thr:.2f} -> exceed {exceed:.2f};"
                       f" rate {rate:.2f} => charge {pollutant_charge:.2f}")
        if applied_multiplier != 1.0:
            reason_line += f" (severity multiplier x{applied_multiplier})"

        reasons.append(reason_line)

    reason_text = "\n".join(reasons)
    return round(total, 2), reason_text


if __name__ == "__main__":
    # Example input (the values you gave in the prompt)
    attribute_name = ["co2", "co", "Temp", "humid "]
    value = [2768.0, 182.0, 28.2, 53.7]

    total_amount, reason = estimate_billing(attribute_name, value)
    print("Total billing amount:", total_amount)
    print("Reason / breakdown:\n", reason)



