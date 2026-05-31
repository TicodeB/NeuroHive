/**
 * ASSET-FORGE · Premium Pack — Google Sheets "Pro" edition
 * GeminiSidebar.gs — Tier 2 in-sheet AI ("💬 Spýtaj sa svojich dát").
 *
 * A "💬 ask your data" sidebar that calls Gemini with the OWNER'S OWN free API
 * key (stored per-file via the menu, never committed, never sent to us). The
 * model only ever sees (a) the pack's live KPIs and (b) the precomputed
 * insights — so answers stay grounded in the owner's real numbers and on the
 * trade's own vocabulary. It explains and summarises; it never takes an action
 * (no orders, no payments) — the trust line (agentic_tech_stack.md §2/§5).
 *
 * Honest constraints (agentic_tech_stack.md §5): a live AI cannot run inside an
 * offline .xlsx — this tier requires the Google Sheets edition + a free Gemini
 * key, and the free tier has usage limits that change. Frame AI as a bonus.
 */

/** Menu target — open the chat sidebar. */
function afOpenSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('Sidebar')
    .setTitle('💬 Spýtaj sa svojich dát');
  SpreadsheetApp.getUi().showSidebar(html);
}

function afHasGeminiKey() {
  return !!PropertiesService.getDocumentProperties().getProperty(AF.PROP_GEMINI);
}


/**
 * Called from Sidebar.html. Answers a free-text question grounded in the sheet.
 * Returns a plain string (Slovak by default — the pack's language).
 */
function afAskGemini(question) {
  if (!question || !question.trim()) return 'Napíšte otázku.';
  var system =
    'Si stručný biznis asistent pre majiteľa malej prevádzky. Odpovedaj po ' +
    'slovensky, vecne a krátko. Vychádzaj VÝHRADNE z priložených čísel a ' +
    'postrehov — nič si nevymýšľaj. Ak dáta na odpoveď nestačia, povedz to. ' +
    'Nenavrhuj nič nezvratné (žiadne objednávky ani platby), len vysvetli a ' +
    'odporuč ďalší krok.';
  return afGeminiCall(system, afBuildContext() + '\n\nOTÁZKA: ' + question);
}

/** Tier-2 polish for the deterministic briefing (called from Briefing.gs). */
function afGeminiBriefing(rawBriefing) {
  var system =
    'Prepíš nasledujúci strohý briefing do 3–4 priateľských viet po slovensky. ' +
    'Zachovaj všetky čísla presne, nič nepridávaj. Zvýrazni 1 vec, ktorá si ' +
    'zaslúži pozornosť dnes.';
  return afGeminiCall(system, rawBriefing);
}


/** Assemble the grounding context from the live dashboard. */
function afBuildContext() {
  var kpis = afReadKpis();
  var insights = afReadInsights();
  var lines = ['ŽIVÉ UKAZOVATELE (KPI):'];
  kpis.forEach(function (k) { lines.push('- ' + k.label + ': ' + (k.display || k.value)); });
  if (insights.length) {
    lines.push('', 'POSTREHY:');
    insights.forEach(function (s) { lines.push('- ' + s); });
  }
  return lines.join('\n');
}


/** Low-level Gemini REST call via UrlFetchApp. Returns text or throws/strings an error. */
function afGeminiCall(systemText, userText) {
  var key = PropertiesService.getDocumentProperties().getProperty(AF.PROP_GEMINI);
  if (!key) return '⚠️ Najprv nastavte Gemini API kľúč (menu ⚙️ ASSET-FORGE → 🔑).';

  var url = 'https://generativelanguage.googleapis.com/v1beta/models/' +
            encodeURIComponent(AF.GEMINI_MODEL) + ':generateContent?key=' +
            encodeURIComponent(key);
  var payload = {
    system_instruction: { parts: [{ text: systemText }] },
    contents: [{ role: 'user', parts: [{ text: userText }] }],
    generationConfig: { temperature: 0.2, maxOutputTokens: 512 }
  };
  var resp = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
  var code = resp.getResponseCode();
  var body = resp.getContentText();
  if (code !== 200) {
    if (code === 429) return '⚠️ Bezplatný limit Gemini je momentálne vyčerpaný. Skúste neskôr.';
    if (code === 400 || code === 403) return '⚠️ Kľúč je neplatný alebo bez prístupu. Skontrolujte ho v menu 🔑.';
    return '⚠️ Gemini chyba (' + code + ').';
  }
  try {
    var json = JSON.parse(body);
    var text = json.candidates &&
               json.candidates[0].content.parts.map(function (p) { return p.text; }).join('');
    return (text || '').trim() || '(prázdna odpoveď)';
  } catch (e) {
    return '⚠️ Nepodarilo sa prečítať odpoveď.';
  }
}
