/**
 * ASSET-FORGE · Premium Pack — Google Sheets "Pro" edition
 * =========================================================
 * Phase 13g · Tier 1–2 of the agentic stack (see research/agentic_tech_stack.md).
 *
 *   Tier 0  the offline .xlsx pack            (no code, works on open)
 *   Tier 1  Apps Script automation  ← THIS    (briefing + journal + triggers)
 *   Tier 2  Gemini in-sheet AI       ← THIS    (grounded "ask your data" sidebar)
 *
 * EVERYTHING here is FREE to run on a personal Google account. Nothing is
 * irreversible: the scripts only READ the pack and APPEND to a journal — they
 * never auto-order, auto-pay, or overwrite the owner's numbers. That is the
 * trust line (agentic_tech_stack.md §2).
 *
 * Config.gs — shared configuration + helpers.
 * LANGUAGE-AGNOSTIC BY DESIGN: sheets are matched by their numeric prefix
 * ("00", "01", "02", "03"…), which is identical across every pack and every
 * language (sk/cs/de/hu/pl/en). So the same code runs on bar_sk, baker_sk,
 * greengrocer_sk … with zero edits. KPI tiles are read by POSITION, not by
 * label text, so a butcher's "Hodnota orezu" and a bar's "Hodnota strát" are
 * both picked up automatically.
 *
 * The KPI tile geometry mirrors scripts/build_pack.py → build_dashboard():
 *   - tiles laid out in a 3-column grid; columns B / F / J  (1-indexed 2 / 6 / 10)
 *   - row groups start at top = 5, 10, 15, 20  → label row = top+1, value row = top+2
 *   - up to 7 KPIs (the dashboard never exceeds two rows of three + one)
 */

var AF = {
  /** Numeric prefixes of the fixed spine (pack_spec.py FIXED + LEDGER_12M). */
  PREFIX: {
    METHOD:    '00',   // 00 · Metóda
    PLANNER:   '01',   // 01 · Denný plán
    DASHBOARD: '02',   // 02 · Prehľad   ← KPI tiles + Postrehy insights live here
    LEDGER:    '03'    // 03 · Cash flow
  },

  /** Where the period journal (append-only history) is kept. Auto-created. */
  JOURNAL_SHEET: 'Denník',

  /** Document-property keys (per-file storage, survives across runs). */
  PROP_SNAPSHOT: 'AF_LAST_SNAPSHOT',   // last KPI snapshot, for deltas
  PROP_GEMINI:   'GEMINI_API_KEY',     // owner's OWN free Gemini key (Tier 2)

  /**
   * Weekly e-mail recipient. Leave '' to disable the e-mail (toast + journal
   * still run). Set to the owner's address to receive a Monday summary.
   */
  EMAIL_TO: '',

  /** Gemini (Tier 2) — free-tier model. Re-verify availability live (limits move). */
  GEMINI_MODEL: 'gemini-1.5-flash',

  /** Dashboard KPI tile geometry (see header). 1-indexed rows/cols. */
  KPI_COLS:      [2, 6, 10],          // B, F, J
  KPI_TOP_ROWS:  [5, 10, 15, 20]      // group anchors → label = +1, value = +2
};


/** Return the spreadsheet whose tab name starts with `prefix` (e.g. '02'). */
function afSheetByPrefix(prefix) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var name = sheets[i].getName();
    // tolerant match: "02 · Prehľad", "02 Prehľad", "02·Prehľad", "02. Prehľad"
    if (name.replace(/^\s+/, '').indexOf(prefix) === 0) return sheets[i];
  }
  return null;
}

function afDashboard() { return afSheetByPrefix(AF.PREFIX.DASHBOARD); }


/**
 * Read every populated KPI tile off the dashboard by POSITION.
 * Returns [{ label, value, a1 }] in reading order. Stops a column group once
 * an empty label is hit, so 6-KPI and 7-KPI packs both work.
 */
function afReadKpis() {
  var sh = afDashboard();
  if (!sh) throw new Error('Dashboard sheet (prefix "' + AF.PREFIX.DASHBOARD + '") not found.');
  var out = [];
  for (var g = 0; g < AF.KPI_TOP_ROWS.length; g++) {
    var top = AF.KPI_TOP_ROWS[g];
    for (var c = 0; c < AF.KPI_COLS.length; c++) {
      var col = AF.KPI_COLS[c];
      var label = String(sh.getRange(top + 1, col).getDisplayValue() || '').trim();
      if (!label) continue;                       // empty tile slot → skip
      var valCell = sh.getRange(top + 2, col);
      var value = valCell.getValue();
      if (typeof value !== 'number') {
        var n = parseFloat(String(value).replace(/[^0-9.\-]/g, ''));
        value = isNaN(n) ? null : n;
      }
      out.push({
        label: label,
        value: value,
        display: valCell.getDisplayValue(),
        a1: valCell.getA1Notation()
      });
    }
  }
  return out;
}


/** Read the dashboard "Postrehy" insight sentences (already computed by formulas). */
function afReadInsights() {
  var sh = afDashboard();
  if (!sh) return [];
  var data = sh.getDataRange().getDisplayValues();
  var insights = [];
  // insight rows live below the KPI grid; they are long sentences in column B.
  for (var r = AF.KPI_TOP_ROWS[1] + 3; r < data.length; r++) {
    var cell = String(data[r][1] || '').trim();   // column B (index 1)
    if (cell.length > 25 && /[:.]/.test(cell)) insights.push(cell);
  }
  return insights;
}
