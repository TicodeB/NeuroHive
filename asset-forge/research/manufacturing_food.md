# Research — FOOD MANUFACTURING (Phase 2)

**Vertical:** Food manufacturing · **Business types:** Bakery, Butchery/meat, Dairy,
Beverage, Ready meals/catering production (business_type ids 6–10).
**Context:** EU / Ireland seller. Metric units, EU dates (DD/MM/YYYY), comma thousands.
**Method:** Brief Section [7] — 5 questions per business type, scored to rubric [6],
buyer dimension tagged, every MUST/SHOULD row carries an `evidence_url`.

> Dedupe rule honoured: where a hospitality asset already covers the same *function*
> (HACCP system, temperature log, cleaning schedule, supplier/incoming traceability,
> H&S safety statement, fire register, maintenance/PPM, training matrix, cashflow/P&L),
> Phase 2 **reuses the existing `digital_assets` row** rather than re-creating it. Only
> genuinely new manufacturing functions get new asset rows.

---

## [A] REGULATORY MUST-FLOOR (verified LIVE, not from memory)

The legal floor is what auto-promotes assets to MUST (rubric [6], Legal = 3). For food
manufacturing the floor is **broader and harder** than hospitality because manufacturers
place *prepacked* product on the market for other businesses.

| Obligation | Who it binds | Source (verified 29/05/2026) |
|---|---|---|
| **HACCP-based food safety management** (Reg (EC) 852/2004) | all 5 types | [FSAI — Starting a Food Business](https://www.fsai.ie/business-advice/starting-a-food-business/business-start-up-information-factsheet) |
| **Approval of establishments handling products of animal origin** (Reg (EC) 853/2004) — approval number + health/identification mark; retail butcher has a *marginal, localised, restricted* exemption | **Butchery/meat, Dairy** | [FSAI — Specific Hygiene Rules for Food of Animal Origin](https://www.fsai.ie/enforcement-and-legislation/legislation/food-legislation/food-hygiene/specific-hygiene-rules-for-food-of-animal-origin) · [FSAI — Approval of Food Establishments (PDF)](https://www.fsai.ie/getattachment/380ffd12-a55b-42eb-b434-5dcd8acca1b6/final-guidance-on-the-approval-of-food-establishments.pdf?lang=en-IE&ext=.pdf) |
| **Identification / health marking** of products of animal origin | Butchery/meat, Dairy | [FSAI — Identification marking and labelling](https://www.fsai.ie/enforcement-and-legislation/legislation/food-legislation/meat-fresh-meat/identification-marking-and-labelling) |
| **Food information / labelling incl. mandatory nutrition declaration** (Reg (EU) 1169/2011, mandatory since 13/12/2016; per 100 g/ml, tabular, English) — **alcoholic drinks are exempt from nutrition** but still declare allergens (e.g. sulphites) | Bakery, Dairy, Beverage (soft), Ready meals | [FSAI — Nutrition Labelling](https://www.fsai.ie/business-advice/labelling/labelling-nutrition-information/nutrition-labelling) · [FSAI — Food Information to Consumers](https://www.fsai.ie/business-advice/labelling/food-information-to-consumers) |
| **Allergen declaration** (14 EU allergens, Reg 1169/2011) | all that label food | [FSAI — Allergens](https://www.fsai.ie/business-advice/running-a-food-business/allergens) |
| **Traceability one-step-back/forward + withdrawal/recall capability** (Reg (EC) 178/2002, Arts 18–19) | all 5 types | [FSAI — Starting a Food Business](https://www.fsai.ie/business-advice/starting-a-food-business/business-start-up-information-factsheet) |
| **Net-quantity / average-quantity control + 'e' mark** (Packaged Goods (Quantity Control) Act 1980; Metrology Act 1996; NSAI Legal Metrology) | any prepacked good sold by quantity (esp. Bakery, Beverage, Dairy, Ready meals) | [NSAI — Control of Packaged Goods](https://www.nsai.ie/legal-metrology/control-of-quantities/) · [NSAI — e-mark](https://www.nsai.ie/legal-metrology/enforcement-information/inspection-types/packaged-good-inspection/emark/) |
| **Safety Statement + risk assessment** (S.19, Safety, Health & Welfare at Work Act 2005) and **fire safety** statutory duty | all 5 (employers) | [HSA — Safety Statement & Risk Assessment](https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/) |

**Voluntary-but-commercially-decisive standards (retail-supply gateway):** BRCGS Food
Safety, IFS Food, FSSC 22000, **SALSA** (small producers). Not law, but a retailer/
foodservice buyer will refuse to list an unaccredited supplier — so the underlying
documents (GMP self-inspection, supplier approval, calibration, foreign-body control)
are SHOULD-tier with high willingness-to-pay. Mapped in depth in the Phase 10 bonus track.

---

## [B] BUSINESS-TYPE DEEP DIVES (5 questions each)

### 6 — Bakery
1. **Departments (even informal):** Production (mixing/proving/baking), Quality &
   Compliance (HACCP, allergens, labelling), Procurement & Inventory (flour/fats/yeast),
   Finance (batch costing, cashflow), Sales/CRM (wholesale + counter), Maintenance (ovens/mixers).
2. **Recurring record-producing workflows:** daily batch/production runs with yield &
   wastage; ingredient goods-in + FIFO rotation; allergen cross-contact control
   (gluten/wheat/nuts/egg/milk dominate); prepacked label + nutrition generation;
   net-weight checks on packaged loaves; short shelf-life / date-coding.
3. **Assets per workflow (scored in DB):** Batch Production & Yield Record, Recipe/BOM &
   Batch Costing, Product Label & Nutrition Generator (legal), Net-Quantity/e-mark Sheet
   (legal), Shelf-Life & Date-Coding Record, Raw-Material FIFO Inventory, plus reused
   HACCP/Allergen/Temp/Cleaning/Traceability/H&S/Fire.
4. **Top pain points:** wafer-thin margins destroyed by un-costed recipes and ingredient
   price swings; allergen accuracy on a wide SKU range; daily wastage of unsold short-life
   stock; manual label/nutrition creation per SKU is slow and error-prone.
5. **Existing tools & gaps:** generic ERP/bakery software (e.g. recipe-costing SaaS) is
   priced for scale; owners of micro-bakeries want an owned spreadsheet. Etsy/Gumroad
   already sell "bakery costing / pricing" sheets — demand is proven, quality is uneven.

### 7 — Butchery / meat
1. **Departments:** Production (cutting/boning/mince/sausage), Quality & Compliance
   (**853/2004 approval**, HACCP, health mark), Procurement (carcass/primal in),
   Finance (cutting yield & costing), Sales (counter + wholesale), Maintenance.
2. **Workflows:** **approved-establishment file + health/identification mark control**
   (legal=3); cold-chain temperature at every step; carcass-to-cut traceability + recall;
   knife/blade & foreign-body control; cutting-yield/costing; allergens on seasoned/
   processed lines (sausage rusk = gluten).
3. **Assets:** Approved Establishment File & Health-Mark Control (legal=3), Batch/Yield
   Record, Recall/Mock-Recall, Foreign-Body Control, Recipe/BOM costing, plus reused
   HACCP/Temp/Cleaning/Traceability/H&S/Fire.
4. **Pain points:** losing the approval/health-mark audit = business stops; cutting-yield
   leakage is invisible without records; cold-chain breaches and recall readiness;
   traceability across split carcasses.
5. **Tools & gaps:** meat-specific ERP exists but is heavyweight/costly; small butchers
   run paper diaries → digitising the approval file + yield sheet is an unmet, defensible niche.

### 8 — Dairy
1. **Departments:** Production (pasteurisation/cheese/yoghurt), Quality & Compliance
   (**853/2004 approval**, raw-milk hygiene, pasteurisation CCP), Procurement (milk intake),
   Finance, Sales (wholesale-heavy), Maintenance (plant/calibration).
2. **Workflows:** approved-establishment file + health mark (legal=3); **pasteurisation /
   heat-treatment CCP records**; raw-milk intake & cold chain; calibration of probes/
   thermometers; batch traceability + recall; label + nutrition; net-quantity control.
3. **Assets:** Approved Establishment File (legal=3), Calibration Log, Batch/Yield Record,
   Recall/Mock-Recall, Label & Nutrition Generator, Net-Quantity Sheet, plus reused
   HACCP/Temp/Cleaning/Traceability/H&S/Fire.
4. **Pain points:** pasteurisation/heat-treatment evidence is make-or-break at audit;
   calibration drift invalidates CCP data; thin margins + milk-price volatility; recall
   exposure on a perishable, animal-origin product.
5. **Tools & gaps:** dairy MES/LIMS are enterprise-priced; artisan dairies (the growth
   segment) need affordable CCP + calibration + traceability sheets.

### 9 — Beverage
1. **Departments:** Production (brew/blend/bottle/can), Quality & Compliance (HACCP,
   labelling, **fill-volume control**), Procurement, Finance (incl. **excise/duty** if
   alcoholic), Sales (wholesale/distribution), Maintenance.
2. **Workflows:** batch/brew records & yield; **net-content / average-quantity fill control
   + e-mark** (legal — high relevance to liquids); label (allergens e.g. sulphites; nutrition
   for soft drinks, **alcohol exempt from nutrition**); shelf-life/date-coding; cold chain
   where needed; excise/duty tracking for alcohol.
3. **Assets:** Net-Quantity/e-mark Control (legal, high), Batch/Yield Record, Label &
   Nutrition Generator, Shelf-Life Record, Recipe/BOM costing, plus reused HACCP/Cleaning/
   Traceability/H&S/Fire; excise tracking folded into Cashflow/P&L for now.
4. **Pain points:** under/over-fill = legal exposure or margin loss; excise/duty admin for
   small breweries/distilleries; label compliance differs alcoholic vs soft; batch
   consistency.
5. **Tools & gaps:** brewery management SaaS exists but craft producers complain about cost
   and over-complexity; a fill-control + batch + costing sheet bundle is an unmet niche.

### 10 — Ready meals / catering production
1. **Departments:** Production (cook/chill/assembly), Quality & Compliance (HACCP-heavy,
   cook & chill CCPs, allergens, labelling), Procurement, Finance (recipe costing at scale),
   Sales (B2B contracts), Maintenance.
2. **Workflows:** cook/chill/reheat **CCP temperature records**; full allergen matrix across
   many SKUs; label + nutrition per product (legal); date-coding & shelf-life validation;
   batch traceability + recall; supplier approval; production planning vs orders.
3. **Assets:** Label & Nutrition Generator (legal), Batch/Yield Record, Shelf-Life &
   Date-Coding, Supplier Approval Register, Production Planning Sheet, Recall/Mock-Recall,
   plus reused HACCP/Allergen/Temp/Cleaning/Traceability/H&S/Fire.
4. **Pain points:** allergen + label compliance across a large, changing SKU range is the
   biggest liability; cook/chill CCP evidence; costing accuracy on fixed-price B2B contracts;
   planning production to order without over/under-production.
5. **Tools & gaps:** food-production ERP is enterprise-grade; small/contract caterers need
   an affordable CCP + allergen/label + costing toolkit they own.

---

## [C] CROSS-TYPE INSIGHTS (feeds Phase 6/7)
- **New universal-core candidates within food manufacturing** (MUST across ≥3 of the 5):
  Batch/Yield Record, Label & Nutrition Generator, Net-Quantity/e-mark Control,
  Recall/Mock-Recall, plus the reused HACCP/Temp/Cleaning/Traceability/H&S/Fire that already
  span hospitality too — these are the highest-leverage build-once/sell-many products.
- **853/2004 Approved Establishment File** is a high-value *niche* MUST for meat & dairy only
  (Legal=3): low competition, high pain, strong willingness-to-pay.
- **Label & Nutrition Generator** is the most cross-cutting *new* product and pairs naturally
  with the hospitality Allergen tool → a "Food Labelling & Allergen Suite" bundle.
- Excise/duty (alcoholic beverage) flagged for a dedicated Phase 8/10 follow-up; folded into
  Cashflow/P&L for Phase 2 to avoid premature scope creep.

## [D] EU/Ireland notes
- Units metric (kg, g, ml, L, °C, minutes). Dates DD/MM/YYYY. Comma thousands (1,067,558).
- EU VAT on digital goods remains in scope for the seller (Ireland) — locked in Phase 8.
</content>
