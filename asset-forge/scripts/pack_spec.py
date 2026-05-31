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

REGISTRY = {s.key: s for s in (HOSPITALITY_SK, BUTCHER_SK, BAKER_SK,
                               BAR_SK, GREENGROCER_SK, PATISSERIE_SK)}


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
        st = next(m for m in REGISTRY[key].modules if m.type == "STOCK")
        print(f"  {key:<14} item='{st.terms['item_label']}'  loss='{st.terms['loss_label']}'"
              f"  e.g. {st.terms['seed_items'][0]}")
    print("\nALL SPECS VALID" if ok else "\nVALIDATION FAILED")
