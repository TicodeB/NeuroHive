/**
 * ASSET-FORGE · Premium Pack — Google Sheets "Pro" edition
 * Menu.gs — the on-open menu that wires every tier together.
 *
 * Runs automatically when the owner opens the sheet (simple trigger onOpen).
 * Adds a single "⚙️ ASSET-FORGE" menu so a non-technical owner never has to
 * touch the code editor again after the one-time paste-in.
 */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('⚙️ ASSET-FORGE')
    .addItem('📋 Dnešný briefing (teraz)', 'afRunBriefingNow')
    .addItem('🗒️ Zapísať dnešok do denníka', 'afJournalNow')
    .addSeparator()
    .addItem('▶️ Zapnúť automatiku (denná + týždenná)', 'afInstallTriggers')
    .addItem('⏹️ Vypnúť automatiku', 'afRemoveTriggers')
    .addSeparator()
    .addItem('💬 Spýtaj sa svojich dát (AI)', 'afOpenSidebar')
    .addItem('🔑 Nastaviť Gemini API kľúč', 'afSetGeminiKey')
    .addToUi();
}


/**
 * Tier 1 — install time-driven triggers (free Apps Script "cron"):
 *   · nightly  ~23:00 → afNightly  (journal snapshot + refresh briefing note)
 *   · Monday   ~07:00 → afWeekly   (weekly briefing; e-mails if EMAIL_TO set)
 * Idempotent: clears our own triggers first so re-running never duplicates.
 */
function afInstallTriggers() {
  afRemoveTriggers();
  var ss = SpreadsheetApp.getActive();
  ScriptApp.newTrigger('afNightly').timeBased().everyDays(1).atHour(23).create();
  ScriptApp.newTrigger('afWeekly').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(7).create();
  SpreadsheetApp.getUi().alert(
    'Automatika zapnutá ✅',
    'Každú noc sa zapíše snímka do denníka a obnoví sa briefing.\n' +
    'Každý pondelok ráno sa pripraví týždenný súhrn' +
    (AF.EMAIL_TO ? ' a pošle sa na ' + AF.EMAIL_TO + '.' : ' (e-mail je vypnutý — pozri Config.gs).'),
    SpreadsheetApp.getUi().ButtonSet.OK);
}

function afRemoveTriggers() {
  var ours = { afNightly: 1, afWeekly: 1 };
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (ours[t.getHandlerFunction()]) ScriptApp.deleteTrigger(t);
  });
}


/** Trigger target — nightly chores. */
function afNightly() {
  afJournalAppend();          // append-only history row
  afWriteBriefingNote();      // refresh the "today" note on the dashboard
}

/** Trigger target — Monday morning weekly summary. */
function afWeekly() {
  var text = afBuildBriefing(true);
  afWriteBriefingNote(text);
  if (AF.EMAIL_TO) {
    MailApp.sendEmail(AF.EMAIL_TO,
      'Týždenný briefing — ' + SpreadsheetApp.getActive().getName(), text);
  }
}


/** Menu target — prompt for and store the owner's OWN free Gemini key. */
function afSetGeminiKey() {
  var ui = SpreadsheetApp.getUi();
  var resp = ui.prompt(
    'Gemini API kľúč',
    'Vložte svoj VLASTNÝ bezplatný kľúč z aistudio.google.com/apikey.\n' +
    'Uloží sa len do tohto súboru (Document Properties) — nikam sa neodosiela.',
    ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  var key = resp.getResponseText().trim();
  if (!key) { ui.alert('Kľúč nebol zadaný.'); return; }
  PropertiesService.getDocumentProperties().setProperty(AF.PROP_GEMINI, key);
  ui.alert('Hotovo ✅', 'Kľúč uložený. Otvorte „💬 Spýtaj sa svojich dát (AI)".', ui.ButtonSet.OK);
}
