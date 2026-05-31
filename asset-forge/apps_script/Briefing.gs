/**
 * ASSET-FORGE · Premium Pack — Google Sheets "Pro" edition
 * Briefing.gs — Tier 1 "morning briefing".
 *
 * Turns the live dashboard numbers into a plain-language summary WITH DELTAS
 * (vs the last snapshot), so the owner is *served by* the sheet instead of
 * reading it. No AI required — pure formulas + Apps Script. If the Gemini key
 * is set (Tier 2), the briefing is additionally rewritten into a warmer,
 * grounded paragraph; otherwise the deterministic version is used.
 *
 * Delivery (non-destructive, every one optional):
 *   · a toast at the bottom of the screen        (afRunBriefingNow)
 *   · a cell NOTE on the dashboard A1            (afWriteBriefingNote)
 *   · a Monday e-mail                            (afWeekly, if EMAIL_TO set)
 */

/** Menu target — build the briefing and show it now. */
function afRunBriefingNow() {
  var text = afBuildBriefing(false);
  afWriteBriefingNote(text);
  SpreadsheetApp.getActive().toast(text, '📋 Dnešný briefing', 30);
}


/**
 * Build the briefing string. Reads KPIs by position, compares to the stored
 * snapshot, and lists the precomputed dashboard insights (Postrehy).
 * @param {boolean} weekly  prefix the heading for the weekly run.
 */
function afBuildBriefing(weekly) {
  var kpis = afReadKpis();
  var prev = afLoadSnapshot();
  var tz = Session.getScriptTimeZone();
  var stamp = Utilities.formatDate(new Date(), tz, 'dd/MM/yyyy');   // EU date
  var lines = [];
  lines.push((weekly ? 'TÝŽDENNÝ' : 'DNEŠNÝ') + ' BRIEFING · ' + stamp);
  lines.push('');

  kpis.forEach(function (k) {
    var line = '• ' + k.label + ': ' + (k.display || k.value);
    if (prev && prev[k.label] != null && k.value != null) {
      var d = k.value - prev[k.label];
      if (Math.abs(d) > 0.0001) {
        var arrow = d > 0 ? '▲' : '▼';
        line += '  (' + arrow + ' ' + afFmtDelta(d) + ' od minula)';
      }
    }
    lines.push(line);
  });

  var insights = afReadInsights();
  if (insights.length) {
    lines.push('');
    lines.push('POSTREHY:');
    insights.forEach(function (s) { lines.push('— ' + s); });
  }

  var text = lines.join('\n');

  // Tier 2 polish: if a Gemini key exists, ask it to rewrite warmly + grounded.
  if (afHasGeminiKey()) {
    try {
      var nicer = afGeminiBriefing(text);
      if (nicer) text = nicer + '\n\n(— automaticky zostavené z vašich dát)';
    } catch (e) { /* fall back silently to the deterministic briefing */ }
  }

  afSaveSnapshot(kpis);   // remember for next time's deltas
  return text;
}


/** Write/refresh the briefing as a NOTE on dashboard cell A1 (non-destructive). */
function afWriteBriefingNote(text) {
  if (text == null) text = afBuildBriefing(false);
  var sh = afDashboard();
  if (sh) sh.getRange('A1').setNote(text);
}


/* ---- snapshot store (Document Properties) -------------------------------- */

function afSaveSnapshot(kpis) {
  var map = {};
  kpis.forEach(function (k) { if (k.value != null) map[k.label] = k.value; });
  PropertiesService.getDocumentProperties()
    .setProperty(AF.PROP_SNAPSHOT, JSON.stringify(map));
}

function afLoadSnapshot() {
  var raw = PropertiesService.getDocumentProperties().getProperty(AF.PROP_SNAPSHOT);
  if (!raw) return null;
  try { return JSON.parse(raw); } catch (e) { return null; }
}

function afFmtDelta(d) {
  var abs = Math.abs(d);
  if (abs < 1) return (d > 0 ? '+' : '-') + abs.toFixed(2);          // ratios/%
  return (d > 0 ? '+' : '-') + Math.round(abs).toLocaleString('sk-SK');
}
