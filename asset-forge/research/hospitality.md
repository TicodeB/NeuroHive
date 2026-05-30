# Research — HOSPITALITY (Phase 1)

**Vertical:** Hospitality · **Business types:** Bar/pub · Café/coffee shop ·
Restaurant · B&B/guesthouse · Hotel
**Context:** EU (Ireland) seller. Metric units, DD/MM/YYYY, EU thousands
separators. **Buyer dimension** tagged per asset: operator / auditor /
consultant.

> **Method note (brief [7]):** for each business type we answer the 5 research
> questions, then score every asset×business-type pairing on the rubric [6]
> (Legal·3 + Revenue·2 + Pain·2 + Frequency·1, max 24) and store the **raw axis
> scores** in `intelligence.db` (`asset_map`). Legal-mandatory items (Legal=3)
> auto-promote to MUST regardless of score. Rows + evidence are captured now;
> the bulk tier finalisation/cross-check happens in Phase 5 via `classify.py`.

---

## 0. The regulatory MUST-floor (applies across all five business types)

These set Legal=3 (or 2) and define the non-negotiable assets. Verified live:

- **Food safety management based on HACCP** is a legal requirement for every
  food business in Ireland (Reg. (EC) 852/2004). A documented system —
  prerequisite programmes, temperature control, cleaning, traceability — must be
  kept. → HACCP system, temperature logs, cleaning schedule, traceability log =
  **Legal=3**. [FSAI — starting a food business](https://www.fsai.ie/business-advice/starting-a-food-business/business-start-up-information-factsheet)
- **Allergen declaration** for non-prepacked food is mandatory under
  Reg. (EU) 1169/2011 (FIC), implemented in Ireland by S.I. 489/2014 (updated by
  S.I. 656/2024) — applies to restaurants, cafés, bars, takeaways. 14 allergens
  must be declared. → Allergen matrix/declaration tool = **Legal=3**.
  [FSAI — allergens for business](https://www.fsai.ie/business-advice/running-a-food-business/allergens)
- **Safety statement + risk assessment** is mandatory for every employer under
  Section 19, Safety, Health and Welfare at Work Act 2005. → H&S risk
  assessment / safety statement / incident log = **Legal=3**.
  [HSA — safety statement & risk assessment](https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/)
- **Fire safety + emergency arrangements** are a statutory duty; HSA publishes
  hospitality-specific law guidance (hotels, restaurants, catering & bars). →
  Fire safety register/checks log = **Legal=3**.
  [HSA — catering & hospitality, the law](https://www.hsa.ie/eng/your_industry/catering_and_hospitality/the_law/)
- **Accommodation (B&B/guesthouse/hotel)** calling itself a guest house must be
  registered with Fáilte Ireland under the Tourist Traffic Acts 1939–2016, and
  self-declare compliance with statutory obligations under the Welcome Standard.
  → guest register and accommodation-quality assets gain a Legal/expected
  weighting. [Fáilte Ireland — guesthouses](https://www.failteireland.ie/Supports/registration-and-grading/national-quality-assurance-framework/Guest-Houses.aspx) ·
  [Welcome Standard](https://www.failteireland.ie/welcomestandard.aspx)

> Because all five hospitality business types serve food (a bar serves food, a
> B&B serves breakfast, a hotel runs a kitchen), the food-safety MUST-floor
> applies to **all five**.

---

## 1. Bar / pub

**Departments active (even informally):** Operations, Quality & Compliance
(HACCP, H&S, fire), Procurement & Inventory (cellar/stock), Finance (takings,
GP, cashflow), HR (rota, training), Front-of-house, Maintenance (cellar/lines),
Reporting.

**Recurring record-producing workflows:** opening/closing stock counts & wastage;
cellar/beer-line cleaning; till Z-read & cash banking; staff rota & wage cost;
temperature & cleaning logs; H&S/fire checks.

**Assets + scoring rationale:**
- HACCP system, temperature log, cleaning schedule, traceability log → **MUST**
  (Legal=3; bars serving food are food businesses).
- H&S risk assessment, fire safety register → **MUST** (Legal=3).
- **Stock & wastage tracker** → SHOULD (R3/P3/F3): shrinkage and over-pour are
  the classic profit leak; EPOS stock modules exist but owners complain they are
  complex and contract-locked (below).
- **Cashflow & P&L tracker** → SHOULD. **Daily takings/till reconciliation** →
  SHOULD. **Beer-line cleaning log** → SHOULD (quality + hygiene; ~weekly).
- **Recipe/drink GP costing** → COULD. **Booking diary**, **feedback tracker** →
  COULD.

**Top pain points:** stock shrinkage/wastage & GP erosion; till variances vs
banking; expensive, hard-to-exit EPOS contracts; line-cleaning discipline.

**Existing tools & gaps:** Epos Now and similar offer stock control but reviewers
report complex UIs ("too many tabs/buttons"), no training mode, long support
waits, and £89/mo surcharges + lengthy contracts that are hard to exit.
[Capterra — Epos Now reviews](https://www.capterra.com/p/152638/Epos-Now/reviews/) ·
[Startups — best pub/bar POS 2026](https://startups.co.uk/payment-processing/best-pos-systems-bars-and-pubs/)

---

## 2. Café / coffee shop

**Departments active:** Operations, Quality & Compliance, Procurement, Finance,
HR, Front-of-house, Reporting.

**Recurring workflows:** allergen declarations for bakery/deli items; temp &
cleaning logs; daily takings; ingredient costing for menu pricing; staff rota.

**Assets + scoring rationale:**
- Allergen matrix → **MUST** and HACCP/temp/cleaning/traceability → **MUST**
  (Legal=3) — cafés handle high-allergen baked/deli items, so allergen accuracy
  is acute (Pain=3).
- H&S + fire → **MUST** (Legal=3).
- **Recipe/menu GP costing** → SHOULD (tight margins on food + coffee).
- **Cashflow & P&L**, **takings reconciliation**, **stock tracker**, **rota**,
  **training matrix** → SHOULD.
- Feedback tracker → COULD.

**Top pain points:** allergen accuracy on a changing daily-specials menu;
thin margins; wastage on fresh/perishable stock; pricing guesswork.

---

## 3. Restaurant

**Departments active:** all ten, most intensively. Highest asset density of the
five.

**Recurring workflows:** HACCP CCP monitoring; allergen control across a full
menu; recipe costing & menu engineering; covers forecasting & reservations;
rota & labour-cost %; stock & wastage; supplier traceability.

**Assets + scoring rationale:**
- HACCP, allergen matrix, temp, cleaning, traceability → **MUST** (Legal=3,
  Pain=3 — a restaurant is the highest-stakes food operation).
- H&S + fire → **MUST** (Legal=3).
- **Recipe/menu GP costing** → SHOULD (R3/P3 — menu engineering is the main
  margin lever). **Staff rota & labour-cost** → SHOULD (R3/P3/F3). **Stock &
  wastage** → SHOULD. **Cashflow & P&L** → SHOULD. **Table booking & covers
  diary** → SHOULD. **Training matrix** → SHOULD. **Takings reconciliation** →
  SHOULD.
- Maintenance register, event quote generator, feedback tracker → COULD.

**Top pain points:** food-cost % / GP erosion; labour-cost % vs covers; no-shows
on reservations; allergen liability; food waste.

**Buyer-dimension capture:** HACCP system also sells to the **consultant** who
builds it for clients (MUST), and the allergen matrix is what the **auditor**/EHO
inspects (MUST) — the same premise generates demand from both sides of the audit.

---

## 4. B&B / guesthouse

**Departments active:** Operations (rooms + breakfast), Quality & Compliance
(food safety for breakfast service, fire, H&S), Front-of-house/Bookings, Finance,
Maintenance.

**Recurring workflows:** room bookings & occupancy; guest check-in/register;
breakfast food-safety (HACCP-lite); fire/H&S checks; simple cashflow.

**Assets + scoring rationale:**
- HACCP/temp/cleaning/traceability for breakfast service → **MUST** (Legal=3;
  scaled to a small kitchen).
- H&S + fire → **MUST** (Legal=3).
- **Room bookings & occupancy dashboard** → SHOULD (R3/P3/F3 — direct-booking
  vs OTA management is the core revenue workflow). **Guest register & check-in
  log** → SHOULD (expected for a registered premises). **Cashflow & P&L** →
  SHOULD.
- Stock tracker, rota, feedback tracker, maintenance register → COULD (solo/
  small operation, low frequency).

**Top pain points:** OTA commission vs direct bookings; occupancy/seasonality
cashflow; meeting Fáilte Welcome Standard expectations; double-bookings.

---

## 5. Hotel

**Departments active:** all ten, at the largest scale — includes a restaurant/
bar AND accommodation, so it inherits both food-service and accommodation MUSTs.

**Recurring workflows:** everything in restaurant + accommodation; PPM/maintenance
across rooms & plant; function/event sales; RevPAR/ADR reporting; multi-department
rota.

**Assets + scoring rationale:**
- All food-safety MUSTs (HACCP/allergen/temp/cleaning/traceability) → **MUST**
  (Legal=3). H&S + fire → **MUST** (Legal=3; fire pain is highest given guest
  volume/overnight occupancy).
- **Room bookings & occupancy dashboard** (RevPAR/ADR) → SHOULD. **Guest
  register** → SHOULD. **Stock & wastage** → SHOULD. **Rota & labour-cost** →
  SHOULD. **Cashflow & P&L** → SHOULD. **Maintenance & PPM register** → SHOULD.
  **Function/event quote generator** → SHOULD (functions are high-margin
  revenue).
- Recipe costing, takings reconciliation, feedback tracker, beer-line log →
  COULD.

**Top pain points:** revenue management (RevPAR/ADR) across channels; preventive
maintenance across rooms/plant; coordinating multi-department rotas to labour %;
function/event quoting speed.

---

## Cross-cutting observations (feeds Phase 6/7)

- **Universal-core candidates** (MUST across all five → build once, sell many):
  HACCP system, allergen matrix, temperature log, cleaning schedule, traceability
  log, H&S risk assessment, fire safety register. These are the highest-leverage
  hospitality products and the first shippable should sit on one of them.
- **Highest willingness-to-pay "wanted" assets** (SHOULD): stock & wastage
  tracker, GP/menu-costing calculator, staff rota & labour-cost scheduler,
  cashflow & P&L tracker, room-occupancy dashboard — desired (not dreaded), and
  the competitor gap (complex/expensive EPOS) is real.
- **EU VAT** on digital goods sold to EU buyers is in scope for the Ireland-based
  seller — flagged for the Phase 8 monetization decision.

## Sources
- [FSAI — starting a food business / HACCP](https://www.fsai.ie/business-advice/starting-a-food-business/business-start-up-information-factsheet)
- [FSAI — allergens for business (Reg 1169/2011, S.I. 489/2014)](https://www.fsai.ie/business-advice/running-a-food-business/allergens)
- [HSA — safety statement & risk assessment (S.19 Act 2005)](https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/)
- [HSA — catering & hospitality: the law](https://www.hsa.ie/eng/your_industry/catering_and_hospitality/the_law/)
- [Fáilte Ireland — guesthouses (registration)](https://www.failteireland.ie/Supports/registration-and-grading/national-quality-assurance-framework/Guest-Houses.aspx)
- [Fáilte Ireland — Welcome Standard](https://www.failteireland.ie/welcomestandard.aspx)
- [Capterra — Epos Now reviews (gaps)](https://www.capterra.com/p/152638/Epos-Now/reviews/)
- [Startups — best pub/bar POS systems 2026 (gaps)](https://startups.co.uk/payment-processing/best-pos-systems-bars-and-pubs/)
- [7shifts — free restaurant management templates (price/benchmark)](https://www.7shifts.com/resources/templates/)
- [Etsy — staff rota templates (price benchmark)](https://www.etsy.com/market/staff_rota_template)
