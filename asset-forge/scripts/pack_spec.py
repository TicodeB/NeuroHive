#!/usr/bin/env python3
"""
ASSET-FORGE · Phase 13c — Pack skeleton + industry-terminology mechanism
========================================================================
Factors the P2 SK premium pilot into a REUSABLE definition so a new vertical =
"swap the terminology + the palette," not a rebuild. The fixed skeleton
(Method · Planner · Dashboard · operational modules · Settings) and all formulas
live in the builder + `design_system.py`; everything that differs per trade is
captured here as a `PackSpec`.

"Terminology" = the *correct professional vocabulary of the trade* (labels, line
items, categories, metrics a butcher/baker/dealer actually uses) — NOT slang.
Structure stays constant; only the words change. (Samuel, 31/05/2026.)

A `PackSpec` carries:
  · vertical name + language (one language per pack — Premium-Pack carve-out)
  · palette overrides (3-colour Theme: primary / accent / ink)
  · an ordered list of `Module`s, each = a known module_type + its trade terms

13d will wire a generic builder to consume a `PackSpec` (today's pilot becomes
`hospitality_sk` fed through it). This file is the spec + validator + registry,
runnable as a dry-run that prints each pack's sheet plan and a terminology diff.

Run:  python3 scripts/pack_spec.py
"""
from __future__ import annotations
from dataclasses import dataclass, field

# --- module catalogue: the reusable operational templates -------------------
# module_type -> required term keys (validator checks these exist & non-empty)
FIXED = {"METHOD", "PLANNER", "DASHBOARD"}                  # every pack has these
MODULE_SLOTS = {
    "METHOD":     ["title", "subtitle", "steps"],
    "PLANNER":    ["title", "subtitle", "checklist"],
    "DASHBOARD":  ["title", "subtitle", "kpis", "insights"],
    "LEDGER_12M": ["title", "subtitle", "revenue_lines", "cos_lines", "overhead_lines"],
    "MARGIN":     ["title", "subtitle", "unit_label", "seed_items"],
    "STOCK":      ["title", "subtitle", "item_label", "loss_label", "seed_items"],
    "LABOUR":     ["title", "subtitle", "role_label", "target_pct"],
    "TAKINGS":    ["title", "subtitle", "source_label"],
    "TRAINING":   ["title", "subtitle", "topics"],
}
# metrics each operational module exposes, that DASHBOARD kpis/insights may cite
MODULE_METRICS = {
    # Phase 13i: + Budget-vs-Actual variance metrics (Datarails FP&A spine)
    "LEDGER_12M": ["revenue_total", "gross", "net", "cash_close",
                   "rev_plan", "rev_var", "rev_var_pct", "net_var"],
    "MARGIN":     ["avg", "below_target"],
    "STOCK":      ["loss_value"],
    "LABOUR":     ["pct", "cost"],
    "TAKINGS":    ["variance_total"],
}


@dataclass
class Module:
    type: str
    terms: dict = field(default_factory=dict)


@dataclass
class PackSpec:
    key: str
    vertical: str
    language: str                 # ISO: sk / cs / de / hu / pl / en (one per pack)
    palette: dict                 # {"primary": "..", "accent": "..", "ink": ".."}
    modules: list                 # ordered list[Module]

    def sheet_plan(self):
        order = {"METHOD": "00", "PLANNER": "01", "DASHBOARD": "02"}
        ops, n = [], 3
        plan = []
        for m in self.modules:
            if m.type in order:
                plan.append((order[m.type], m.type, m.terms.get("title", m.type)))
        for m in self.modules:
            if m.type not in FIXED:
                plan.append((f"{n:02d}", m.type, m.terms.get("title", m.type)))
                n += 1
        return plan


def validate(spec: PackSpec) -> list[str]:
    errs = []
    types = [m.type for m in spec.modules]
    for f in FIXED:
        if f not in types:
            errs.append(f"{spec.key}: missing required fixed module {f}")
    if not any(t not in FIXED for t in types):
        errs.append(f"{spec.key}: no operational modules (only the fixed spine)")
    if len(spec.language) != 2:
        errs.append(f"{spec.key}: language must be a 2-letter ISO code, got {spec.language!r}")
    for need in ("primary", "accent", "ink"):
        if need not in spec.palette:
            errs.append(f"{spec.key}: palette missing {need}")
    for m in spec.modules:
        if m.type not in MODULE_SLOTS:
            errs.append(f"{spec.key}: unknown module_type {m.type!r}")
            continue
        for key in MODULE_SLOTS[m.type]:
            if not m.terms.get(key):
                errs.append(f"{spec.key}/{m.type}: missing/empty term '{key}'")
    # dashboard kpis must cite real module.metric pairs
    dash = next((m for m in spec.modules if m.type == "DASHBOARD"), None)
    if dash:
        present = {m.type for m in spec.modules}
        for label, src in dash.terms.get("kpis", []):
            mod, _, metric = src.partition(".")
            if mod not in present:
                errs.append(f"{spec.key}/DASHBOARD: kpi '{label}' cites absent module {mod}")
            elif metric not in MODULE_METRICS.get(mod, []):
                errs.append(f"{spec.key}/DASHBOARD: kpi '{label}' cites unknown metric {mod}.{metric}")
    return errs


# ============================================================================
# EXAMPLE 1 — hospitality_sk  (mirrors the built P2 pilot; the reference impl)
# ============================================================================
HOSPITALITY_SK = PackSpec(
    key="hospitality_sk", vertical="Gastro / pohostinstvo", language="sk",
    palette={"primary": "2D6CDF", "accent": "15A38C", "ink": "1A2B45"},
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ukáže maržu, mzdy a hotovosť skôr, než zabolia",
            "steps": ["RÁNO: 3 priority + otvorenie", "POČAS DŇA: tržby + straty",
                      "VEČER: uzávierka pokladne", "TÝŽDENNE: zmeny + marža",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: teploty chladničiek", "Otvorenie: hotovosť spočítaná",
                          "Zatvorenie: tržby zapísané", "Zatvorenie: straty zapísané",
                          "Zatvorenie: prevádzka zabezpečená"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …", "Hodnota strát …",
                         "Položky pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow, plán a odchýlka",
            "plan_label": "Plán (rok)",
            "revenue_lines": ["Tržby z jedál", "Tržby z nápojov", "Ostatné príjmy"],
            "cos_lines": ["Náklady na jedlo", "Náklady na nápoje"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie", "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža", "subtitle": "Náklady na porciu a hrubá marža",
            "unit_label": "Jedlo / nápoj",
            "seed_items": ["Kôš s domácim chlebom", "Rybacia polievka", "Hovädzí burger", "Cappuccino", "Čapované pivo"]}),
        Module("STOCK", {"title": "Zásoby", "subtitle": "Spotreba a hodnota strát",
            "item_label": "Položka", "loss_label": "Straty",
            "seed_items": ["Čapované pivo", "Domáce červené víno", "Čerstvé ryby", "Rib-eye steak", "Mlieko"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia", "target_pct": 0.35}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena potravín",
                       "Alergény", "Požiarna ochrana", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# EXAMPLE 2 — butcher_sk  (same skeleton, BUTCHER terminology — the proof)
# ============================================================================
BUTCHER_SK = PackSpec(
    key="butcher_sk", vertical="Mäsiarstvo", language="sk",
    palette={"primary": "7A2E2E", "accent": "A23E3E", "ink": "2B1A1A"},   # meat-red theme
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži výťažnosť, orez a maržu dielov",
            "steps": ["RÁNO: 3 priority + kontrola chladenia", "PRÍJEM: navážka jatočných tiel",
                      "POČAS DŇA: búranie, orez a straty", "VEČER: uzávierka pultu + veľkoodber",
                      "MESAČNE: cash flow + prehľad výťažnosti"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a rozvrh búrania a expedície",
            "checklist": ["Otvorenie: teploty chladiarní a mraziarní", "Otvorenie: čistota píly a nožov",
                          "Zatvorenie: navážka a straty zapísané", "Zatvorenie: faktúry veľkoodber",
                          "Zatvorenie: chladiaci reťazec zabezpečený"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — výťažnosť, orez a marža dielov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža dielov", "MARGIN.avg"),
                     ("Hodnota orezu a strát", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Výťažnosť pri vykostení …", "Hodnota orezu a strát …",
                         "Diely pod cieľovou maržou …", "Podiel miezd …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby pult (maloobchod)", "Tržby veľkoodber", "Tržby výroba (údeniny)"],
            "cos_lines": ["Nákup jatočných tiel", "Koreniny, obaly a črevá"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a chladenie", "Doprava", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža dielov", "subtitle": "Náklad na kg, výťažnosť a marža dielu/výrobku",
            "unit_label": "Diel / výrobok",
            "seed_items": ["Bravčové karé", "Hovädzia sviečková", "Mleté mäso", "Klobása domáca", "Slanina údená"]}),
        Module("STOCK", {"title": "Navážka a orez", "subtitle": "Jatočné telá → diely; hodnota orezu a strát",
            "item_label": "Diel / surovina", "loss_label": "Orez a strata",
            "seed_items": ["Jatočné telo bravčové (polovica)", "Hovädzia štvrť", "Kuracie prsia", "Bôčik", "Plece"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (mäsiar / predavač)", "target_pct": 0.25}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby pultu a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · faktúry veľkoodber"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena potravín (HACCP)",
                       "Krížová kontaminácia", "Chladiaci reťazec", "Ostré nástroje / píla", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# EXAMPLE 3 — baker_sk  (first net-new PRODUCTION vertical, Samuel's choice 31/05)
# ============================================================================
BAKER_SK = PackSpec(
    key="baker_sk", vertical="Pekáreň / cukráreň", language="sk",
    palette={"primary": "9C5B2E", "accent": "E0A458", "ink": "3A2A1A"},   # warm crust/gold
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži navažovanie, odpis a maržu výrobkov",
            "steps": ["RÁNO: nábeh pecí + 3 priority", "VÝROBA: navažovanie podľa receptúr (baker's %)",
                      "POČAS DŇA: predaj + odpis nepredaného", "VEČER: uzávierka + objednávka surovín",
                      "MESAČNE: cash flow + prehľad marže"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a rozvrh výroby a predaja",
            "checklist": ["Otvorenie: teploty pecí, chladení a mrazení", "Otvorenie: cesto a kysnutie pripravené",
                          "Zatvorenie: nepredané odpísané a zapísané", "Zatvorenie: objednávka múky a surovín",
                          "Zatvorenie: pece vypnuté, čistota a hygiena"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — marža výrobkov, odpis a mzdy",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža výrobkov", "MARGIN.avg"),
                     ("Hodnota odpisu", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (nepredané) …", "Výrobky pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby predajňa (maloobchod)", "Tržby veľkoodber (kaviarne/obchody)", "Tržby objednávky (torty/akcie)"],
            "cos_lines": ["Nákup surovín (múka, tuky, cukor)", "Obaly a dekorácie"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie (pece)", "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža výrobkov", "subtitle": "Náklad na kus, baker's % a marža výrobku",
            "unit_label": "Výrobok",
            "seed_items": ["Rožok", "Chlieb kváskový", "Croissant", "Torta Sacher (rez)", "Buchta tvarohová"]}),
        Module("STOCK", {"title": "Suroviny a odpis", "subtitle": "Spotreba surovín a hodnota odpisu nepredaného",
            "item_label": "Surovina / výrobok", "loss_label": "Odpis a strata",
            "seed_items": ["Múka hladká", "Maslo", "Kvások", "Rožky (nepredané)", "Chlieb (nepredaný)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (pekár / predavač)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby predajne a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · objednávky"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena potravín (HACCP)",
                       "Alergény (lepok, orechy…)", "Práca s pecou / horúce povrchy", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# EXAMPLE 4 — bar_sk  (Phase 13f · Bar / pub · NACE 56.30 · beverage-led hospitality)
# ============================================================================
BAR_SK = PackSpec(
    key="bar_sk", vertical="Bar / pub", language="sk",
    palette={"primary": "1F5C4D", "accent": "C9982C", "ink": "16261F"},   # bottle-green + brass
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži výčap, straty a maržu nápojov",
            "steps": ["RÁNO: 3 priority + výmena sudov a CO₂",
                      "POČAS DŇA: tržby + rozliate a straty",
                      "VEČER: uzávierka pokladne + inventúra fliaš",
                      "TÝŽDENNE: zmeny + marža nápojov (pour cost)",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh zmeny",
            "checklist": ["Otvorenie: teploty chladenia a výčapu",
                          "Otvorenie: hotovosť v pokladni spočítaná",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: rozliate a straty zapísané",
                          "Zatvorenie: sudy, CO₂ a prevádzka zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža nápojov", "MARGIN.avg"),
                     ("Hodnota strát (rozliate)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Podiel miezd …", "Hodnota strát (rozliate) …",
                         "Nápoje pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby čapované (pivo, cider)", "Tržby destiláty a koktaily",
                              "Tržby víno a nealko", "Tržby kuchyňa / snacky"],
            "cos_lines": ["Nákup piva a sudov", "Nákup destilátov, vína a nealka", "Náklady kuchyňa"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a chladenie",
                               "Licencie (hudba/TV/športy)", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža nápojov", "subtitle": "Náklad na nálev (pour cost) a marža nápoja",
            "unit_label": "Nápoj",
            "seed_items": ["Čapované pivo 0,5 l", "Pohár vína 0,2 l", "Panák destilátu 0,04 l",
                           "Miešaný nápoj (koktail)", "Nealko 0,3 l"]}),
        Module("STOCK", {"title": "Sklad a straty", "subtitle": "Spotreba nápojov a hodnota strát (rozliate)",
            "item_label": "Položka", "loss_label": "Straty",
            "seed_items": ["Sud piva 50 l", "Fľaškové pivo", "Vodka 0,7 l", "Víno (fľaša)", "Nealko (prepravka)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (barman / čašník)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · sprepitné"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Zodpovedný výčap alkoholu", "Hygiena potravín",
                       "Alergény", "Manipulácia s bremenami (sudy)", "Požiarna ochrana", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# EXAMPLE 5 — greengrocer_sk  (Phase 13f · Ovocie a zelenina · NACE 47.21 · fresh-produce retail)
# ============================================================================
GREENGROCER_SK = PackSpec(
    key="greengrocer_sk", vertical="Ovocie a zelenina", language="sk",
    palette={"primary": "3B7A2A", "accent": "E8732A", "ink": "23351C"},   # leaf-green + citrus
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži kazivosť, maržu na kg a obrátku tovaru",
            "steps": ["RÁNO: 3 priority + príjem dodávky a kontrola kvality",
                      "POČAS DŇA: dopĺňanie, váženie, zľavy na dozreté",
                      "VEČER: uzávierka + odpis pokazeného tovaru",
                      "TÝŽDENNE: marža na kg + obrátka a straty",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: kontrola kvality a sviežosti tovaru",
                          "Otvorenie: váhy a cenovky pripravené",
                          "Zatvorenie: tržby zapísané (uzávierka)",
                          "Zatvorenie: pokazený tovar odpísaný a zapísaný",
                          "Zatvorenie: chladenie a sklad zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na kg", "MARGIN.avg"),
                     ("Hodnota odpisu (kazivosť)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (kazivosť) …", "Tovar pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby ovocie", "Tržby zelenina", "Tržby ostatné (vajcia, byliny, sušené)"],
            "cos_lines": ["Nákup ovocia a zeleniny", "Obaly, prepravky a vrecká"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a chladenie",
                               "Doprava a rozvoz", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na kg", "subtitle": "Nákupná a predajná cena na kg a marža položky",
            "unit_label": "Tovar",
            "seed_items": ["Jablká (kg)", "Banány (kg)", "Zemiaky (kg)", "Paradajky (kg)", "Mrkva (kg)", "Šalát (ks)"]}),
        Module("STOCK", {"title": "Sklad a kazivosť", "subtitle": "Spotreba a hodnota odpisu pokazeného tovaru",
            "item_label": "Tovar", "loss_label": "Odpis",
            "seed_items": ["Jablká", "Banány", "Šalát", "Paradajky", "Mäkké ovocie (bobule)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (predavač / vodič)", "target_pct": 0.18}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena potravín",
                       "Skladovanie a chladiaci reťazec", "Váženie a cenotvorba", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# EXAMPLE 6 — patisserie_sk  (Phase 13f · Cukráreň · NACE 10.72 · fine pastry/confectionery)
# ============================================================================
PATISSERIE_SK = PackSpec(
    key="patisserie_sk", vertical="Cukráreň", language="sk",
    palette={"primary": "7A3B5E", "accent": "D9A441", "ink": "2A1726"},   # plum + gold
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži receptúry, objednávky, odpis a maržu zákuskov",
            "steps": ["RÁNO: nábeh + 3 priority + kontrola chladenia",
                      "VÝROBA: navažovanie podľa receptúr + objednávky tort",
                      "POČAS DŇA: predaj vo vitríne + odpis nepredaného",
                      "VEČER: uzávierka + objednávka surovín",
                      "MESAČNE: cash flow + prehľad marže"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a rozvrh výroby a objednávok",
            "checklist": ["Otvorenie: teploty chladiacich vitrín a mrazení",
                          "Otvorenie: objednávky tort na dnes pripravené",
                          "Zatvorenie: nepredané zákusky odpísané a zapísané",
                          "Zatvorenie: objednávka surovín (smotana, čokoláda)",
                          "Zatvorenie: chladiaci reťazec a hygiena zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — marža zákuskov, odpis a mzdy",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža zákuskov", "MARGIN.avg"),
                     ("Hodnota odpisu (nepredané)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (nepredané) …", "Zákusky pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby vitrína (zákusky, dezerty)", "Tržby objednávky (torty/akcie)",
                              "Tržby veľkoodber (kaviarne/hotely)"],
            "cos_lines": ["Nákup surovín (smotana, čokoláda, ovocie)", "Obaly a dekorácie"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a chladenie",
                               "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža zákuskov", "subtitle": "Náklad na kus podľa receptúry a marža výrobku",
            "unit_label": "Výrobok",
            "seed_items": ["Veterník", "Laskonka", "Torta Sacher (rez)", "Makrónka",
                           "Tiramisu (porcia)", "Torta na objednávku (kg)"]}),
        Module("STOCK", {"title": "Suroviny a odpis", "subtitle": "Spotreba surovín a hodnota odpisu nepredaného",
            "item_label": "Surovina / výrobok", "loss_label": "Odpis",
            "seed_items": ["Smotana na šľahanie", "Čokoláda (poleva)", "Maslo", "Zákusky (nepredané)", "Ovocie (dekor)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (cukrár / predavač)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby predajne a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · objednávky"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena potravín (HACCP)",
                       "Alergény (lepok, orechy, mlieko…)", "Chladiaci reťazec", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# EXAMPLE 7 — hospitality_en  (Phase 13h · localisation proof: the SK pilot
#             cloned into ENGLISH. Same skeleton, modules, palette + FP&A spine;
#             only the trade terminology is translated. UI chrome comes from
#             i18n.EN. English is authored natively here — SK/CS/DE/HU/PL still
#             need a native-editor pass before listing per the standing rule.)
# ============================================================================
HOSPITALITY_EN = PackSpec(
    key="hospitality_en", vertical="Hospitality / Food service", language="en",
    palette={"primary": "2D6CDF", "accent": "15A38C", "ink": "1A2B45"},
    modules=[
        Module("METHOD", {"title": "Method",
            "subtitle": "The pack that shows margin, wages and cash before they hurt",
            "steps": ["MORNING: 3 priorities + opening", "DURING THE DAY: takings + losses",
                      "EVENING: cash-up (till close)", "WEEKLY: rota + margin",
                      "MONTHLY: cash flow + overview"]}),
        Module("PLANNER", {"title": "Day plan",
            "subtitle": "Three priorities and a clear schedule for the day",
            "checklist": ["Opening: fridge temperatures", "Opening: float counted",
                          "Closing: takings recorded", "Closing: losses recorded",
                          "Closing: premises secured"]}),
        Module("DASHBOARD", {"title": "Overview",
            "subtitle": "Automatic dashboard — pulls live figures from the other sheets",
            "kpis": [("Annual revenue", "LEDGER_12M.revenue_total"),
                     ("Gross margin", "LEDGER_12M.gross"),
                     ("Net profit", "LEDGER_12M.net"),
                     ("Revenue vs plan", "LEDGER_12M.rev_var"),
                     ("Closing cash", "LEDGER_12M.cash_close"),
                     ("Average margin", "MARGIN.avg"),
                     ("Labour share", "LABOUR.pct")],
            "insights": ["Revenue vs plan …", "Net margin …", "Labour share …", "Loss value …",
                         "Items below target margin …", "Till difference …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-month cash flow, plan and variance",
            "plan_label": "Plan (year)",
            "revenue_lines": ["Food sales", "Drink sales", "Other income"],
            "cos_lines": ["Food cost", "Drink cost"],
            "overhead_lines": ["Wages and staff", "Rent and rates", "Utilities", "Marketing", "Other overheads"]}),
        Module("MARGIN", {"title": "Margin", "subtitle": "Cost per portion and gross margin",
            "unit_label": "Dish / drink",
            "seed_items": ["Basket of house bread", "Fish soup", "Beef burger", "Cappuccino", "Draught beer"]}),
        Module("STOCK", {"title": "Stock", "subtitle": "Usage and loss value",
            "item_label": "Item", "loss_label": "Losses",
            "seed_items": ["Draught beer", "House red wine", "Fresh fish", "Rib-eye steak", "Milk"]}),
        Module("LABOUR", {"title": "Rota", "subtitle": "Shifts and labour cost share",
            "role_label": "Role", "target_pct": 0.35}),
        Module("TAKINGS", {"title": "Takings", "subtitle": "Daily takings and cash-up",
            "source_label": "Z-reading · cash · cards"}),
        Module("TRAINING", {"title": "Training", "subtitle": "Training matrix — proof before a shift",
            "topics": ["Induction", "Manual handling", "Food hygiene",
                       "Allergens", "Fire safety", "H&S / first aid"]}),
    ],
)

# ============================================================================
# Phase 13f · BATCH 2 — personal services (NACE 96.02). These trades are
# LABOUR-led and carry almost no stock, so the spec deliberately OMITS the
# STOCK module → the generic builder yields a 6-KPI dashboard (no loss tile)
# and skips the stock insight. Margin is materials-cost-per-service.
# ============================================================================

# EXAMPLE 8 — hairdresser_sk  (Kaderníctvo · NACE 96.02 · service-led, no stock)
HAIRDRESSER_SK = PackSpec(
    key="hairdresser_sk", vertical="Kaderníctvo", language="sk",
    palette={"primary": "8E3B6B", "accent": "40B5A6", "ink": "2A1622"},   # rose-plum + teal
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži obsadenosť kresla, maržu služieb a mzdy",
            "steps": ["RÁNO: 3 priority + príprava kresiel a rezervácie",
                      "POČAS DŇA: služby + predaj vlasovej kozmetiky",
                      "VEČER: uzávierka pokladne + obsadenosť kresla",
                      "TÝŽDENNE: zmeny + marža služieb",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: čistota a dezinfekcia nástrojov",
                          "Otvorenie: rezervácie na dnes skontrolované",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: spotreba farieb a kozmetiky zapísaná",
                          "Zatvorenie: prevádzka a hygiena zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža služieb", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Služby pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby strihanie a úprava", "Tržby farbenie a melír",
                              "Tržby predaj vlasovej kozmetiky"],
            "cos_lines": ["Nákup farieb a vlasovej kozmetiky", "Spotrebný materiál (fólie, rukavice)"],
            "overhead_lines": ["Mzdy a provízie", "Nájom a poplatky", "Energie a voda",
                               "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža služieb", "subtitle": "Materiálový náklad na službu a marža",
            "unit_label": "Služba",
            "seed_items": ["Dámsky strih", "Pánsky strih", "Farbenie", "Melír / balayage",
                           "Spoločenský účes", "Predaj šampónu (ks)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov (vrátane provízií)",
            "role_label": "Pozícia (kaderník / asistent)", "target_pct": 0.45}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · prepitné"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Hygiena a dezinfekcia nástrojov",
                       "Práca s chemikáliami (farby, peroxid)", "Test citlivosti / alergie",
                       "Manipulácia s bremenami", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 9 — beauty_salon_sk  (Kozmetický salón · NACE 96.02 · treatment-led, no stock)
BEAUTY_SALON_SK = PackSpec(
    key="beauty_salon_sk", vertical="Kozmetický salón", language="sk",
    palette={"primary": "7C5CBF", "accent": "C77FA8", "ink": "241B33"},   # lavender + rose
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži obsadenosť kabín, maržu ošetrení a mzdy",
            "steps": ["RÁNO: 3 priority + príprava kabín a rezervácie",
                      "POČAS DŇA: ošetrenia + predaj kozmetiky",
                      "VEČER: uzávierka pokladne + obsadenosť kabín",
                      "TÝŽDENNE: zmeny + marža ošetrení",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: čistota a sterilizácia nástrojov",
                          "Otvorenie: rezervácie a kabíny pripravené",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: spotreba prípravkov zapísaná",
                          "Zatvorenie: prevádzka a hygiena zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža ošetrení", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Ošetrenia pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby ošetrenia tváre a tela", "Tržby manikúra/pedikúra a nechty",
                              "Tržby predaj kozmetiky"],
            "cos_lines": ["Nákup kozmetiky a prípravkov", "Spotrebný materiál (jednorazový)"],
            "overhead_lines": ["Mzdy a provízie", "Nájom a poplatky", "Energie a voda",
                               "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža ošetrení", "subtitle": "Náklad prípravkov na ošetrenie a marža",
            "unit_label": "Ošetrenie",
            "seed_items": ["Kozmetické ošetrenie tváre", "Manikúra", "Gélové nechty",
                           "Depilácia voskom", "Masáž tváre", "Predaj krému (ks)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov (vrátane provízií)",
            "role_label": "Pozícia (kozmetička / nechtárka)", "target_pct": 0.45}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · poukazy"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Hygiena a sterilizácia nástrojov",
                       "Práca s prístrojmi a prípravkami", "Test citlivosti / alergie",
                       "Manipulácia s chemikáliami", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 10 — barber_sk  (Holičstvo / barbershop · NACE 96.02 · service-led, no stock)
BARBER_SK = PackSpec(
    key="barber_sk", vertical="Holičstvo / barbershop", language="sk",
    palette={"primary": "2B3A55", "accent": "B5894E", "ink": "161D2B"},   # navy + bronze (classic barber)
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži obsadenosť kresla, maržu služieb a mzdy",
            "steps": ["RÁNO: 3 priority + príprava kresiel a rezervácie",
                      "POČAS DŇA: strihy, úprava brady + predaj kozmetiky",
                      "VEČER: uzávierka pokladne + obsadenosť kresla",
                      "TÝŽDENNE: zmeny + marža služieb",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: čistota a dezinfekcia strojčekov a britiev",
                          "Otvorenie: rezervácie na dnes skontrolované",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: spotreba pánskej kozmetiky zapísaná",
                          "Zatvorenie: prevádzka a hygiena zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža služieb", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Služby pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby strih vlasov", "Tržby úprava brady (holenie)",
                              "Tržby predaj pánskej kozmetiky"],
            "cos_lines": ["Nákup pánskej kozmetiky (oleje, pomády)", "Spotrebný materiál (žiletky, uteráky)"],
            "overhead_lines": ["Mzdy a provízie", "Nájom a poplatky", "Energie a voda",
                               "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža služieb", "subtitle": "Materiálový náklad na službu a marža",
            "unit_label": "Služba",
            "seed_items": ["Pánsky strih", "Strih strojčekom (fade)", "Úprava brady",
                           "Klasické holenie britvou", "Strih + brada", "Predaj pomády (ks)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov (vrátane provízií)",
            "role_label": "Pozícia (barber / holič)", "target_pct": 0.40}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · prepitné"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Hygiena a dezinfekcia nástrojov",
                       "Práca s britvou a strojčekmi", "Krížová kontaminácia / kožné ochorenia",
                       "Manipulácia s bremenami", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# Phase 13f · BATCH 3 — accommodation + convenience retail. These KEEP the
# STOCK module → standard 7-KPI dashboards (loss tile present). Terminology
# spans short-stay hosting (occupancy + per-night yield) and grocery retail.
# ============================================================================

# EXAMPLE 11 — bnb_sk  (Penzión / B&B · NACE 55.20 · accommodation + breakfast)
BNB_SK = PackSpec(
    key="bnb_sk", vertical="Penzión / B&B", language="sk",
    palette={"primary": "2E7D8A", "accent": "D98C4A", "ink": "1B2E33"},   # teal + warm amber
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži obsadenosť, cenu izby a maržu raňajok",
            "steps": ["RÁNO: 3 priority + check-out a upratovanie izieb",
                      "POČAS DŇA: check-in, rezervácie, raňajky",
                      "VEČER: uzávierka + obsadenosť na zajtra",
                      "TÝŽDENNE: zmeny + marža (raňajky, doplnky)",
                      "MESAČNE: cash flow + prehľad obsadenosti"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: izby upratané a pripravené",
                          "Otvorenie: raňajky a zásoby skontrolované",
                          "Zatvorenie: tržby a platby zapísané (uzávierka)",
                          "Zatvorenie: rezervácie a check-in na zajtra",
                          "Zatvorenie: prevádzka a kľúče zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža doplnkov", "MARGIN.avg"),
                     ("Hodnota odpisu (raňajky)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (raňajky) …", "Položky pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby ubytovanie", "Tržby raňajky a strava",
                              "Tržby doplnkové služby (parkovanie, wellness)"],
            "cos_lines": ["Nákup potravín (raňajky)", "Pranie, čistenie a spotrebný materiál"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a voda",
                               "Online provízie (Booking/OTA)", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža doplnkov", "subtitle": "Náklad a marža raňajok a doplnkových služieb",
            "unit_label": "Položka / služba",
            "seed_items": ["Raňajky (osoba)", "Polpenzia (osoba)", "Fľaša vína",
                           "Parkovanie (noc)", "Neskorý check-out"]}),
        Module("STOCK", {"title": "Sklad a odpis", "subtitle": "Spotreba potravín a hodnota odpisu (raňajky)",
            "item_label": "Položka", "loss_label": "Odpis",
            "seed_items": ["Pečivo a chlieb", "Vajcia", "Mliečne výrobky", "Údeniny a syry", "Ovocie"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (recepcia / upratovanie)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · platby OTA"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Hygiena potravín (raňajky)", "Alergény",
                       "Požiarna ochrana a evakuácia", "GDPR / ochrana údajov hostí",
                       "Manipulácia s bremenami", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 12 — convenience_sk  (Potraviny / večierka · NACE 47.11 · grocery retail)
CONVENIENCE_SK = PackSpec(
    key="convenience_sk", vertical="Potraviny / večierka", language="sk",
    palette={"primary": "1F6FB2", "accent": "F2A93B", "ink": "15293A"},   # retail blue + amber
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu, kazivosť a obrátku tovaru",
            "steps": ["RÁNO: 3 priority + príjem dodávky a doplnenie",
                      "POČAS DŇA: predaj + kontrola dátumov spotreby",
                      "VEČER: uzávierka + odpis prošlého tovaru",
                      "TÝŽDENNE: marža kategórií + obrátka a straty",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: regály doplnené a cenovky správne",
                          "Otvorenie: chladenie a dátumy spotreby skontrolované",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: prošlý tovar odpísaný a zapísaný",
                          "Zatvorenie: pokladňa a prevádzka zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža kategórií", "MARGIN.avg"),
                     ("Hodnota odpisu (prošlé)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (prošlé) …", "Kategórie pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby potraviny a nápoje", "Tržby tabak a lotéria",
                              "Tržby ostatné (drogéria, tlač)"],
            "cos_lines": ["Nákup tovaru (potraviny, nápoje)", "Nákup tabak a ostatné"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a chladenie",
                               "Platobné terminály a poplatky", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža kategórií", "subtitle": "Nákupná a predajná cena a marža kategórie",
            "unit_label": "Tovar / kategória",
            "seed_items": ["Pečivo", "Mlieko a mliečne", "Nápoje nealko", "Cigarety (balík)",
                           "Pivo (plechovka)", "Drogéria"]}),
        Module("STOCK", {"title": "Sklad a odpis", "subtitle": "Zásoby a hodnota odpisu (prošlé/poškodené)",
            "item_label": "Tovar", "loss_label": "Odpis",
            "seed_items": ["Pečivo", "Mlieko", "Jogurty", "Údeniny", "Ovocie a zelenina"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (predavač)", "target_pct": 0.15}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · stravné lístky"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Hygiena potravín", "Predaj tabaku a alkoholu (vek)",
                       "Chladiaci reťazec a dátumy spotreby", "Manipulácia s bremenami",
                       "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 13 — airbnb_sk  (Krátkodobý prenájom · NACE 55.20 · short-stay hosting)
AIRBNB_SK = PackSpec(
    key="airbnb_sk", vertical="Krátkodobý prenájom (Airbnb)", language="sk",
    palette={"primary": "C84C66", "accent": "3FB8AE", "ink": "261319"},   # coral + teal
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži obsadenosť, výnos na noc a náklady na upratovanie",
            "steps": ["RÁNO: 3 priority + check-out a turnover",
                      "POČAS DŇA: upratovanie, check-in, komunikácia s hosťami",
                      "VEČER: rezervácie + ceny na ďalšie dni",
                      "TÝŽDENNE: obsadenosť + výnos na noc a náklady",
                      "MESAČNE: cash flow + prehľad výnosov"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Príchod: byt uprataný a vybavený (toaletné, uteráky)",
                          "Príchod: check-in a kľúče/zámok pripravené",
                          "Odchod: tržby a poplatky zapísané",
                          "Odchod: rezervácie a turnover na zajtra",
                          "Odchod: kontrola škôd a doplnenie zásob"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža doplnkov", "MARGIN.avg"),
                     ("Hodnota strát (spotreba)", "STOCK.loss_value"),
                     ("Podiel nákladov na upratovanie", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota strát (spotreba) …", "Položky pod cieľovou maržou …",
                         "Podiel nákladov na upratovanie …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby ubytovanie (nocľažné)", "Poplatok za upratovanie",
                              "Doplnkové služby (transfer, raňajky)"],
            "cos_lines": ["Upratovanie a pranie", "Spotrebný materiál (toaletné, uvítací balík)"],
            "overhead_lines": ["Provízie platforiem (Airbnb/Booking)", "Nájom / hypotéka a poplatky",
                               "Energie a internet", "Údržba a opravy", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža doplnkov", "subtitle": "Náklad a marža doplnkových služieb a noci",
            "unit_label": "Položka / služba",
            "seed_items": ["Noc (apartmán)", "Poplatok za upratovanie", "Skorý check-in",
                           "Neskorý check-out", "Uvítací balík"]}),
        Module("STOCK", {"title": "Spotreba a straty", "subtitle": "Spotrebný materiál a hodnota strát/poškodení",
            "item_label": "Položka", "loss_label": "Straty/odpis",
            "seed_items": ["Toaletný papier", "Hygienické potreby", "Pranie posteľnej bielizne",
                           "Káva/čaj (uvítací)", "Poškodenia (vybavenie)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Upratovanie a podiel nákladov na turnover",
            "role_label": "Pozícia (upratovanie / co-host)", "target_pct": 0.20}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Výplaty platforiem a uzávierka",
            "source_label": "Výplaty platforiem (Airbnb/Booking) · hotovosť · prevody"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie (co-host)", "Hygiena a upratovanie (turnover)",
                       "Bezpečnosť hostí a detektory dymu", "GDPR / ochrana údajov hostí",
                       "Miestna daň z ubytovania / regulácia", "Manipulácia s bremenami",
                       "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# Phase 13f · BATCH 4 — event catering · fresh-flower retail · professional
# services. Caterer + Florist KEEP the STOCK module (perishable inputs →
# 7-KPI dashboards, loss tile present); Bookkeeper is a pure service practice
# with no stock → STOCK omitted → 6-KPI dashboard (like batch 2).
# ============================================================================

# EXAMPLE 14 — caterer_sk  (Catering / hromadné stravovanie · NACE 56.21 · event catering)
CATERER_SK = PackSpec(
    key="caterer_sk", vertical="Catering / hromadné stravovanie", language="sk",
    palette={"primary": "6E2639", "accent": "C8A15A", "ink": "241019"},   # burgundy + warm sand
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži kalkuláciu na osobu, plytvanie a maržu podujatí",
            "steps": ["RÁNO: 3 priority + potvrdenie objednávok na podujatia",
                      "VÝROBA: príprava podľa menu a počtu osôb",
                      "POČAS PODUJATIA: výdaj + kontrola kvality a teplôt",
                      "PO PODUJATÍ: vyúčtovanie + odpis nespotrebovaných surovín",
                      "MESAČNE: cash flow + prehľad marže podujatí"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh prípravy a podujatí",
            "checklist": ["Otvorenie: teploty chladenia a prepravných boxov",
                          "Otvorenie: objednávky a počty osôb potvrdené",
                          "Zatvorenie: tržby podujatí zapísané",
                          "Zatvorenie: odpis a plytvanie zapísané",
                          "Zatvorenie: vozidlá a vybavenie vyčistené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na osobu", "MARGIN.avg"),
                     ("Hodnota odpisu (plytvanie)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (plytvanie) …", "Menu pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby firemné podujatia (catering)", "Tržby svadby a oslavy",
                              "Tržby rozvoz / denné menu (krabičky)"],
            "cos_lines": ["Nákup surovín (potraviny, nápoje)", "Obaly, jednorazový riad a prenájmy"],
            "overhead_lines": ["Mzdy a personál (vrátane brigádnikov)", "Nájom kuchyne a poplatky",
                               "Energie a chladenie", "Doprava a vozidlá", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na osobu", "subtitle": "Náklad na osobu (cover) a marža menu/položky",
            "unit_label": "Menu / položka (na osobu)",
            "seed_items": ["Trojchodové menu (osoba)", "Rautové kanapky (10 ks)", "Grilovaný špíz (porcia)",
                           "Polievka (porcia)", "Svadobné menu (osoba)", "Nealko balíček (osoba)"]}),
        Module("STOCK", {"title": "Sklad a plytvanie", "subtitle": "Spotreba surovín a hodnota odpisu (plytvanie)",
            "item_label": "Surovina / položka", "loss_label": "Odpis / plytvanie",
            "seed_items": ["Mäso a hydina", "Zelenina a šaláty", "Pečivo", "Mliečne výrobky", "Hotové jedlá (nespotrebované)"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (kuchár / čašník / brigádnik)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Tržby podujatí a vyúčtovanie",
            "source_label": "Faktúry podujatí · zálohy · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena potravín (HACCP)",
                       "Alergény", "Chladiaci reťazec a preprava jedál", "Požiarna ochrana", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 15 — florist_sk  (Kvetinárstvo · NACE 47.76 · fresh-flower retail)
FLORIST_SK = PackSpec(
    key="florist_sk", vertical="Kvetinárstvo", language="sk",
    palette={"primary": "B43C72", "accent": "6FA88C", "ink": "2A1320"},   # rose-magenta + sage
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži kazivosť kvetov, maržu kytíc a obrátku",
            "steps": ["RÁNO: 3 priority + príjem dodávky a rezanie stoniek",
                      "POČAS DŇA: viazanie kytíc, predaj a objednávky",
                      "VEČER: uzávierka + odpis zvädnutých kvetov",
                      "TÝŽDENNE: marža kytíc + obrátka a straty",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: kontrola sviežosti a výmena vody vo vázach",
                          "Otvorenie: objednávky a rozvozy na dnes pripravené",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: zvädnuté kvety odpísané a zapísané",
                          "Zatvorenie: chladenie a sklad zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža kytíc", "MARGIN.avg"),
                     ("Hodnota odpisu (zvädnuté)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (zvädnuté) …", "Kytice pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby kytice a rezané kvety", "Tržby črepníkové rastliny",
                              "Tržby objednávky a rozvoz (svadby, pohreby)", "Tržby doplnky (vázy, darčeky)"],
            "cos_lines": ["Nákup kvetov a rastlín", "Aranžérsky materiál (stuhy, obaly, oázis)"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a chladenie",
                               "Doprava a rozvoz", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža kytíc", "subtitle": "Materiálový náklad na výrobok a marža",
            "unit_label": "Kytica / výrobok",
            "seed_items": ["Kytica zmiešaná", "Ruže (zväzok)", "Svadobná kytica", "Smútočný veniec",
                           "Črepníková rastlina", "Aranžmán v boxe"]}),
        Module("STOCK", {"title": "Sklad a kazivosť", "subtitle": "Spotreba a hodnota odpisu zvädnutých kvetov",
            "item_label": "Kvet / tovar", "loss_label": "Odpis (zvädnuté)",
            "seed_items": ["Ruže", "Tulipány", "Chryzantémy", "Zeleň a listy", "Črepníkové rastliny"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (florista / predavač)", "target_pct": 0.25}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · hotovosť · karty · objednávky"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Bezpečná práca s nožom a náradím",
                       "Skladovanie a chladenie kvetov", "Práca s chemikáliami (hnojivá, konzervanty)",
                       "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 16 — bookkeeper_sk  (Účtovníctvo / účtovná kancelária · NACE 69.20 ·
#              professional service, NO STOCK → 6-KPI dashboard)
BOOKKEEPER_SK = PackSpec(
    key="bookkeeper_sk", vertical="Účtovníctvo / účtovná kancelária", language="sk",
    palette={"primary": "34406B", "accent": "2E9E78", "ink": "161A2B"},   # indigo + emerald (trust)
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži vyťaženosť, maržu na klienta a cash flow",
            "steps": ["RÁNO: 3 priority + termíny a podania (DPH, dane, mzdy)",
                      "POČAS DŇA: spracovanie dokladov a evidencia hodín",
                      "VEČER: fakturácia a stav rozpracovanosti",
                      "TÝŽDENNE: vyťaženosť + marža na klienta",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: termíny podaní na dnes skontrolované (DPH, mzdy)",
                          "Otvorenie: prijaté doklady zaevidované",
                          "Zatvorenie: odpracované hodiny zapísané",
                          "Zatvorenie: vystavené faktúry zapísané",
                          "Zatvorenie: zálohovanie údajov a GDPR zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na klienta", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Klienti pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby vedenie účtovníctva (paušál)", "Tržby mzdy a personalistika",
                              "Tržby dane a poradenstvo (ročné)"],
            "cos_lines": ["Účtovný softvér a licencie", "Subdodávky (audit, právne)"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a internet",
                               "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na klienta", "subtitle": "Náklad času na službu a marža na klienta",
            "unit_label": "Klient / služba",
            "seed_items": ["Jednoduché účtovníctvo (mesačne)", "Podvojné účtovníctvo (mesačne)",
                           "Spracovanie miezd (zamestnanec)", "Daňové priznanie (ročné)", "Poradenstvo (hodina)"]}),
        Module("LABOUR", {"title": "Kapacita", "subtitle": "Vyťaženosť a podiel mzdových nákladov",
            "role_label": "Pozícia (účtovník / asistent)", "target_pct": 0.45}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Vystavené faktúry a úhrady",
            "source_label": "Vystavené faktúry · paušály · prevody · hotovosť"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "GDPR / ochrana osobných údajov",
                       "AML / ochrana pred praním špinavých peňazí", "Legislatíva a zmeny (dane, mzdy)",
                       "Kybernetická bezpečnosť a zálohovanie", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# Phase 13f BATCH 5 — Brewery · Gym · Photographer (pack_queue ids 17/15/22, pri 48)
# ============================================================================

# EXAMPLE 17 — brewery_sk  (Pivovar / remeselné pivo · NACE 11.05 · beer manufacture)
#              production vertical, KEEPS STOCK → 7-KPI dashboard (loss tile present)
BREWERY_SK = PackSpec(
    key="brewery_sk", vertical="Pivovar / remeselné pivo", language="sk",
    palette={"primary": "A6531C", "accent": "E3B23C", "ink": "241405"},   # copper + golden amber
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži výrobu várok, maržu na hl a odpis znehodnoteného piva",
            "steps": ["RÁNO: 3 priority + kontrola várky a kvasenia",
                      "VÝROBA: rmutovanie, chmeľovar, stáčanie podľa receptúry",
                      "POČAS DŇA: výčap / expedícia + kontrola kvality a teplôt",
                      "VEČER: uzávierka + odpis znehodnotených šarží",
                      "MESAČNE: cash flow + prehľad marže na hektoliter"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh výroby a expedície",
            "checklist": ["Otvorenie: teploty kvasných a ležiackych tankov",
                          "Otvorenie: sanitácia liniek a kontrola CO₂",
                          "Zatvorenie: tržby výčapu a veľkoobchodu zapísané",
                          "Zatvorenie: odpis znehodnotených šarží zapísaný",
                          "Zatvorenie: tlakové nádoby a sklad zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža (na hl)", "MARGIN.avg"),
                     ("Hodnota odpisu (znehodnotené)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (znehodnotené) …", "Druhy piva pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby čapované pivo (sudy / hl)", "Tržby fľaše a plechovky",
                              "Tržby tap room / výčap", "Tržby veľkoobchod a distribúcia"],
            "cos_lines": ["Suroviny (slad, chmeľ, kvasinky, voda)", "Obaly (fľaše, plechovky, etikety, sudy)"],
            "overhead_lines": ["Mzdy a personál", "Nájom a poplatky", "Energie a voda",
                               "Spotrebná daň z piva (excise)", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na hl", "subtitle": "Náklad na hektoliter / 0,5 l a marža druhu piva",
            "unit_label": "Druh piva (na hl / 0,5 l)",
            "seed_items": ["Svetlý ležiak 11°", "Polotmavý ležiak 12°", "IPA", "Pšeničné (weizen)",
                           "Stout", "Sezónny špeciál"]}),
        Module("STOCK", {"title": "Sklad a odpis", "subtitle": "Spotreba surovín a hodnota odpisu znehodnotených šarží",
            "item_label": "Surovina / šarža", "loss_label": "Odpis (znehodnotené)",
            "seed_items": ["Slad", "Chmeľ", "Kvasinky", "Hotové pivo (šarža)", "CO₂"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (sládok / stáčač / výčap)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Tržby výčapu a veľkoobchodu",
            "source_label": "Výčap (Z) · faktúry veľkoobchod · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Manipulácia s bremenami", "Hygiena výroby (HACCP)",
                       "Zodpovedný výčap alkoholu", "Tlakové nádoby (CO₂) a sanitačné chemikálie",
                       "Spotrebná daň a evidencia výroby", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 18 — gym_sk  (Fitnescentrum / posilňovňa · NACE 93.13 · fitness facilities)
#              membership-led service, NO STOCK → 6-KPI dashboard
GYM_SK = PackSpec(
    key="gym_sk", vertical="Fitnescentrum / posilňovňa", language="sk",
    palette={"primary": "D7402B", "accent": "1F2933", "ink": "2A0C08"},   # energetic red + graphite
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži členské, vyťaženosť a maržu služieb",
            "steps": ["RÁNO: 3 priority + kontrola strojov a čistoty",
                      "POČAS DŇA: príchody, predaj členstiev a vstupov",
                      "VEČER: uzávierka + obsadenosť a obnovy členstiev",
                      "TÝŽDENNE: vyťaženosť tréningov + marža služieb",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: kontrola strojov a bezpečnosti",
                          "Otvorenie: čistota a dezinfekcia plôch",
                          "Zatvorenie: tržby zapísané (uzávierka Z)",
                          "Zatvorenie: obnovy a nedoplatky členstiev skontrolované",
                          "Zatvorenie: prevádzka a šatne zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža služieb", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Služby pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby členské (mesačné / ročné)", "Tržby jednorazové vstupy",
                              "Tržby osobný tréning (PT)", "Tržby skupinové cvičenia",
                              "Tržby doplnky a nápoje"],
            "cos_lines": ["Vybavenie a údržba strojov", "Licencie (hudba, software, rezervácie)"],
            "overhead_lines": ["Mzdy a tréneri", "Nájom a poplatky", "Energie (kúrenie, voda, klíma)",
                               "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža služieb", "subtitle": "Náklad na službu a marža členstva/služby",
            "unit_label": "Služba / členstvo",
            "seed_items": ["Mesačné členstvo", "Ročné členstvo", "Jednorazový vstup",
                           "Osobný tréning (hodina)", "Skupinová lekcia", "10-vstupová permanentka"]}),
        Module("LABOUR", {"title": "Kapacita", "subtitle": "Vyťaženosť a podiel mzdových nákladov",
            "role_label": "Pozícia (tréner / recepcia)", "target_pct": 0.40}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Denné tržby a uzávierka pokladne",
            "source_label": "Uzávierka (Z) · členské (inkaso) · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Prvá pomoc a resuscitácia (defibrilátor)",
                       "Bezpečné používanie strojov a inštruktáž", "Hygiena a dezinfekcia",
                       "Ochrana osobných údajov (GDPR – členovia)", "Požiarna ochrana a evakuácia", "BOZP"]}),
    ],
)

# EXAMPLE 19 — photographer_sk  (Fotograf / fotoateliér · NACE 74.20 · photographic activities)
#              project-led service, NO STOCK → 6-KPI dashboard
PHOTOGRAPHER_SK = PackSpec(
    key="photographer_sk", vertical="Fotograf / fotoateliér", language="sk",
    palette={"primary": "4A4E69", "accent": "E0A458", "ink": "1B1C28"},   # muted indigo-slate + amber
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu na zákazku, balíčky a rozpracovanosť",
            "steps": ["RÁNO: 3 priority + potvrdenie termínov a fotení",
                      "POČAS FOTENIA: realizácia podľa balíčka a brífingu",
                      "PO FOTENÍ: výber, úprava a odovzdanie + zálohovanie",
                      "TÝŽDENNE: marža na zákazku + stav rozpracovanosti",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: technika nabitá a pamäťové karty pripravené",
                          "Otvorenie: termíny a lokácie na dnes potvrdené",
                          "Zatvorenie: zálohovanie fotiek (2 kópie) urobené",
                          "Zatvorenie: tržby a prijaté zálohy zapísané",
                          "Zatvorenie: vybavenie skontrolované a uložené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na zákazku", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Balíčky pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby svadby a podujatia", "Tržby portréty a rodiny (ateliér)",
                              "Tržby firemné a produktové foto", "Tržby predaj tlače a albumov",
                              "Tržby video"],
            "cos_lines": ["Tlač, albumy a fotoprodukty", "Subdodávky (druhý fotograf, asistent, vizážista)"],
            "overhead_lines": ["Mzdy a personál", "Nájom ateliéru a poplatky",
                               "Technika a software (úpravy, cloud)", "Marketing", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na zákazku", "subtitle": "Náklad na balíček a marža na zákazku",
            "unit_label": "Balíček / zákazka",
            "seed_items": ["Svadobný balíček", "Portrétne fotenie (ateliér)", "Rodinné fotenie (exteriér)",
                           "Firemné headshoty", "Produktové foto (set)", "Fotokniha / album"]}),
        Module("LABOUR", {"title": "Kapacita", "subtitle": "Vyťaženosť a podiel mzdových nákladov",
            "role_label": "Pozícia (fotograf / editor)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Faktúry zákaziek a úhrady",
            "source_label": "Faktúry zákaziek · zálohy · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Ochrana osobných údajov a súhlas (GDPR, právo na podobizeň)",
                       "Zálohovanie a kybernetická bezpečnosť", "Bezpečná práca s technikou a osvetlením",
                       "Autorské práva a licencie", "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# Phase 13f BATCH 6 — Electrician · Plumber · Carpenter (pack_queue ids 19/20/21, pri 45/45/36)
# Construction trades, quote/job-led, NO STOCK → 6-KPI dashboards (like bookkeeper)
# ============================================================================

# EXAMPLE 20 — electrician_sk  (Elektrikár / elektroinštalácie · NACE 43.21)
ELECTRICIAN_SK = PackSpec(
    key="electrician_sk", vertical="Elektrikár / elektroinštalácie", language="sk",
    palette={"primary": "1B3A6B", "accent": "F2C200", "ink": "0E1830"},   # navy + electric yellow
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu na zákazku, materiál vs práca a rozpracovanosť",
            "steps": ["RÁNO: 3 priority + materiál a náradie na zákazky dňa",
                      "NA STAVBE: realizácia podľa cenovej ponuky",
                      "PO PRÁCI: súpis prác, fotodokumentácia, revízne správy",
                      "TÝŽDENNE: marža na zákazku + stav rozpracovanosti",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: náradie, materiál a vozidlo pripravené",
                          "Otvorenie: zákazky a adresy na dnes potvrdené",
                          "Zatvorenie: odpracované hodiny a materiál zapísané",
                          "Zatvorenie: vystavené faktúry a zálohy zapísané",
                          "Zatvorenie: revízne správy a fotodokumentácia uložené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na zákazku", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Zákazky pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby elektroinštalácie (novostavby / rekonštrukcie)",
                              "Tržby opravy a údržba", "Tržby revízie a merania",
                              "Tržby materiál (preúčtovaný)"],
            "cos_lines": ["Elektroinštalačný materiál (káble, ističe, rozvádzače)",
                          "Subdodávky a prenájom mechanizmov"],
            "overhead_lines": ["Mzdy a personál", "Vozidlá a pohonné hmoty", "Náradie a vybavenie",
                               "Poistenie a poplatky", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na zákazku", "subtitle": "Náklad materiálu a práce na zákazku a marža",
            "unit_label": "Zákazka / výkon",
            "seed_items": ["Kompletná elektroinštalácia bytu", "Zapojenie rozvádzača", "Výmena ističa",
                           "Inštalácia zásuvky / vypínača", "Revízia elektroinštalácie", "Inštalácia bleskozvodu"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (elektrikár / pomocník)", "target_pct": 0.35}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Faktúry zákaziek a úhrady",
            "source_label": "Faktúry zákaziek · zálohy · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Odborná spôsobilosť v elektrotechnike (vyhl. 508/2009 Z. z.)",
                       "Práca pod napätím a bezpečnosť", "Práca vo výškach",
                       "Manipulácia s bremenami", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 21 — plumber_sk  (Inštalatér / kúrenár · NACE 43.22)
PLUMBER_SK = PackSpec(
    key="plumber_sk", vertical="Inštalatér / kúrenár", language="sk",
    palette={"primary": "1C6E8C", "accent": "D2691E", "ink": "0C2530"},   # water blue + copper
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu na zákazku, materiál vs práca a rozpracovanosť",
            "steps": ["RÁNO: 3 priority + materiál a náradie na zákazky dňa",
                      "NA STAVBE: realizácia podľa cenovej ponuky (voda, kúrenie, plyn)",
                      "PO PRÁCI: tlakové skúšky, súpis prác, fotodokumentácia",
                      "TÝŽDENNE: marža na zákazku + stav rozpracovanosti",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: náradie, materiál a vozidlo pripravené",
                          "Otvorenie: zákazky a adresy na dnes potvrdené",
                          "Zatvorenie: odpracované hodiny a materiál zapísané",
                          "Zatvorenie: vystavené faktúry a zálohy zapísané",
                          "Zatvorenie: tlakové skúšky a fotodokumentácia uložené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na zákazku", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Zákazky pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby vodoinštalácie a rozvody", "Tržby kúrenie a kotly",
                              "Tržby plynoinštalácie", "Tržby opravy a havárie (pohotovosť)",
                              "Tržby materiál (preúčtovaný)"],
            "cos_lines": ["Inštalačný materiál (rúrky, armatúry, kotly)",
                          "Subdodávky a prenájom mechanizmov"],
            "overhead_lines": ["Mzdy a personál", "Vozidlá a pohonné hmoty", "Náradie a vybavenie",
                               "Poistenie a poplatky", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na zákazku", "subtitle": "Náklad materiálu a práce na zákazku a marža",
            "unit_label": "Zákazka / výkon",
            "seed_items": ["Výmena kotla", "Rekonštrukcia kúpeľne (rozvody)", "Montáž radiátorov",
                           "Oprava havárie (voda)", "Inštalácia bojlera", "Pripojenie plynového spotrebiča"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (inštalatér / pomocník)", "target_pct": 0.35}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Faktúry zákaziek a úhrady",
            "source_label": "Faktúry zákaziek · zálohy · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Odborná spôsobilosť na plynové zariadenia (vyhl. 508/2009 Z. z.)",
                       "Práca s plynom a tlakové skúšky", "Zváranie a práca s otvoreným ohňom",
                       "Práca vo výškach", "Manipulácia s bremenami", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 22 — carpenter_sk  (Stolár / tesár · NACE 43.32 · joinery installation)
CARPENTER_SK = PackSpec(
    key="carpenter_sk", vertical="Stolár / tesár", language="sk",
    palette={"primary": "6B4423", "accent": "8AA63C", "ink": "2A1A0E"},   # walnut brown + sap green
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu na zákazku, materiál vs práca a rozpracovanosť",
            "steps": ["RÁNO: 3 priority + materiál a náradie na zákazky dňa",
                      "V DIELNI / NA STAVBE: výroba a montáž podľa zákazky",
                      "PO PRÁCI: súpis prác, odovzdanie, fotodokumentácia",
                      "TÝŽDENNE: marža na zákazku + stav rozpracovanosti",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: náradie, materiál a vozidlo pripravené",
                          "Otvorenie: zákazky a zameranie na dnes potvrdené",
                          "Zatvorenie: odpracované hodiny a materiál zapísané",
                          "Zatvorenie: vystavené faktúry a zálohy zapísané",
                          "Zatvorenie: dielňa a stroje zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na zákazku", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Zákazky pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby výroba nábytku na mieru", "Tržby montáž (dvere, okná, kuchyne)",
                              "Tržby opravy a renovácie", "Tržby materiál (preúčtovaný)"],
            "cos_lines": ["Materiál (drevo, kovanie, lamino, lak)", "Subdodávky a prenájom"],
            "overhead_lines": ["Mzdy a personál", "Dielňa — nájom a energie", "Vozidlá a pohonné hmoty",
                               "Náradie a stroje", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na zákazku", "subtitle": "Náklad materiálu a práce na zákazku a marža",
            "unit_label": "Zákazka / výrobok",
            "seed_items": ["Kuchyňa na mieru", "Vstavaná skriňa", "Interiérové dvere (montáž)",
                           "Drevené schodisko", "Pracovná doska", "Renovácia nábytku"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (stolár / pomocník)", "target_pct": 0.35}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Faktúry zákaziek a úhrady",
            "source_label": "Faktúry zákaziek · zálohy · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Bezpečná obsluha drevoobrábacích strojov (píly, frézy)",
                       "Práca vo výškach (montáž)", "Manipulácia s bremenami",
                       "Práca s chemikáliami (laky, lepidlá)", "Protipožiarna ochrana (drevný prach)",
                       "BOZP / prvá pomoc"]}),
    ],
)

# ============================================================================
# Phase 13f BATCH 7 — Car dealer · Dental practice (pack_queue ids 18/23) — FINAL drain
# ============================================================================

# EXAMPLE 23 — car_dealer_sk  (Predaj automobilov / autobazár · NACE 45.11)
#              retail with vehicle inventory, KEEPS STOCK → 7-KPI dashboard
CAR_DEALER_SK = PackSpec(
    key="car_dealer_sk", vertical="Predaj automobilov / autobazár", language="sk",
    palette={"primary": "1C3D5A", "accent": "C0392B", "ink": "0F1A26"},   # showroom blue + signal red
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu na vozidlo, obrátku skladu a starnutie zásob",
            "steps": ["RÁNO: 3 priority + obhliadky a skúšobné jazdy",
                      "POČAS DŇA: predaj, protiúčty, financovanie a poistenie",
                      "VEČER: uzávierka + stav skladu vozidiel",
                      "TÝŽDENNE: marža na vozidlo + obrátka a starnutie skladu",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: vozidlá pripravené (čistota, palivo, EČV)",
                          "Otvorenie: obhliadky a skúšobné jazdy na dnes potvrdené",
                          "Zatvorenie: tržby a zálohy zapísané",
                          "Zatvorenie: stav skladu a starnutie vozidiel skontrolované",
                          "Zatvorenie: kľúče a areál zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na vozidlo", "MARGIN.avg"),
                     ("Hodnota odpisu (starnutie)", "STOCK.loss_value"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Čistá marža …", "Hodnota odpisu (starnutie skladu) …", "Vozidlá pod cieľovou maržou …",
                         "Podiel miezd …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby predaj vozidiel (jazdené)", "Tržby predaj vozidiel (nové)",
                              "Tržby financovanie a poistenie (provízie)", "Tržby servis a doplnky"],
            "cos_lines": ["Nákup vozidiel a protiúčty", "Príprava a kondícia (servis, detailing, STK/EK)"],
            "overhead_lines": ["Mzdy a personál (predajcovia)", "Areál a poplatky",
                               "Inzercia a marketing", "Poistenie a financovanie skladu", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na vozidlo", "subtitle": "Náklad obstarania a prípravy na vozidlo a marža",
            "unit_label": "Vozidlo / model",
            "seed_items": ["Malé mestské auto (jazdené)", "Rodinný kombi (jazdené)", "SUV (jazdené)",
                           "Dodávka / úžitkové", "Nové vozidlo (objednávka)", "Luxusný segment"]}),
        Module("STOCK", {"title": "Sklad vozidiel", "subtitle": "Obrátka skladu a hodnota odpisu (starnutie / zľavy)",
            "item_label": "Vozidlo / kategória", "loss_label": "Odpis / zľava (starnutie)",
            "seed_items": ["Vozidlá do 90 dní", "Vozidlá 90–180 dní", "Vozidlá nad 180 dní",
                           "Protiúčty (na predaj)", "Komisný predaj"]}),
        Module("LABOUR", {"title": "Zmeny", "subtitle": "Zmeny a podiel mzdových nákladov",
            "role_label": "Pozícia (predajca / mechanik prípravy)", "target_pct": 0.15}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Predaj vozidiel a úhrady",
            "source_label": "Kúpne zmluvy · zálohy · financovanie · hotovosť · prevody"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "DPH — osobitná úprava (marža) pri jazdených vozidlách",
                       "Limit platby v hotovosti (zákon 394/2012 Z. z.)",
                       "Spotrebiteľské práva a záruka (jazdené vozidlá)",
                       "Ochrana osobných údajov (GDPR)", "AML pri vysokých platbách", "BOZP / prvá pomoc"]}),
    ],
)

# EXAMPLE 24 — dental_sk  (Zubná ambulancia / stomatológia · NACE 86.23)
#              health service, NO STOCK → 6-KPI dashboard
DENTAL_SK = PackSpec(
    key="dental_sk", vertical="Zubná ambulancia / stomatológia", language="sk",
    palette={"primary": "2E8B8B", "accent": "E8A0BF", "ink": "10262A"},   # clinical teal + gum-rose
    modules=[
        Module("METHOD", {"title": "Metóda",
            "subtitle": "Balík, ktorý ustráži maržu na úkon, vyťaženosť kresla a objednávky",
            "steps": ["RÁNO: 3 priority + príprava ambulancie a sterilizácia",
                      "POČAS DŇA: ošetrenia podľa objednávok",
                      "VEČER: uzávierka + evidencia výkonov (poisťovne / priame platby)",
                      "TÝŽDENNE: vyťaženosť kresla + marža na úkon",
                      "MESAČNE: cash flow + prehľad"]}),
        Module("PLANNER", {"title": "Denný plán",
            "subtitle": "Tri priority a jasný rozvrh dňa",
            "checklist": ["Otvorenie: sterilizácia nástrojov a kontrola autoklávu",
                          "Otvorenie: objednávky a recall na dnes potvrdené",
                          "Zatvorenie: výkony a platby zapísané (poisťovňa / priame)",
                          "Zatvorenie: dekontaminácia a biologický odpad zlikvidovaný",
                          "Zatvorenie: zdravotná dokumentácia a zálohovanie zabezpečené"]}),
        Module("DASHBOARD", {"title": "Prehľad",
            "subtitle": "Automatický dashboard — ťahá živé čísla z ostatných hárkov",
            "kpis": [("Ročné tržby", "LEDGER_12M.revenue_total"),
                     ("Hrubá marža", "LEDGER_12M.gross"),
                     ("Čistý zisk", "LEDGER_12M.net"),
                     ("Tržby vs plán", "LEDGER_12M.rev_var"),
                     ("Koncová hotovosť", "LEDGER_12M.cash_close"),
                     ("Priemerná marža na úkon", "MARGIN.avg"),
                     ("Podiel miezd", "LABOUR.pct")],
            "insights": ["Tržby vs plán …", "Čistá marža …", "Podiel miezd …",
                         "Úkony pod cieľovou maržou …", "Rozdiel v pokladni …"]}),
        Module("LEDGER_12M", {"title": "Cash flow", "subtitle": "12-mesačný cash flow a zisk/strata",
            "revenue_lines": ["Tržby úhrady poisťovní (zmluvné výkony)", "Tržby priame platby pacientov (nadštandard)",
                              "Tržby protetika a implantológia", "Tržby dentálna hygiena"],
            "cos_lines": ["Stomatologický materiál (výplne, anestetiká)", "Zubná technika / laboratórium (protetika)"],
            "overhead_lines": ["Mzdy a personál (sestra, hygienička)", "Nájom a poplatky", "Energie",
                               "Prístroje a servis (RTG, kreslo, autokláv)", "Ostatné réžie"]}),
        Module("MARGIN", {"title": "Marža na úkon", "subtitle": "Materiálový náklad na úkon a marža výkonu",
            "unit_label": "Úkon / výkon",
            "seed_items": ["Preventívna prehliadka", "Záchovná výplň (fotokompozit)", "Endodoncia (ošetrenie koreňa)",
                           "Extrakcia zuba", "Dentálna hygiena", "Korunka / protetika"]}),
        Module("LABOUR", {"title": "Kapacita", "subtitle": "Vyťaženosť kresla a podiel mzdových nákladov",
            "role_label": "Pozícia (lekár / sestra / hygienička)", "target_pct": 0.30}),
        Module("TAKINGS", {"title": "Tržby", "subtitle": "Úhrady poisťovní a priame platby",
            "source_label": "Úhrady poisťovní · priame platby · hotovosť · karty"}),
        Module("TRAINING", {"title": "Školenia", "subtitle": "Matica školení — dôkaz pred zmenou",
            "topics": ["Zaškolenie", "Ochrana osobných údajov a zdravotná dokumentácia (GDPR)",
                       "Sterilizácia, hygiena a dekontaminácia", "Prevádzkový poriadok a infekčná kontrola (RÚVZ)",
                       "Radiačná ochrana (RTG zariadenia)", "Nakladanie s nebezpečným / biologickým odpadom",
                       "BOZP / prvá pomoc / KPR"]}),
    ],
)

REGISTRY = {s.key: s for s in (HOSPITALITY_SK, BUTCHER_SK, BAKER_SK,
                               BAR_SK, GREENGROCER_SK, PATISSERIE_SK,
                               HOSPITALITY_EN,
                               HAIRDRESSER_SK, BEAUTY_SALON_SK, BARBER_SK,
                               BNB_SK, CONVENIENCE_SK, AIRBNB_SK,
                               CATERER_SK, FLORIST_SK, BOOKKEEPER_SK,
                               BREWERY_SK, GYM_SK, PHOTOGRAPHER_SK,
                               ELECTRICIAN_SK, PLUMBER_SK, CARPENTER_SK,
                               CAR_DEALER_SK, DENTAL_SK)}


if __name__ == "__main__":
    print("ASSET-FORGE · pack-spec dry-run\n" + "=" * 60)
    ok = True
    for key, spec in REGISTRY.items():
        errs = validate(spec)
        ok = ok and not errs
        print(f"\n▶ {key}  ({spec.vertical} · lang={spec.language} · "
              f"primary=#{spec.palette['primary']})")
        for num, mtype, title in spec.sheet_plan():
            print(f"    {num} · {title:<22} [{mtype}]")
        print("   ", "✅ valid" if not errs else "❌ " + "; ".join(errs))
    # terminology diff — proves the swap on one shared module
    print("\n" + "=" * 60 + "\nTERMINOLOGY SWAP (STOCK module) — same slot, trade words:")
    for key in REGISTRY:
        st = next((m for m in REGISTRY[key].modules if m.type == "STOCK"), None)
        if st is None:
            print(f"  {key:<14} (no STOCK — service-led, 6-KPI dashboard)")
            continue
        print(f"  {key:<14} item='{st.terms['item_label']}'  loss='{st.terms['loss_label']}'"
              f"  e.g. {st.terms['seed_items'][0]}")
    print("\nALL SPECS VALID" if ok else "\nVALIDATION FAILED")
