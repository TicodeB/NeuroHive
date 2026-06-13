/* Leanta checkout configuration — THE ONLY FILE TO EDIT AT GO-LIVE.
 *
 * Paste each product's hosted-checkout URL (Lemon Squeezy "Buy" link,
 * Stripe Payment Link, or Gumroad link) into `checkoutUrl`.
 *  - URL present  -> the site renders a direct "Buy now" button.
 *  - URL empty "" -> the site renders a "Reserve by email" pre-order button
 *                    (mailto with a prefilled order subject) so orders can be
 *                    taken and fulfilled manually from day one.
 *
 * Platform strategy (MONETIZATION_BRIEF.md §1): Lemon Squeezy primary
 * (Merchant of Record — handles EU VAT), Gumroad fallback, Etsy discovery.
 */
window.LEANTA = {
  contactEmail: "hello@leanta.ie",

  /* Texting channel. Fill with the business mobile in international format
   * (e.g. "+353871234567") to activate every "Text us" button site-wide.
   * Empty "" -> the buttons fall back to email so nothing dead-ends. */
  contactPhone: "",

  /* Lea's 3D pet (story page /v4/). Remix the Omma community pet
   * (https://omma.build/community/i6ttegp2zyw1) in your own Omma/Spline
   * account, publish it, and paste the public scene/embed URL here.
   * Empty "" -> the built-in animated SVG pet is used instead. */
  ommaPetUrl: "",

  products: {
    p13: {
      name: "Compliance Readiness Check (Gap-Analysis & Mock-Audit)",
      price: "€29",
      checkoutUrl: ""
    },
    p1: {
      name: "Café & Restaurant Compliance Pack",
      price: "€34",
      checkoutUrl: ""
    },
    p2: {
      name: "Hospitality Operations & GP Bundle",
      price: "€49",
      checkoutUrl: ""
    },
    bundle: {
      name: "Hospitality Pro Bundle (Compliance + Operations)",
      price: "€69",
      checkoutUrl: ""
    },
    p3: {
      name: "H&S Risk Assessment & Safety Statement Builder",
      price: "€19",
      checkoutUrl: ""
    },
    p4: {
      name: "Cashflow & P&L Tracker",
      price: "€24",
      checkoutUrl: ""
    },
    p5: {
      name: "Fire Safety Register & Checks Log",
      price: "€15",
      checkoutUrl: ""
    },
    p12: {
      name: "Staff Training & Induction Matrix",
      price: "€15",
      checkoutUrl: ""
    }
  }
};
