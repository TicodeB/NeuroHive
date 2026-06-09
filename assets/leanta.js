/* Leanta site behaviour: buy buttons + quiz scoring. No tracking, no cookies,
   no external requests — everything runs in the visitor's browser (GDPR-clean). */

(function () {
  "use strict";

  var cfg = window.LEANTA || { contactEmail: "", products: {} };

  /* ---- Buy buttons -------------------------------------------------------
     Any element: <span data-buy="p1" data-style="primary"></span>
     Renders "Buy now" (checkout URL configured) or "Reserve by email". */
  function renderBuyButtons() {
    document.querySelectorAll("[data-buy]").forEach(function (slot) {
      var id = slot.getAttribute("data-buy");
      var p = cfg.products[id];
      if (!p) return;

      var a = document.createElement("a");
      a.className = "btn " + (slot.getAttribute("data-style") === "outline" ? "" : "btn-primary");
      if (slot.hasAttribute("data-block")) a.classList.add("btn-block");

      if (p.checkoutUrl) {
        a.href = p.checkoutUrl;
        a.textContent = "Buy now — " + p.price;
        a.rel = "noopener";
      } else {
        var subject = "Order: " + p.name + " (" + p.price + ")";
        var body = [
          "Hi Leanta,",
          "",
          "I'd like to order: " + p.name + " — " + p.price + ".",
          "",
          "Please send me the payment link and the file.",
          "",
          "Name / business: ",
          "Country (for VAT): "
        ].join("\n");
        a.href = "mailto:" + cfg.contactEmail +
          "?subject=" + encodeURIComponent(subject) +
          "&body=" + encodeURIComponent(body);
        a.textContent = "Reserve by email — " + p.price;
        var note = document.createElement("div");
        note.className = "fineprint";
        note.style.marginTop = ".45rem";
        note.textContent = "Launch week: orders are confirmed by email with a secure payment link, then your file is delivered the same day.";
        slot.appendChild(note);
      }
      slot.insertBefore(a, slot.firstChild);
    });
  }

  /* ---- Readiness quiz ---------------------------------------------------
     Yes = 100, Partly = 50, No = 0. Average across answered questions.
     RAG verdict mirrors the P13 workbook: green >=85, amber 60-84, red <60. */
  function initQuiz() {
    var form = document.getElementById("quiz-form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var qs = form.querySelectorAll(".quiz-q");
      var sum = 0, answered = 0;
      qs.forEach(function (q) {
        var sel = q.querySelector("input:checked");
        if (sel) { sum += Number(sel.value); answered++; }
      });

      var result = document.getElementById("quiz-result");
      var scoreEl = document.getElementById("quiz-score");
      var verdictEl = document.getElementById("quiz-verdict");
      var detailEl = document.getElementById("quiz-detail");

      if (!answered) {
        result.className = "amber";
        scoreEl.textContent = "—";
        verdictEl.textContent = "Answer at least one question to get your verdict.";
        detailEl.textContent = "";
        result.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }

      var pct = Math.round(sum / answered);
      scoreEl.textContent = pct + "%";

      if (pct >= 85) {
        result.className = "green";
        verdictEl.textContent = "🟢 Likely to pass — keep your records current.";
        detailEl.textContent = "Strong base. The full 26-clause gap analysis + 20-question mock audit will confirm it and catch the gaps a 10-question check can't.";
      } else if (pct >= 60) {
        result.className = "amber";
        verdictEl.textContent = "🟠 Borderline — an inspector would find gaps.";
        detailEl.textContent = "You'd likely get follow-up actions rather than a clean pass. The Readiness Check pinpoints and prioritises every gap so you fix the right things first.";
      } else {
        result.className = "red";
        verdictEl.textContent = "🔴 At risk — significant gaps in your records.";
        detailEl.textContent = "Missing statutory records are the fastest route to enforcement. Start with the Compliance Pack — it contains every record an inspector asks for.";
      }
      result.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderBuyButtons();
    initQuiz();
  });
})();
