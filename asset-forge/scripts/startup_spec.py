#!/usr/bin/env python3
"""
ASSET-FORGE · Turnkey Startup Packs — pack specifications
=========================================================
A PARALLEL spec system for the new "0 → profitable in 90–180 day" startup packs
(LEANTA product line). It is deliberately separate from `pack_spec.py` (the
24-pack "operate-an-existing-business" REGISTRY) so that system stays untouched.

It reuses the SAME design layer (`design_system.py`) — the builders in
`startup_build.py` / `grant_build.py` import these specs and emit one premium,
formula-linked `.xlsx` per phase.

Each spec carries:
  · identity + palette + language
  · a single source-of-truth `Assumptions` block (rooms/ADR/occupancy/cost ratios,
    the capex breakdown and the funding mix) — every workbook links to its own
    copy of these so files stay self-contained (no fragile cross-file links)
  · a 15-strong `kpis` catalogue with targets + 🟢🟡🔴 thresholds + sample values
  · phase metadata (number, key, filename, title, subtitle)

Numbers are seeded from the brief and sense-checked against published Irish
4-star/boutique benchmarks; sources are cited in each workbook's Assumptions sheet
(see `startup_build.SOURCES`).
"""
from __future__ import annotations
from dataclasses import dataclass, field


# --------------------------------------------------------------------------- KPI
@dataclass(frozen=True)
class KPI:
    """One dashboard metric with a target and traffic-light thresholds.

    `unit`  : 'pct' (0–1 stored as fraction), 'eur', or 'num'
    `higher_better` : True  → green when value ≥ good, amber ≥ warn, else red
                      False → green when value ≤ good, amber ≤ warn, else red
    `good`/`warn` are the two threshold edges (in the metric's own unit).
    `sample` drives the included worked example so calcs prove out.
    """
    key: str
    label: str
    unit: str
    target: float
    good: float
    warn: float
    higher_better: bool
    sample: float
    note: str = ""


# --------------------------------------------------------------- Assumptions
@dataclass
class Assumptions:
    """Single source of truth for the hotel's operating + funding model."""
    rooms: int
    adr: float                 # average daily rate, €
    occupancy: float           # fraction 0–1
    fb_rev_pct: float          # F&B + other revenue as % of rooms revenue
    # cost ratios (as % of total revenue unless noted)
    payroll_pct: float
    fb_cost_pct: float         # cost of F&B sales as % of F&B revenue
    rooms_cost_pct: float      # housekeeping/laundry/amenities as % of rooms rev
    utilities_pct: float
    sales_mktg_pct: float
    admin_pct: float
    property_pct: float        # rent/insurance/rates as % of total revenue
    # capex breakdown (€) — leased property, so fit-out led
    capex: dict = field(default_factory=dict)
    # funding mix (€)
    funding: dict = field(default_factory=dict)

    @property
    def revpar(self) -> float:
        return round(self.adr * self.occupancy, 2)

    @property
    def rooms_revenue(self) -> float:
        return round(self.rooms * 365 * self.revpar, 0)

    @property
    def total_revenue(self) -> float:
        return round(self.rooms_revenue * (1 + self.fb_rev_pct), 0)

    @property
    def capex_total(self) -> float:
        return float(sum(self.capex.values()))

    @property
    def funding_total(self) -> float:
        return float(sum(self.funding.values()))


# --------------------------------------------------------------- Phase
@dataclass(frozen=True)
class Phase:
    num: str          # "00".."06"
    key: str          # builder key
    filename: str     # output .xlsx name
    title: str
    subtitle: str


# --------------------------------------------------------------- PackSpec
@dataclass
class StartupPackSpec:
    pack_key: str
    vertical: str
    display: str
    industry_dir: str          # e.g. "hospitality/boutique-hotel-4star"
    currency: str
    language: str
    palette: dict
    assumptions: Assumptions
    kpis: list                 # list[KPI]
    phases: list               # list[Phase]
    prefix: str                # filename metric prefix, e.g. "Hotel"


# =====================================================================
# Boutique Hotel · 4-star · 20–30 rooms (pilot)
# =====================================================================
HOTEL_ASSUMPTIONS = Assumptions(
    rooms=24,
    adr=135.0,
    occupancy=0.72,
    fb_rev_pct=0.28,           # F&B + events + other ≈ 28% on top of rooms
    payroll_pct=0.30,
    fb_cost_pct=0.30,
    rooms_cost_pct=0.10,
    utilities_pct=0.05,
    sales_mktg_pct=0.06,
    admin_pct=0.05,
    property_pct=0.12,
    capex={
        "Lease deposit & legal": 45000,
        "Building refurbishment & fit-out": 240000,
        "FF&E (rooms, beds, furniture)": 120000,
        "Kitchen & F&B equipment": 55000,
        "IT, PMS, POS & networking": 30000,
        "Branding, signage & website": 25000,
        "Pre-opening payroll & training": 35000,
        "Working capital buffer": 50000,
    },
    funding={
        "Founder equity (incl. SURE refund)": 180000,
        "LEO Priming grant": 80000,
        "Bank / SBCI term loan": 300000,
        "Microfinance Ireland loan": 40000,
    },
)

HOTEL_KPIS = [
    KPI("occupancy", "Occupancy", "pct", 0.72, 0.70, 0.55, True, 0.74,
        "Rooms sold ÷ rooms available"),
    KPI("adr", "ADR (Avg Daily Rate)", "eur", 135, 130, 110, True, 138,
        "Rooms revenue ÷ rooms sold"),
    KPI("revpar", "RevPAR", "eur", 97, 90, 70, True, 102,
        "ADR × occupancy"),
    KPI("goppar", "GOPPAR", "eur", 45, 40, 25, True, 47,
        "Gross operating profit per available room"),
    KPI("nps", "Guest NPS", "num", 60, 50, 30, True, 58,
        "Net promoter score from guest surveys"),
    KPI("payroll_pct", "Labour cost %", "pct", 0.30, 0.32, 0.40, False, 0.31,
        "Total payroll ÷ total revenue"),
    KPI("fb_cost_pct", "F&B cost %", "pct", 0.30, 0.30, 0.38, False, 0.32,
        "Cost of F&B sales ÷ F&B revenue"),
    KPI("repeat_pct", "Repeat guest %", "pct", 0.25, 0.25, 0.15, True, 0.27,
        "Returning guests ÷ total guests"),
    KPI("alos", "ALOS (nights)", "num", 2.0, 1.8, 1.3, True, 1.9,
        "Average length of stay"),
    KPI("direct_pct", "Direct booking %", "pct", 0.40, 0.40, 0.25, True, 0.38,
        "Direct bookings ÷ total (vs OTA)"),
    KPI("turnaround", "Room turnaround (min)", "num", 30, 30, 45, False, 33,
        "Avg housekeeping turnaround per room"),
    KPI("maint_resp", "Maint. response (hrs)", "num", 4, 4, 12, False, 5,
        "Avg time to resolve a maintenance ticket"),
    KPI("staff_turnover", "Staff turnover %", "pct", 0.25, 0.25, 0.45, False, 0.28,
        "Annualised staff leavers ÷ headcount"),
    KPI("complaints", "Complaints / 100 stays", "num", 3, 3, 7, False, 4,
        "Logged complaints per 100 stays"),
    KPI("collection_pct", "Payment collection %", "pct", 0.98, 0.98, 0.92, True, 0.97,
        "Cash collected ÷ invoiced"),
]

HOTEL_PHASES = [
    Phase("00", "market_validation", "00_Market_Validation.xlsx",
          "Market Validation", "Phase 0 · Is there a viable market for the hotel?"),
    Phase("01", "business_plan", "01_Business_Plan.xlsx",
          "Business Plan", "Phase 1 · Service, model & 3-scenario P&L"),
    Phase("02", "capital_raising", "02_Capital_Raising.xlsx",
          "Capital Raising", "Phase 2 · Capex, funding mix, runway & cash-flow"),
    Phase("03", "procurement", "03_Procurement.xlsx",
          "Procurement", "Phase 3 · Vendors, fit-out budget & purchase orders"),
    Phase("04", "team_building", "04_Team_Building.xlsx",
          "Team Building", "Phase 4 · Org design, hiring & payroll budget"),
    Phase("05", "operations", "05_Operations.xlsx",
          "Operations", "Phase 5 · Daily playbooks & the live KPI dashboard"),
    Phase("06", "launch_100days", "06_Launch_100Days.xlsx",
          "Launch & First 100 Days", "Phase 6 · Soft open → grand open → scorecard"),
]

BOUTIQUE_HOTEL = StartupPackSpec(
    pack_key="boutique_hotel_4star",
    vertical="Boutique Hotel",
    display="Boutique Hotel · 4-Star Turnkey Startup Pack",
    industry_dir="hospitality/boutique-hotel-4star",
    currency="€",
    language="en",
    palette={"primary": "2D6CDF", "accent": "15A38C", "ink": "1A2B45"},
    assumptions=HOTEL_ASSUMPTIONS,
    kpis=HOTEL_KPIS,
    phases=HOTEL_PHASES,
    prefix="Hotel",
)

STARTUP_REGISTRY = {
    "boutique_hotel_4star": BOUTIQUE_HOTEL,
}


# --------------------------------------------------------------- validation
def validate(spec: StartupPackSpec) -> list:
    """Light self-checks mirroring pack_spec.validate()."""
    errs = []
    if len(spec.kpis) < 15:
        errs.append(f"{spec.pack_key}: needs ≥15 KPIs, has {len(spec.kpis)}")
    if len({k.key for k in spec.kpis}) != len(spec.kpis):
        errs.append(f"{spec.pack_key}: duplicate KPI keys")
    if len(spec.phases) != 7:
        errs.append(f"{spec.pack_key}: expected 7 phases, has {len(spec.phases)}")
    a = spec.assumptions
    if abs(a.capex_total - a.funding_total) > 1:
        errs.append(f"{spec.pack_key}: capex {a.capex_total} ≠ funding {a.funding_total}")
    for k in spec.kpis:
        if k.unit not in ("pct", "eur", "num"):
            errs.append(f"{spec.pack_key}: KPI {k.key} bad unit {k.unit}")
    return errs


if __name__ == "__main__":
    for key, spec in STARTUP_REGISTRY.items():
        errs = validate(spec)
        a = spec.assumptions
        print(f"{key}: {len(spec.kpis)} KPIs, {len(spec.phases)} phases")
        print(f"  RevPAR €{a.revpar} · rooms rev €{a.rooms_revenue:,.0f} · "
              f"total rev €{a.total_revenue:,.0f}")
        print(f"  capex €{a.capex_total:,.0f} · funding €{a.funding_total:,.0f}")
        print(f"  validate: {'OK' if not errs else errs}")
