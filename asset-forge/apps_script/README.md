# Google Sheets "Pro" edition — Apps Script add-on

**Phase 13g · Tiers 1–2 of the agentic stack** (`research/agentic_tech_stack.md`).
Turns any ASSET-FORGE premium pack (`products/pack_*.xlsx`) into a self-running
Google Sheets edition: a **morning briefing**, an **append-only journal**, and an
optional **"ask your data" Gemini sidebar** — all on **free** Google tooling, no
SaaS subscription, no lock-in.

> **Promise to the buyer:** *you bought a pack, not a subscription.* Tier 0 (the
> offline `.xlsx`) works forever with nothing installed. These scripts are an
> **opt-in bonus** for buyers who want automation + AI. Everything here only
> **reads** the pack and **appends** to a journal — it never auto-orders,
> auto-pays, or overwrites your numbers.

---

## What's in this folder (paste-in files)

| File | Tier | What it does |
|---|---|---|
| `Config.gs` | — | Shared config + helpers. **Language-agnostic:** finds sheets by their number prefix (`00`,`01`,`02`,`03`) and reads KPI tiles by position, so it works on every pack (sk/cs/de/…) unchanged. |
| `Menu.gs` | 1 | Adds the **⚙️ ASSET-FORGE** menu; installs/removes the daily + weekly triggers. |
| `Briefing.gs` | 1 | Builds the plain-language **briefing with deltas** (toast + cell note + optional weekly e-mail). |
| `Rollover.gs` | 1 | Appends a dated **journal** snapshot — the history every trend needs. Append-only = safe. |
| `GeminiSidebar.gs` | 2 | Server side of the **Gemini** "ask your data" sidebar (uses the buyer's own free key). |
| `Sidebar.html` | 2 | The chat UI for the sidebar. |

All `.gs` syntax-checked with Node 22 (`node --check`).

---

## Setup — three levels, stop at any one

### Level 0 · Stay offline (no setup)
Just use `products/pack_<vertical>_<lang>.xlsx` in Excel / LibreOffice / Google
Sheets. The dashboard already reads like a tiny analyst. **Nothing below is
required.**

### Level 1 · Turn on automation (free Google account)
1. Upload the pack to Google Drive and **open it as a Google Sheet**
   (`File → Save as Google Sheets`, or import the `.xlsx`).
2. `Extensions → Apps Script`. Delete the empty `Code.gs`.
3. Create the files and paste in the matching contents:
   `Config.gs`, `Menu.gs`, `Briefing.gs`, `Rollover.gs`, `GeminiSidebar.gs`,
   and an **HTML** file named `Sidebar` (paste `Sidebar.html`).
   *File names must match — the sidebar is loaded by the name `Sidebar`.*
4. Save, then reload the spreadsheet. A new **⚙️ ASSET-FORGE** menu appears.
5. `⚙️ ASSET-FORGE → ▶️ Zapnúť automatiku`. Approve the one-time permission
   prompt (Google shows "unverified app" for personal scripts — that's normal;
   it's *your* script in *your* file).
   - Nightly ≈23:00 → journal snapshot + refreshed briefing note (hover cell **A1**
     on the `02 · Prehľad` sheet).
   - Monday ≈07:00 → weekly summary. To e-mail it, set `EMAIL_TO` in `Config.gs`.
6. Run a briefing anytime: `⚙️ ASSET-FORGE → 📋 Dnešný briefing`.

### Level 2 · Add the AI (free Gemini key)
1. Get a free key at **aistudio.google.com/apikey**.
2. `⚙️ ASSET-FORGE → 🔑 Nastaviť Gemini API kľúč` → paste it.
   *Stored only in this file's Document Properties — never committed, never sent
   to us.*
3. `⚙️ ASSET-FORGE → 💬 Spýtaj sa svojich dát` opens the sidebar. Ask in plain
   language ("Kde strácam najviac peňazí?"). Answers are **grounded** in your
   dashboard KPIs + insights only.
4. With a key set, the daily briefing is also auto-rewritten into a warmer
   paragraph (falls back to the plain version if the free limit is hit).

---

## How it stays grounded & safe
- The AI only ever sees your **live KPI tiles** + the **Postrehy** sentences the
  pack already computes — not invented data. If the numbers don't support an
  answer, it says so.
- **Read-only by design:** scripts read the pack and *append* to `Denník`. They
  never edit your ledger, never order stock, never move money. Delete a journal
  row to undo.
- **Your data, your account, your key.** No third-party add-on, no recurring fee.

## Honest limits (don't over-promise in listings)
- A live AI **cannot** run in an offline `.xlsx` — Tier 2 needs the Sheets
  edition + a free Gemini key.
- Free Gemini / Apps Script have **usage limits that change** — frame AI as a
  *bonus*, and re-verify limits live before any listing claim
  (dated 31/05/2026).
- Slovak UI strings are **build-proof grade** → native-editor pass before any
  public listing (standing pre-launch task).

## Sources
- https://developers.google.com/apps-script/guides/triggers/installable
- https://ai.google.dev/gemini-api/docs/quickstart (REST `generateContent`)
- `research/agentic_tech_stack.md` §1–§5 (the layered stack + trust line)
