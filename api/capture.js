/* Leanta lead capture — Vercel serverless function.
   Receives {name,biz,pain,phone,budget} from the /v4 lead form.
   If Twilio env vars are configured it (a) SMS-notifies Samuel and
   (b) sends the visitor a confirmation SMS when they left a mobile.
   Without env vars it returns 503 so the page falls back to mailto —
   the form NEVER silently loses a lead.

   Env vars to set in Vercel (Settings → Environment Variables):
     TWILIO_ACCOUNT_SID  TWILIO_AUTH_TOKEN  TWILIO_FROM  (E.164, e.g. +3538...)
     CAPTURE_TO          Samuel's mobile, E.164
   GDPR: data is relayed to Twilio (processor) and not stored here; the
   visitor initiated contact (consent). Mention Twilio in the privacy page
   before flipping this on in production. */

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ ok: false });

  const { TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, CAPTURE_TO } = process.env;
  if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_FROM || !CAPTURE_TO) {
    return res.status(503).json({ ok: false, reason: "capture not configured" });
  }

  const { name = "", biz = "", pain = "", phone = "", budget = "" } = req.body || {};
  if (!name && !biz && !pain) return res.status(400).json({ ok: false });

  const clip = (s, n) => String(s).slice(0, n);
  const notify =
    `LEANTA lead: ${clip(name, 40) || "—"} · ${clip(biz, 60) || "—"} · ` +
    `start: ${clip(budget, 30)} · pain: ${clip(pain, 120) || "—"}` +
    (phone ? ` · mob: ${clip(phone, 20)}` : "");

  const send = (to, body) =>
    fetch(`https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json`, {
      method: "POST",
      headers: {
        Authorization: "Basic " + Buffer.from(`${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}`).toString("base64"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ From: TWILIO_FROM, To: to, Body: body }),
    });

  try {
    const jobs = [send(CAPTURE_TO, notify)];
    if (/^\+?[0-9 ()-]{7,20}$/.test(phone)) {
      jobs.push(send(phone.replace(/[ ()-]/g, ""),
        "Leanta here — got your note. A human replies within a working day, by message (no call unless you ask). " +
        "This is a one-off confirmation, you're not on any list."));
    }
    const results = await Promise.allSettled(jobs);
    const ok = results[0].status === "fulfilled" && results[0].value.ok;
    return res.status(ok ? 200 : 502).json({ ok });
  } catch {
    return res.status(502).json({ ok: false });
  }
}
