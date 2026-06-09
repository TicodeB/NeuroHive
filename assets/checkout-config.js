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
  contactEmail: "samuel.vyhnanek+leanta@gmail.com",

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
    }
  }
};
