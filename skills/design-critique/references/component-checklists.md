# UI Component Review Checklists

Quick evaluation checklists for common UI components.

---

## 1. Buttons & Calls-to-Action (CTAs)
- [ ] **Visual Hierarchy**: One clear Primary button per view; secondary and tertiary actions use outline or ghost styles.
- [ ] **Label Clarity**: Action-oriented verb labels (e.g., "Save Changes", "Create Account") instead of generic "OK" or "Submit".
- [ ] **State Coverage**: Hover, Active/Pressed, Focus-Visible, Disabled, and Loading states visually defined.
- [ ] **Target Size**: Minimum 44x44px touch area on mobile; adequate padding (minimum 8-12px horizontal).
- [ ] **Placement**: Primary actions placed predictably (e.g., bottom-right of modals, top-right or sticky bottom on forms).

---

## 2. Forms & Data Input
- [ ] **Label Placement**: Labels placed above input fields for fast top-to-bottom eye scanning.
- [ ] **Input Constraints**: Use appropriate input types (`email`, `number`, `tel`) to trigger correct mobile keyboards.
- [ ] **Helper & Error Text**: Persistent helper text placed below inputs; inline error validation displays *after* field interaction, not before.
- [ ] **Required vs Optional**: Clearly mark optional fields (or required fields if most are optional).
- [ ] **Autofill & Password Managers**: Proper `name` and `autocomplete` attributes supported in HTML/React code.

---

## 3. Navigation (Header, Sidebar, Tabs)
- [ ] **Active Indicator**: Current page or tab is unambiguously highlighted (color, background, indicator line).
- [ ] **Limit Items**: Top-level navigation items capped at 5–7 choices to avoid cognitive overload.
- [ ] **Breadcrumbs & Back Navigation**: Deep hierarchical screens provide clear return paths.
- [ ] **Mobile Collapse**: Navigation degrades gracefully to a mobile drawer/hamburger or bottom tab bar on small screens.

---

## 4. Cards & Content Containers
- [ ] **Clickable Boundaries**: If the card is interactive, the entire card surface is clickable or contains a clear CTA link.
- [ ] **Content Padding**: Minimum 16px or 24px inner padding so text doesn't touch card borders.
- [ ] **Image Aspect Ratios**: Images within cards maintain consistent aspect ratios (e.g., 16:9, 4:3, 1:1) to prevent layout shifts.
- [ ] **Typography Hierarchy**: Distinct title, body, and meta-info styling inside each card.

---

## 5. Modals & Dialogs
- [ ] **Backdrop & Focus Trap**: Dark semi-transparent overlay locks background; keyboard focus trapped inside modal.
- [ ] **Dismissibility**: Clear "X" close icon top-right, Escape key closes modal, overlay click closes modal (unless destructive form).
- [ ] **Header & Footer**: Title clearly states action; footer contains primary and secondary action buttons aligned predictably.

---

## 6. Data Tables & Lists
- [ ] **Alignment**: Text left-aligned; numerical data right-aligned; status badges centered.
- [ ] **Header Distinction**: Table header row visually distinct (bold font, background shade, subtle bottom border).
- [ ] **Pagination or Virtual Scroll**: Data capped per page with clear page indicators or smooth infinite scrolling.
- [ ] **Empty States**: Helpful message, graphic/icon, and call-to-action when table contains zero records.
