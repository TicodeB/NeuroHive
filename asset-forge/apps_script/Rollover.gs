/**
 * ASSET-FORGE · Premium Pack — Google Sheets "Pro" edition
 * Rollover.gs — Tier 1 period bookkeeping (the "month rollover" trail).
 *
 * The pack's 03 · Cash flow is a 12-month ledger; the owner enters numbers as
 * the year unfolds. This script keeps an APPEND-ONLY history ("Denník") so the
 * business builds a dated record over time — the raw material every later
 * trend/briefing needs. It NEVER edits the owner's ledger or overwrites a past
 * row: it only adds a new line. That keeps the rollover safe and reversible
 * (just delete the row), honouring the trust line in agentic_tech_stack.md §2.
 *
 * Each row = a timestamp + a snapshot of every dashboard KPI, in the KPI's own
 * trade language (the header is built from the live labels, so a butcher pack
 * logs "Hodnota orezu" and a bar pack logs "Hodnota strát" automatically).
 */

/** Menu target — write today's snapshot row now. */
function afJournalNow() {
  var sh = afJournalAppend();
  SpreadsheetApp.getActive().toast(
    'Zapísané do denníka „' + sh.getName() + '".', '🗒️ Denník', 6);
}


/**
 * Append one snapshot row to the journal sheet, creating + heading it on first
 * use. Returns the journal sheet. Idempotent header: re-syncs if KPIs change.
 */
function afJournalAppend() {
  var ss = SpreadsheetApp.getActive();
  var kpis = afReadKpis();
  var sh = ss.getSheetByName(AF.JOURNAL_SHEET);

  var header = ['Dátum a čas'].concat(kpis.map(function (k) { return k.label; }));
  if (!sh) {
    sh = ss.insertSheet(AF.JOURNAL_SHEET);
    sh.appendRow(header);
    sh.getRange(1, 1, 1, header.length).setFontWeight('bold');
    sh.setFrozenRows(1);
  } else if (sh.getLastRow() === 0) {
    sh.appendRow(header);
    sh.getRange(1, 1, 1, header.length).setFontWeight('bold');
    sh.setFrozenRows(1);
  } else {
    // keep the header in sync if a pack version adds/removes a KPI
    var existing = sh.getRange(1, 1, 1, sh.getLastColumn()).getDisplayValues()[0];
    if (existing.length !== header.length) {
      sh.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');
    }
  }

  var tz = Session.getScriptTimeZone();
  var stamp = Utilities.formatDate(new Date(), tz, 'dd/MM/yyyy HH:mm');   // EU format
  var row = [stamp].concat(kpis.map(function (k) { return k.value; }));
  sh.appendRow(row);
  return sh;
}
