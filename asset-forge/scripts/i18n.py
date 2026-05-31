#!/usr/bin/env python3
"""
ASSET-FORGE · Phase 13h — localisation string table (i18n)
==========================================================
The Premium-Pack track is "one language per file" (Samuel, 30/05). Until now the
generic builder (`build_pack.py`) hardcoded its UI chrome in Slovak — section
headers, column headers, help notes, dropdown lists, status words and the
dashboard insight-formula text. That made every pack Slovak-only.

This module externalises ALL of that chrome into a per-language table so cloning
a vertical into a new language = "add a language block here + translate the
PackSpec terminology", with ZERO builder changes. `sk` is the reference block and
reproduces the previous hardcoded strings byte-for-byte (so existing SK packs are
an exact regression). `en` is the first clone, authored at native quality.

  · Terminology (trade words: revenue lines, seed items…) lives in the PackSpec.
  · Chrome (the fixed UI furniture) lives here, keyed by language.

Adding a language later (cs/de/hu/pl): copy the `sk` block, translate every
value natively, and add a PackSpec in that language. The builder needs no edits.
Public copy in any non-English language still requires a native-editor pass
before listing (standing rule).

Insight-formula values are Python format templates: the builder substitutes the
live cell references ({rev_plan}, {rv}, {rvp}, {net}, {rev}, {pct}, {loss},
{bt}, {vt}). The text around them is what gets translated.
"""
from __future__ import annotations

# ---------------------------------------------------------------- Slovak (ref)
SK = {
    "lang_name": "Slovenčina",
    # method sheet
    "method_contains": "Čo balík obsahuje",
    "method_how": "Metóda — ako to používať",
    "method_colors": "Farby",
    "method_color_note": "Oranžová = vyplníte vy   ·   Modrá = vypočíta sa automaticky   ·   Biela/sivá = záznamy",
    "footer_region": "EU (Írsko)",
    "footer_tail": "Šablóna — nie je finančné ani právne poradenstvo.",
    # common
    "business_name": "Názov prevádzky",
    "year": "Rok",
    "period": "Obdobie",
    "month": "Mesiac",
    "total_year": "Spolu (rok)",
    # planner
    "planner_date": "Dátum",
    "planner_day": "Deň",
    "planner_priorities": "Dnešné 3 priority",
    "planner_schedule": "Rozvrh dňa",
    "planner_openclose": "Otvorenie / Zatvorenie",
    "planner_head": ["Čas", "Úloha", "Priorita", "Hotovo"],
    "dv_priority": "Vysoká,Stredná,Nízka",
    "dv_yesno": "Áno,Nie",
    "dv_days": "Po,Ut,St,Št,Pi,So,Ne",
    # ledger
    "ledger_note": ("Vyplňte oranžové bunky (mesačné skutočnosti + ročný plán). Súčty, marža, zisk, "
                    "odchýlka od plánu a koncová hotovosť sa počítajú automaticky."),
    "months": ["Jan", "Feb", "Mar", "Apr", "Máj", "Jún", "Júl", "Aug", "Sep", "Okt", "Nov", "Dec"],
    "ledger_item_head": "Položka",
    "ledger_head_year": "Rok",
    "ledger_head_var_eur": "Odchýlka €",
    "ledger_head_var_pct": "Odchýlka %",
    "ledger_plan_default": "Plán",
    "ledger_sec_revenue": "TRŽBY",
    "ledger_sec_cos": "NÁKLADY NA PREDAJ",
    "ledger_sec_overhead": "RÉŽIE",
    "ledger_sec_cash": "HOTOVOSŤ",
    "ledger_revenue_total": "Tržby spolu",
    "ledger_cos_total": "Náklady spolu",
    "ledger_gross": "HRUBÁ MARŽA",
    "ledger_overhead_total": "Réžie spolu",
    "ledger_net": "ČISTÝ ZISK",
    "ledger_cash_open": "Počiatočná hotovosť",
    "ledger_cash_close": "Koncová hotovosť",
    # margin
    "margin_note": "Zadajte náklady a cieľovú maržu. Odporúčaná cena (bez DPH) sa vypočíta; vedľa vidíte reálnu maržu.",
    "margin_head": ["Veľkosť", "Náklady €", "Cieľ marža %", "Odpor. cena €", "Cena v menu €", "Reálna marža %", "Stav"],
    "margin_low": "NÍZKA",
    "margin_ok": "OK",
    "margin_avg": "Priemerná reálna marža",
    "margin_below": "Položky pod cieľom",
    # stock
    "stock_note": "Hodnota strát sa počíta automaticky. Vysoké straty sa zvýraznia — konajte pri úniku.",
    "stock_head_unit": "Jedn.",
    "stock_head_open": "Počiatočné",
    "stock_head_buy": "Nákup",
    "stock_head_close": "Koncové",
    "stock_qty_suffix": "(množ.)",
    "stock_unit_price": "Cena/jedn. €",
    "stock_value_tmpl": "Hodnota — {loss} €",
    "stock_total_tmpl": "{loss} — spolu",
    # labour
    "labour_week": "Týždeň od",
    "labour_sales_plan": "Plán tržieb €",
    "labour_note_tmpl": "Náklad = hodiny × sadzba. Cieľ pre tento odbor býva ~{pct} % tržieb.",
    "labour_head": ["Pozícia", "Deň", "Od", "Do", "Hodiny", "Sadzba €/h", "Náklad €"],
    "labour_total": "Mzdové náklady spolu",
    "labour_pct": "Podiel miezd na tržbách",
    # takings
    "takings_note_tmpl": "Zdroje: {src}. Rozdiel = (hotovosť + karty) − uzávierka; hodnoty mimo nuly sa zvýraznia.",
    "takings_head": ["Dátum", "Uzávierka € (Z)", "Hotovosť €", "Karty €", "Vklad €", "Spolu spočítané €", "Rozdiel €", "Kontroloval"],
    # training
    "training_note": "Zadajte dátum absolvovania (DD/MM/RRRR). Prázdna bunka = chýbajúce školenie pred prácou.",
    "training_head_employee": "Zamestnanec",
    "training_head_start": "Nástup",
    "training_head_retrain": "Preškolenie",
    "training_legal_note": "Pozn.: podľa zákona o BOZP musia byť zamestnanci školení na svoju prácu — maticu udržiavajte aktuálnu.",
    # dashboard
    "dash_insights": "Postrehy",
    "dash_auto_note": "Tieto čísla sa aktualizujú automaticky, keď vyplníte ostatné hárky.",
    "ins_rev_plan": ('=IFERROR(IF({rev_plan}="","Tržby vs plán: zadajte ročný plán v hárku Cash flow.",'
                     '"Tržby vs plán: "&TEXT({rv},"#,##0 €")&" ("&TEXT({rvp},"+0.0%;-0.0%")&") — "&'
                     'IF({rvp}>=0,"NAD plánom.","POD plánom, preverte hlavný zdroj tržieb.")),'
                     '"Tržby vs plán: zatiaľ bez dát.")'),
    "ins_net": ('=IFERROR("Čistá marža: "&TEXT({net}/{rev},"0.0%")&IF({net}/{rev}>=0.1,'
                '" — zdravé."," — pozor, je nízka."),"Čistá marža: zatiaľ bez dát.")'),
    "ins_labour": ('=IFERROR("Podiel miezd: "&TEXT({pct},"0.0%")&IF({pct}>0.35,'
                   '" — NAD cieľom 35 %."," — v poriadku."),"Podiel miezd: zatiaľ bez dát.")'),
    "ins_stock": '=IFERROR("Hodnota strát/odpisu: "&TEXT({loss},"#,##0.00 €")&".","Straty: zatiaľ bez dát.")',
    "ins_margin": '=IFERROR("Položky pod cieľovou maržou: "&TEXT({bt},"0")&".","Marža: zatiaľ bez dát.")',
    "ins_takings": ('=IFERROR("Rozdiel v pokladni (rok): "&TEXT({vt},"#,##0.00 €")&IF(ABS({vt})>1,'
                    '" — preverte."," — sedí."),"Pokladňa: zatiaľ bez dát.")'),
}

# ---------------------------------------------------------------- English
EN = {
    "lang_name": "English",
    "method_contains": "What's in the pack",
    "method_how": "Method — how to use it",
    "method_colors": "Colours",
    "method_color_note": "Orange = you fill in   ·   Blue = calculated automatically   ·   White/grey = records",
    "footer_region": "EU (Ireland)",
    "footer_tail": "Template — not financial or legal advice.",
    "business_name": "Business name",
    "year": "Year",
    "period": "Period",
    "month": "Month",
    "total_year": "Total (year)",
    "planner_date": "Date",
    "planner_day": "Day",
    "planner_priorities": "Today's 3 priorities",
    "planner_schedule": "Day schedule",
    "planner_openclose": "Opening / Closing",
    "planner_head": ["Time", "Task", "Priority", "Done"],
    "dv_priority": "High,Medium,Low",
    "dv_yesno": "Yes,No",
    "dv_days": "Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    "ledger_note": ("Fill in the orange cells (monthly actuals + annual plan). Totals, margin, profit, "
                    "variance from plan and closing cash are calculated automatically."),
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "ledger_item_head": "Item",
    "ledger_head_year": "Year",
    "ledger_head_var_eur": "Variance €",
    "ledger_head_var_pct": "Variance %",
    "ledger_plan_default": "Plan",
    "ledger_sec_revenue": "REVENUE",
    "ledger_sec_cos": "COST OF SALES",
    "ledger_sec_overhead": "OVERHEADS",
    "ledger_sec_cash": "CASH",
    "ledger_revenue_total": "Total revenue",
    "ledger_cos_total": "Total costs",
    "ledger_gross": "GROSS MARGIN",
    "ledger_overhead_total": "Total overheads",
    "ledger_net": "NET PROFIT",
    "ledger_cash_open": "Opening cash",
    "ledger_cash_close": "Closing cash",
    "margin_note": "Enter costs and target margin. The recommended price (ex VAT) is calculated; the real margin shows alongside.",
    "margin_head": ["Size", "Cost €", "Target margin %", "Rec. price €", "Menu price €", "Real margin %", "Status"],
    "margin_low": "LOW",
    "margin_ok": "OK",
    "margin_avg": "Average real margin",
    "margin_below": "Items below target",
    "stock_note": "Loss value is calculated automatically. High losses are highlighted — act on leaks.",
    "stock_head_unit": "Unit",
    "stock_head_open": "Opening",
    "stock_head_buy": "Purchases",
    "stock_head_close": "Closing",
    "stock_qty_suffix": "(qty)",
    "stock_unit_price": "Unit price €",
    "stock_value_tmpl": "Value — {loss} €",
    "stock_total_tmpl": "{loss} — total",
    "labour_week": "Week of",
    "labour_sales_plan": "Revenue plan €",
    "labour_note_tmpl": "Cost = hours × rate. Target for this sector is usually ~{pct}% of revenue.",
    "labour_head": ["Position", "Day", "From", "To", "Hours", "Rate €/h", "Cost €"],
    "labour_total": "Total labour cost",
    "labour_pct": "Labour as % of revenue",
    "takings_note_tmpl": "Sources: {src}. Difference = (cash + cards) − Z-reading; non-zero values are highlighted.",
    "takings_head": ["Date", "Z-reading €", "Cash €", "Cards €", "Deposit €", "Counted total €", "Difference €", "Checked by"],
    "training_note": "Enter the date completed (DD/MM/YYYY). Empty cell = missing training before work.",
    "training_head_employee": "Employee",
    "training_head_start": "Start",
    "training_head_retrain": "Refresher",
    "training_legal_note": "Note: health & safety law requires staff to be trained for their job — keep the matrix current.",
    "dash_insights": "Insights",
    "dash_auto_note": "These figures update automatically as you fill in the other sheets.",
    "ins_rev_plan": ('=IFERROR(IF({rev_plan}="","Revenue vs plan: enter the annual plan on the Cash flow sheet.",'
                     '"Revenue vs plan: "&TEXT({rv},"#,##0 €")&" ("&TEXT({rvp},"+0.0%;-0.0%")&") — "&'
                     'IF({rvp}>=0,"ABOVE plan.","BELOW plan, check your main revenue source.")),'
                     '"Revenue vs plan: no data yet.")'),
    "ins_net": ('=IFERROR("Net margin: "&TEXT({net}/{rev},"0.0%")&IF({net}/{rev}>=0.1,'
                '" — healthy."," — careful, low."),"Net margin: no data yet.")'),
    "ins_labour": ('=IFERROR("Labour share: "&TEXT({pct},"0.0%")&IF({pct}>0.35,'
                   '" — ABOVE the 35% target."," — fine."),"Labour share: no data yet.")'),
    "ins_stock": '=IFERROR("Loss/waste value: "&TEXT({loss},"#,##0.00 €")&".","Losses: no data yet.")',
    "ins_margin": '=IFERROR("Items below target margin: "&TEXT({bt},"0")&".","Margin: no data yet.")',
    "ins_takings": ('=IFERROR("Till difference (year): "&TEXT({vt},"#,##0.00 €")&IF(ABS({vt})>1,'
                    '" — review."," — matches."),"Till: no data yet.")'),
}

STRINGS = {"sk": SK, "en": EN}


def get_strings(lang: str) -> dict:
    """Return the chrome string table for `lang`, or raise with a clear message."""
    if lang not in STRINGS:
        raise KeyError(
            f"i18n: no string table for language {lang!r}. Add a block to "
            f"scripts/i18n.py (copy 'sk', translate natively) before building a "
            f"{lang!r} pack. Available: {sorted(STRINGS)}")
    return STRINGS[lang]


if __name__ == "__main__":
    # parity check: every language must define the same keys as the sk reference
    ref = set(SK)
    print("i18n languages:", ", ".join(f"{k} ({v['lang_name']})" for k, v in STRINGS.items()))
    ok = True
    for lang, tbl in STRINGS.items():
        missing, extra = ref - set(tbl), set(tbl) - ref
        if missing or extra:
            ok = False
            print(f"  ❌ {lang}: missing={sorted(missing)} extra={sorted(extra)}")
        else:
            print(f"  ✅ {lang}: {len(tbl)} keys, complete")
    print("ALL LANGUAGE TABLES COMPLETE" if ok else "TABLE MISMATCH")
