# Automated Fix for AUT-5

**AI Diagnosis & Recommended Code Change:**

**Cause of the Bug:**
An invisible overlay `<div>` rendered right next to the "Pay Now" link button has `z-50` and `pointer-events-auto` (`<div class="absolute inset-0 z-50 pointer-events-auto rounded-full" aria-hidden="true"></div>`), which places it above the button (`z-40`) and intercepts all mouse pointer events.

**How to Fix It:**
Change `pointer-events-auto` to `pointer-events-none` on the overlay `div` inside `Hero.tsx` so clicks pass through directly to the underlying button link, or remove the overlay if it is unused.