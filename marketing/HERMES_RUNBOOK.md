# HERMES RUNBOOK — message-channel operations + 9 industry reply templates
Plan §15 build. Hermes (or Samuel manually) replies to quiz-result and enquiry
messages. Channels: WhatsApp Business app NOW · sms: links NOW · WhatsApp API
(Twilio/360dialog) only at volume · Telegram = internal ops only · no iMessage.

---

## OPERATOR GUARDRAILS (binding)

1. **Customer-initiated only.** Reply only in threads the customer opened
   (quiz CTA, site button, inbound email/WA/SMS). Never cold-message.
2. **Approved templates only.** Use the 9 templates below + the universal
   blocks. Free-text edits limited to the [bracketed] personalisation slots.
3. **Honest bot disclosure** when any automation drafts or sends:
   > "This reply was drafted with Leanta's assistant — Samuel reads every thread."
4. **Escalate to Samuel (no auto-reply)** when a thread (a) passes 3
   back-and-forths, (b) mentions money owed/refunds/legal/complaint/GDPR
   request, or (c) the customer asks for a human. Mark thread ⚑.
5. **No promises** on grant approval (LEO decides), inspection outcomes, or
   delivery dates Samuel hasn't confirmed.
6. **GDPR:** their message = consent to reply on that channel, on that topic.
   No adding to lists. Delete thread on request, confirm deletion.
7. **Quiet hours:** no outbound 21:00–08:00 IE time; queue for morning.

## MESSAGE SKELETON (all templates)

```
[GREETING + their score/context] → [2–3 action items for THEIR sector] →
[one product or pathway fit] → [no-pressure close + human offer]
```

Keep replies under ~120 words for WhatsApp/SMS. Email may run longer.

---

## THE 9 INDUSTRY ACTION-PLAN TEMPLATES
Trigger: quiz CTA messages arrive prefilled as
`"Hi Leanta — [industry], scored [X/10] on the readiness check"`.

### 1 · CAFÉ
> Hi [name] — thanks for running the check ([X]/10 for your café). The three
> things inspectors flag first in cafés: 1) allergen matrix older than the
> menu, 2) gaps in fridge/freezer temp logs, 3) no cleaning sign-off sheet.
> Start with the temp log — it's the fastest fix and the most-checked record.
> Our Café/Restaurant pack (€34) has all three pre-built so each takes
> seconds a day. Or reply AUDIT and we'll talk about the €200 on-site
> pathway. No rush, no calls unless you ask. — Leanta

### 2 · RESTAURANT
> Hi [name] — [X]/10 for the restaurant. Priority order for you: 1) HACCP
> plan matches what the kitchen actually does now (menu drift is the #1
> finding), 2) supplier traceability one-line log, 3) training matrix with
> due dates. The Operations & GP pack (€49) adds GP% and wastage tiles so
> the same workbook that passes the inspection also tells you Monday's
> margin. Reply AUDIT for the €200 on-site pathway, or just ask anything
> here. — Leanta

### 3 · PUB
> Hi [name] — [X]/10 for the pub. Pubs get caught on: 1) cellar + fridge
> temps unlogged, 2) fire register out of date (the one non-food record
> always checked), 3) if you serve food at all — even toasties — a HACCP-lite
> plan is required. Start with the fire register this week. Compliance Pack
> €34 covers all three. Food menu growing? Reply AUDIT and we'll look at the
> €200 pathway together. — Leanta

### 4 · B&B / HOTEL
> Hi [name] — [X]/10 for the property. Your top three: 1) breakfast HACCP +
> allergen cards (guests ask, inspectors check), 2) fire safety register with
> weekly walk-through line, 3) one-page room-status/cleaning sheet the whole
> team initials. The Hospitality Pro Bundle (€69) is built exactly for this
> mix — rooms + food in one workbook. Grant-curious? The €200 pathway often
> suits accommodation businesses (LEO Digital schemes). Reply AUDIT for
> details. — Leanta

### 5 · SHOP
> Hi [name] — [X]/10 for the shop. Retail quick wins: 1) till reconciliation
> sheet that flags variances the same day (the midnight-retype killer),
> 2) date-rotation log if you sell any fresh/chilled, 3) a simple wastage
> count — two lines a day shows where the margin leaks. Single tools start
> at €15; the Operations pack (€49) does the lot with a dashboard. Want us
> to look at your setup on-site? Reply AUDIT — €200 pathway. — Leanta

### 6 · PRODUCER
> Hi [name] — [X]/10 for the production side. Producers live or die on:
> 1) batch traceability (one line per batch, both directions — your buyers
> will audit this), 2) HACCP with CCP monitoring records, 3) label/allergen
> declarations matching the current recipe sheet. These are exactly the
> records a TÜV-style certifier checks. The Compliance Pack (€34) has the
> spine; if you're heading for BRCGS/ISO, reply AUDIT — that's a €200
> pathway conversation with grant support behind it. — Leanta

### 7 · TRADES
> Hi [name] — [X]/10 for the trade. The three that bite: 1) quote→invoice
> tracking (unbilled jobs are the silent leak — most trades find 1–2 forgotten
> jobs the first week), 2) safety statement current and signed, 3) van-stock/
> materials log so jobs get costed right. The quote-to-invoice tool is €15
> on its own. If admin is eating your evenings, reply AUDIT — the €200
> on-site rebuild is built for exactly this. — Leanta

### 8 · TRANSPORT
> Hi [name] — [X]/10 for the transport side. Priorities: 1) driver hours/
> tacho check sheet (the record that's always requested), 2) vehicle defect
> walk-around log with sign-off, 3) job/delivery costing per run so the
> diesel price stops being a guess. Start with the defect log — it's a legal
> shield. Single tools €15, Operations pack €49. Fleet bigger than 3? Reply
> AUDIT for the €200 on-site pathway. — Leanta

### 9 · OTHER
> Hi [name] — thanks for running the check ([X]/10). Whatever the sector,
> the same three hold: 1) the record an inspector/auditor asks for most in
> your field, kept where the work happens, 2) one money number you check
> weekly (margin, labour or cash), 3) one sheet the whole team actually
> initials. Tell me in one line what your business does and what ate last
> week — I'll point you at the exact tool (€15–69) or the €200 on-site
> pathway. A human reads this thread. — Leanta

---

## UNIVERSAL BLOCKS

**Pre-order reply (checkout not yet live):**
> Thanks [name]! Checkout goes live this week — reply YES and you'll get the
> payment link the moment it's up, nothing charged till then.

**Grant question:**
> Honest version: €200 mobilises the audit + a complete LEO application pack.
> Approved → scheme carries its share, your €200 is credited. Not approved →
> you keep all the work and decide freely. Approval is the LEO's call, never
> ours.

**"Are you a bot?":**
> Partly! Drafts come from Leanta's assistant; Samuel reads and owns every
> thread. Want him directly? Say the word.

**Refund/complaint (ESCALATE — holding line only):**
> Sorry it's not right. Samuel picks this up personally — you'll hear from
> him within one working day. Nothing more needed from you for now.

---

## LOGGING
One line per thread per day in the ops sheet: date · channel · industry ·
template used · stage (new/replied/escalated/closed) · next action.
