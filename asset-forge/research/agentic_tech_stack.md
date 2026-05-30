# Agentic Tech Stack — How a Premium Pack Runs a Client's Business

**Date:** 30/05/2026 · **Owner:** Samuel · **Branch:** `claude/cool-planck-rYR4I`
**Decisions locked (Samuel, 30/05):** ship **BOTH** Excel + Google Sheets · add **Notion +
NotebookLM** to the stack · pilot = **re-skin the existing hospitality flagship** in one
language · AI = **insights now, sidebar later**.

> **The promise to the client:** *"You bought a pack, not a subscription. It works the
> moment you open it. The smarter, more automated layers are there if you want them — all
> on free tools, none locking you in."* Every tier below is **free to run** and **opt-in**.
> The client never pays a recurring SaaS fee to *us*.

---

## 1. The layered stack (each layer adds autonomy; none is mandatory)

```
        ┌─────────────────────────────────────────────────────────────┐
TIER 3  │  KNOWLEDGE + WORKSPACE   Notion companion  ·  NotebookLM Q&A   │  "ask my business"
        ├─────────────────────────────────────────────────────────────┤
TIER 2  │  IN-SHEET AI            Google Sheets + Apps Script + Gemini   │  "it briefs me"
        ├─────────────────────────────────────────────────────────────┤
TIER 1  │  AUTOMATION             Google Sheets + free Apps Script       │  "it does chores"
        ├─────────────────────────────────────────────────────────────┤
TIER 0  │  THE PACK (offline)     Clean .xlsx  ·  formula insights       │  "just open it"
        └─────────────────────────────────────────────────────────────┘
                 ▲ every tier is the SAME data model — you climb only if you want to
```

| Tier | What it is | Tools (all free) | What the client experiences |
|---|---|---|---|
| **0 — The Pack** | The premium offline `.xlsx`. Daily planner + jargon'd operational tabs + dashboard with **built-in insight formulas** | Excel / LibreOffice / Google Sheets — no account needed | Opens it, types today's numbers, sees a clean dashboard that *reads like a tiny analyst* ("Top cost: meat 41%", "Margin −3pts vs last week"). **No SaaS, no login.** |
| **1 — Automation** | The Google Sheets edition of the same pack + **free Google Apps Script** | Google account (free) + Apps Script (free) | Nightly/weekly script does the chores: month rollover, "Today's Briefing" cell, auto-PDF the invoice, email the weekly summary. Runs itself. |
| **2 — In-sheet AI** | Apps Script sidebar that calls **Gemini** with the client's *own free API key* | Gemini free tier + Apps Script | A "💬 Ask your data" sidebar. "Why was last week slow?" → plain-language answer grounded in their sheet. Their key, their data, **no add-on subscription**. |
| **3 — Knowledge + workspace** | (a) **Notion companion** = the method + planner + linked databases as a Notion template. (b) **NotebookLM** loaded with the pack's Method handbook (+ their export) as a grounded Q&A assistant | Notion free · NotebookLM free | "How do I do a stock-take properly?" → NotebookLM answers *from the handbook we shipped*. Notion gives a mobile, shareable task/planner view. |

---

## 2. How it works AGENTICALLY for the client (the loop)

The agentic bit = the client stops *operating* the spreadsheet and starts *being served* by
it. The data they already enter triggers a quiet loop:

```
  client enters daily data  ──►  Apps Script time-trigger (nightly)
        ▲                              │
        │                              ▼
   gets a plain-language        compute KPIs + deltas (formulas)
   "morning briefing"                  │
   (email / Sheet cell /               ▼
    Notion / phone)            Gemini writes the briefing  ──►  flags exceptions
                                       │                         ("order beef — 2 days left")
                                       ▼
                               (optional) push to Notion task / send email
```

- **Trigger, not chat:** the value is it runs *without being asked* — the agent wakes on a
  schedule, reads the sheet, and only bothers the owner when something needs a decision.
- **Grounded, not hallucinated:** Gemini/NotebookLM only ever see (a) the client's own sheet
  data and (b) the Method handbook we ship — so answers stay on-rails and on-jargon.
- **Owner stays in control:** every action is a suggestion or a summary; nothing
  irreversible happens autonomously (no auto-ordering, no auto-payments) — that's the trust line.

### What each external tool genuinely contributes
- **Google Apps Script** — the free "cron + glue." This is the actual automation engine. No server, no cost.
- **Gemini (free key)** — turns numbers into sentences and answers ad-hoc questions *inside* the sheet.
- **NotebookLM** — the **how-do-I** assistant, grounded in the per-industry Method handbook PDF we author (great place to *generate* that handbook content too). It is NOT a spreadsheet engine — it's the manual that talks back.
- **Notion** — the mobile/shareable face + a second sellable format (some buyers live in Notion). Linked databases mirror the sheet's structure; Notion's own automations can nudge tasks.

---

## 3. What WE (the seller) ship to enable each tier

| Deliverable | Enables | Build phase |
|---|---|---|
| `scripts/design_system.py` (reusable openpyxl styling) | premium look on every pack | 13b |
| Re-skinned flagship `.xlsx` + insight-formula block | Tier 0 | 13b |
| Standard **pack skeleton** (Method · Planner · Dashboard · ops tabs · Settings) | all tiers | 13c |
| `apps_script/` — `rollover.gs`, `briefing.gs`, `gemini_sidebar.gs` (paste-in, documented) | Tiers 1–2 | 13e |
| Per-industry **Method handbook** (PDF/Doc) | NotebookLM Tier 3 + buyer onboarding | 13c/13f |
| **Notion template** mirror of the skeleton | Tier 3 / second format | later sub-phase |
| Setup guide per tier ("Stay offline" / "Turn on automation" / "Add the AI") | adoption without support load | each phase |

---

## 4. Why this beats the SaaS competitors (the pitch)

- **They rent you software monthly; we sell you the machine once.** Same automation, same AI,
  zero recurring fee to us — the client only ever uses *free* Google/Notion tiers.
- **No lock-in:** data lives in the client's own file/account. They can stop at Tier 0 forever.
- **Their language, their trade:** jargon + Method handbook per vertical (butcher, retailer,
  …) and per language (SK/CS/DE/HU/PL/EN) — something no generic SaaS does.
- **Graduated trust:** start offline, add automation when ready, add AI when curious. The
  upgrade path *is* the value ladder (and our upsell path).

---

## 5. Honest constraints (do not over-promise in listings)
- A **live AI cannot run inside an offline `.xlsx`** — the AI tiers require the Sheets edition + the client's free Gemini key.
- **Apps Script / Gemini / NotebookLM need a (free) Google account** — Tier 0 is the only truly account-free experience.
- **Notion AI is paid;** the Notion *companion template* is free to use, but don't promise Notion's own AI as included.
- Free Gemini / NotebookLM have **usage limits** and **change** — verify live before any listing claim, and frame AI as "bonus," not the core product.

---

## 6. Sources
- https://basescripts.com/build-a-spreadsheet-chatbot-with-google-apps-script-and-gemini
- https://gptforwork.com/blog/how-to-use-ai-in-google-sheets
- https://support.google.com/docs/answer/14218565 (Gemini in Sheets)
- https://buildwithnotion.com/blog/best-marketplaces-notion-templates/

> Free-tier limits / AI feature availability dated 30/05/2026 — re-verify live at listing time.
</content>
