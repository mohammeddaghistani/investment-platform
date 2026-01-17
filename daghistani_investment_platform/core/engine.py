from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ValuationInputs:
    selected_act: str
    loc_zone: str
    land_area: float
    tech_risks: int
    pop_current: int
    growth_rate: float
    gdv_m2: float
    capex_m2: float
    term_years: int
    grace_rate: float
    zone_multiplier: float
    profit_factor: float = 1.15

def compute_suitability(tech_risks: int) -> int:
    tech_risks = max(0, min(100, int(tech_risks)))
    return 100 - tech_risks

def compute_future_population(pop: int, growth: float, years: int = 10) -> int:
    return int(pop * ((1 + growth) ** years))

def compute_valuation(inp: ValuationInputs) -> Dict:
    total_gdv = inp.gdv_m2 * inp.land_area
    total_capex = inp.capex_m2 * inp.land_area
    residual_value = (total_gdv - (total_capex * inp.profit_factor)) * inp.zone_multiplier
    base_rent = max(residual_value * 0.08, total_gdv * 0.03)
    grace = int(inp.term_years * inp.grace_rate)
    grace = max(0, min(grace, inp.term_years))
    schedule: List[float] = [0.0] * grace + [base_rent * (1.05 ** (i // 5)) for i in range(inp.term_years - grace)]
    return {
        "total_gdv": total_gdv,
        "total_capex": total_capex,
        "residual_value": residual_value,
        "base_rent": base_rent,
        "grace": grace,
        "schedule": schedule,
        "warning_low_gdv": total_gdv <= total_capex * inp.profit_factor,
    }
