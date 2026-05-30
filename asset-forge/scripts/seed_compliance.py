#!/usr/bin/env python3
"""
ASSET-FORGE · Phase 10 (BONUS) — Standards & audit research → DB
Seeds the compliance/audit extension of intelligence.db (brief §15.4).

Adds:
  - table `standards`         (id, name, family, scope, certifying_bodies, current_version, source_url)
  - table `compliance_assets` (id, name, asset_type, buyer_role, standard_ids, business_type_ids, tier, notes)
  - extends `products` with columns `audience` and `standard_ids`
  - view  `v_audit_packs`     (compliance_assets grouped by standard → instant bundle definitions)

All standard versions VERIFIED LIVE 30/05/2026 via Tavily (brief: never from memory).
Idempotent / re-runnable:  python3 scripts/seed_compliance.py
"""
import os, sqlite3

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "intelligence.db"))

# business-type id groups (from DB)
HOSP   = "1,2,3,4,5"
FOODMFG = "6,7,8,9,10"
NONFOOD = "11,12,13,14,15"
TRADES  = "16,17,18,19,20,21"
FOOD    = "1,2,3,4,5,6,7,8,9,10"          # hospitality + food manufacturing
ALL     = ",".join(str(i) for i in range(1, 22))

# ---- standards (live-verified versions, 30/05/2026) -------------------------
STANDARDS = [
    # id, name, family, scope, certifying_bodies, current_version, source_url
    (1, "ISO 9001", "Management systems (ISO)", "Quality management — all sectors (customer-required, not law)",
     "Certification bodies (e.g. NSAI, SGS, BSI, Bureau Veritas, TÜV SÜD/Rheinland/NORD) audit you against it",
     "ISO 9001:2015 + Amd 1:2024 (climate action); ISO 9001:2026 revision at FDIS stage",
     "https://www.iso.org/standard/88431.html"),
    (2, "ISO 14001", "Management systems (ISO)", "Environmental management",
     "Accredited certification bodies", "ISO 14001:2015 + Amd 1:2024 (climate action)",
     "https://www.iso.org/standard/60857.html"),
    (3, "ISO 45001", "Management systems (ISO)", "Occupational health & safety management",
     "Accredited certification bodies", "ISO 45001:2018 + Amd 1:2024 (climate action)",
     "https://www.iso.org/standard/63787.html"),
    (4, "ISO 22000", "Management systems (ISO)", "Food safety management (FSMS)",
     "Accredited certification bodies", "ISO 22000:2018 + Amd 1:2024 (climate action)",
     "https://www.iso.org/standard/65464.html"),
    (5, "ISO 27001", "Management systems (ISO)", "Information security (niche)",
     "Accredited certification bodies", "ISO/IEC 27001:2022",
     "https://www.iso.org/standard/27001"),
    (6, "ISO 50001", "Management systems (ISO)", "Energy management (niche)",
     "Accredited certification bodies", "ISO 50001:2018",
     "https://www.iso.org/standard/69426.html"),
    (7, "HACCP (Codex)", "Food sector", "Hazard analysis — legal floor for all food businesses",
     "Self-implemented; verified by EHO/auditors", "Codex Alimentarius CXC 1-1969, Rev. 2022 (Gen. Principles of Food Hygiene incl. HACCP annex)",
     "https://www.fao.org/fao-who-codexalimentarius"),
    (8, "BRCGS Food Safety", "Food sector (GFSI)", "Food manufacturing/packing — customer-required (retail)",
     "GFSI-recognised certification bodies", "Issue 9 (Aug 2022; effective Feb 2023). Issue 10 in development — TWG started Apr 2026",
     "https://www.brcgs.com/about-brcgs/news/2026/food-10-twg"),
    (9, "IFS Food", "Food sector (GFSI)", "Food manufacturing — customer-required (esp. EU retail)",
     "GFSI-recognised certification bodies", "Version 8 (Doctrine v5, Apr 2026)",
     "https://www.ifs-certification.com/"),
    (10, "FSSC 22000", "Food sector (GFSI)", "Food safety system certification — customer-required",
     "GFSI-recognised certification bodies", "Version 7 (published May 2026; v6 valid to 30 Apr 2027, upgrade to v7 by Apr 2028)",
     "https://blog.qima.com/fssc22000/fssc-22000-v7-key-changes-v6-prepare"),
    (11, "SALSA", "Food sector", "Safe & Local Supplier Approval — small/micro food producers",
     "SALSA-approved auditors", "SALSA (current issue; entry-level GFSI alternative)",
     "https://www.salsafood.co.uk/"),
    (12, "GMP / GHP", "Food sector", "Good Manufacturing / Good Hygiene Practice — PRP foundation",
     "Self-implemented; audited", "Per Codex GHP + sector codes",
     "https://www.fao.org/fao-who-codexalimentarius"),
    (13, "Reg. (EC) 852/2004", "EU legal floor", "Food hygiene — legally mandatory (EU)",
     "Enforced by competent authority (EHO/FSAI in IE)", "Reg. (EC) No 852/2004 (consolidated, as amended)",
     "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0852"),
    (14, "Reg. (EU) 1169/2011 (FIC)", "EU legal floor", "Food information / 14 allergens — legally mandatory",
     "Enforced by competent authority (FSAI in IE)", "Reg. (EU) No 1169/2011 (consolidated, as amended)",
     "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011R1169"),
    (15, "Fáilte Ireland accommodation standards", "Hospitality", "Accommodation quality/registration (IE)",
     "Fáilte Ireland", "Current registration & grading scheme",
     "https://www.failteireland.ie/"),
    (16, "Safe-T-Cert", "Trades / construction", "Construction H&S management (IE/NI)",
     "Safe-T-Cert assessors (CIF/CECA)", "Current scheme",
     "https://www.cif.ie/safe-t-cert/"),
    (17, "CIRI", "Trades / construction", "Construction Industry Register Ireland (statutory register)",
     "CIRI / NSAI", "Statutory register (S.I. construction regs)",
     "https://www.ciri.ie/"),
    (18, "Safe Electric", "Trades / construction", "Electrical works registration — legally required (IE)",
     "Safe Electric (Commission for Regulation of Utilities)", "Current scheme",
     "https://www.safeelectric.ie/"),
    (19, "RGI", "Trades / construction", "Register of Gas Installers of Ireland — legally required (IE)",
     "RGII", "Current scheme",
     "https://www.rgii.ie/"),
    (20, "CHAS / SafeContractor / Constructionline", "Trades / construction", "UK contractor prequalification (SSIP)",
     "SSIP-member assessment bodies", "Current SSIP schemes",
     "https://ssip.org.uk/"),
    (21, "NICEIC / Gas Safe", "Trades / construction", "UK electrical / gas registration — legally required (UK)",
     "NICEIC; Gas Safe Register", "Current schemes",
     "https://www.gassaferegister.co.uk/"),
]

# ---- compliance assets (brief §15.2 auditor/consultant + §15.3 auditee) -----
# id, name, asset_type, buyer_role, standard_ids, business_type_ids, tier, notes
COMPLIANCE_ASSETS = [
    # --- AUDITEE / OPERATOR (buyer = operator) ---
    (1, "Clause-by-clause Gap-Analysis Tool", "Spreadsheet tracker", "operator",
     "1,2,3,4,7,8,9,10", ALL, "MUST",
     "FLAGSHIP (Phase 12). Current-state vs each clause; RAG status + action list. Cheapest to build, clearest pain-killer."),
    (2, "Mock-Audit / Readiness Self-Assessment", "Form/checklist", "operator",
     "1,4,7,8,9,10", FOOD, "MUST",
     "FLAGSHIP. Answers 'will I pass?' — highest willingness-to-pay. Free 'lite' version = lead magnet."),
    (3, "Document-Control Register / Master Document List", "Spreadsheet tracker", "operator",
     "1,2,3,4,9,10", ALL, "SHOULD",
     "Controlled-document list, version, owner, review date — clause 7.5 backbone."),
    (4, "Internal-Audit Programme & Log", "Log book", "operator",
     "1,2,3,4,8,9,10", ALL, "MUST",
     "Annual internal-audit schedule + findings log — mandated by every ISO/GFSI scheme."),
    (5, "Management-Review Template + Minutes Log", "SOP template", "operator",
     "1,2,3,4,9,10", ALL, "SHOULD",
     "Agenda + inputs/outputs + minutes — clause 9.3."),
    (6, "Corrective-Action (CAPA) Log", "Log book", "operator",
     "1,2,3,4,7,8,9,10", ALL, "MUST",
     "Root-cause + correction + verification close-out — clause 10."),
    (7, "Training Matrix / Competency Records", "Spreadsheet tracker", "operator",
     "1,3,4,7,8,9,10", ALL, "MUST",
     "Reuses catalogue asset id 10 (Staff Training & Induction Matrix). Competence evidence — clause 7.2."),
    (8, "Supplier-Approval Register", "Spreadsheet tracker", "operator",
     "4,7,8,9,10", FOOD, "MUST",
     "Approved-supplier list + spec + monitoring. Links catalogue assets 5/28."),
    (9, "Calibration Log", "Log book", "operator",
     "4,7,8,9,10", FOOD, "MUST",
     "Measuring-equipment calibration schedule + records. Links catalogue asset 30."),
    (10, "Traceability Log (food)", "Log book", "operator",
     "4,7,8,9,10,13", FOOD, "MUST",
     "One-step-back/forward batch trace + mock-recall. Links catalogue asset 5."),
    (11, "HACCP Plan + CCP Monitoring + PRP Checklists", "Log book", "operator",
     "4,7,8,9,10,13", FOOD, "MUST",
     "Full HACCP study + CCP logs + prerequisite checklists. Links catalogue asset 1 (P1 flagship)."),
    # --- AUDITOR / CONSULTANT (buyer = auditor/consultant) ---
    (12, "Audit Checklist / Protocol (per standard)", "Form/checklist", "auditor",
     "1,2,3,4,8,9,10", ALL, "SHOULD",
     "Clause-mapped audit question set per standard — the auditor's working tool."),
    (13, "Audit Scoring & Grading Sheet", "Calculator", "auditor",
     "8,9,10", FOODMFG, "SHOULD",
     "Auto-grades against scheme scoring (e.g. BRCGS AA–D, IFS Foundation/Higher)."),
    (14, "Non-Conformance (NC) Register", "Log book", "auditor",
     "1,2,3,4,8,9,10", ALL, "SHOULD",
     "Logs majors/minors + clause ref + due date. Used by both auditor and auditee."),
    (15, "Audit-Schedule Planner (surveillance + recertification)", "Diary/planner", "consultant",
     "1,2,3,4,8,9,10", ALL, "SHOULD",
     "3-year certification cycle: initial → surveillance → recert. Avoids lapse."),
    (16, "Objective-Evidence Register", "Spreadsheet tracker", "auditor",
     "1,4,8,9,10", ALL, "COULD",
     "Maps each clause to the evidence sampled — defensible audit trail."),
    (17, "Audit-Report Generator", "SOP template", "auditor",
     "1,2,3,4,8,9,10", ALL, "SHOULD",
     "Structured findings → formatted report. Saves auditor write-up time."),
    (18, "Auditor Competency Log", "Log book", "auditor",
     "1,2,3,4", ALL, "COULD",
     "Auditor qualifications, CPD, witnessed-audit record — accreditation requirement."),
    (19, "Findings Dashboard", "Dashboard", "consultant",
     "1,4,8,9,10", ALL, "SHOULD",
     "Cross-site/standard open-NC and CAPA-ageing view for a consultant's client book."),
]

# products that map to a standard (audience + standard_ids), brief §15.4
PRODUCT_STANDARD_MAP = {
    1:  ("operator", "7,13,14"),         # P1 Café/Restaurant Compliance Pack
    8:  ("operator", "7,13,4,8,10"),     # P8 Food-Mfg Compliance Core
    10: ("operator", "14"),              # P10 Label & Nutrition (FIC)
    11: ("operator", "1"),               # P11 Manufacturing ISO 9001 / Quality Pack
    7:  ("operator", "18,19"),           # P7 Electrician/Gas Cert Pack (Safe Electric/RGI)
}


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("DROP VIEW IF EXISTS v_audit_packs")
    cur.execute("DROP TABLE IF EXISTS compliance_assets")
    cur.execute("DROP TABLE IF EXISTS standards")

    cur.execute("""
        CREATE TABLE standards (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            family TEXT,
            scope TEXT,
            certifying_bodies TEXT,
            current_version TEXT,
            source_url TEXT
        )""")
    cur.executemany("INSERT INTO standards VALUES (?,?,?,?,?,?,?)", STANDARDS)

    cur.execute("""
        CREATE TABLE compliance_assets (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            asset_type TEXT,
            buyer_role TEXT CHECK(buyer_role IN ('auditor','operator','consultant')),
            standard_ids TEXT,
            business_type_ids TEXT,
            tier TEXT,
            notes TEXT
        )""")
    cur.executemany("INSERT INTO compliance_assets VALUES (?,?,?,?,?,?,?,?)", COMPLIANCE_ASSETS)

    # extend products (guarded — columns may already exist)
    cols = [d[1] for d in cur.execute("PRAGMA table_info(products)")]
    if "audience" not in cols:
        cur.execute("ALTER TABLE products ADD COLUMN audience TEXT")
    if "standard_ids" not in cols:
        cur.execute("ALTER TABLE products ADD COLUMN standard_ids TEXT")
    # default existing 12 products to operator-facing, then map standard-linked ones
    cur.execute("UPDATE products SET audience='operator' WHERE audience IS NULL")
    for pid, (aud, stds) in PRODUCT_STANDARD_MAP.items():
        cur.execute("UPDATE products SET audience=?, standard_ids=? WHERE id=?", (aud, stds, pid))

    # view: compliance_assets grouped by standard → instant bundle definitions
    cur.execute("""
        CREATE VIEW v_audit_packs AS
        SELECT s.id   AS standard_id,
               s.name AS standard,
               s.family,
               s.current_version,
               ca.id  AS asset_id,
               ca.name AS asset,
               ca.buyer_role,
               ca.tier
        FROM standards s
        JOIN compliance_assets ca
          ON (',' || ca.standard_ids || ',') LIKE ('%,' || s.id || ',%')
        ORDER BY s.id, ca.buyer_role, ca.id
    """)

    con.commit()

    # ---- self-verify ----
    ns = cur.execute("SELECT COUNT(*) FROM standards").fetchone()[0]
    nca = cur.execute("SELECT COUNT(*) FROM compliance_assets").fetchone()[0]
    n_op = cur.execute("SELECT COUNT(*) FROM compliance_assets WHERE buyer_role='operator'").fetchone()[0]
    n_aud = cur.execute("SELECT COUNT(*) FROM compliance_assets WHERE buyer_role IN ('auditor','consultant')").fetchone()[0]
    npacks = cur.execute("SELECT COUNT(*) FROM v_audit_packs").fetchone()[0]
    nprod = cur.execute("SELECT COUNT(*) FROM products WHERE standard_ids IS NOT NULL").fetchone()[0]
    print(f"✓ standards: {ns} rows")
    print(f"✓ compliance_assets: {nca} rows ({n_op} operator / {n_aud} auditor+consultant)")
    print(f"✓ products extended: {nprod} mapped to standards (audience set on all 12)")
    print(f"✓ v_audit_packs: {npacks} standard×asset rows")
    print("  Sample — ISO 22000 pack:")
    for r in cur.execute("SELECT asset, buyer_role, tier FROM v_audit_packs WHERE standard='ISO 22000' LIMIT 6"):
        print("   ·", r[0], f"[{r[1]}/{r[2]}]")
    con.close()


if __name__ == "__main__":
    main()
