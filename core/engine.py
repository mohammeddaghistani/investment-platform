from dataclasses import dataclass

@dataclass
class ValuationInputs:
    land_area: float
    gdv_m2: float
    capex_m2: float
    term_years: int
    grace_rate: float
    zone_multiplier: float
    profit_factor: float = 1.15

def compute_valuation(inp: ValuationInputs):
    total_gdv = inp.gdv_m2 * inp.land_area
    total_capex = inp.capex_m2 * inp.land_area
    residual = (total_gdv - (total_capex * inp.profit_factor)) * inp.zone_multiplier
    base_rent = max(residual * 0.08, total_gdv * 0.03)
    grace = int(inp.term_years * inp.grace_rate)
    schedule = [0]*grace + [base_rent * (1.05 ** (i // 5)) for i in range(inp.term_years - grace)]
    return {
        "total_gdv": total_gdv,
        "total_capex": total_capex,
        "residual": residual,
        "base_rent": base_rent,
        "grace": grace,
        "schedule": schedule
    }
