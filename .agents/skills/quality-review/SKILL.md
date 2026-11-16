---
name: quality-review
description: >-
  Governs comprehensive quality assurance, accessibility audits (WCAG 2.1 AA), responsive
  testing, performance profiling, and cross-browser validation. Use whenever reviewing code,
  verifying phase milestones, or conducting pre-release audits.
---

# Quality Review Skill

This skill governs the systematic quality assurance, accessibility compliance, performance profiling, and cross-platform verification for **"What Are We Really Paying For When We Buy a Smartphone?"**.

---

## 1. WHEN TO ACTIVATE

Activate this skill whenever:
- Concluding an implementation phase or reviewing a major component PR.
- Performing accessibility audits against WCAG 2.1 AA standards.
- Profiling performance, Core Web Vitals (LCP, CLS, INP), and frame rates.
- Conducting cross-browser rendering checks (Chrome, Safari, Firefox, Edge).
- Validating responsive reflow across mobile (`375px`), tablet (`768px`), and desktop (`1440px+`).
- Verifying data integrity and mathematical consistency before release.

---

## 2. AUDIT DIMENSIONS & ACCEPTANCE CRITERIA

### Dimension 1: Data Integrity & Provenance
- [ ] Are all active records traced back to the 2,256 de-duplicated unique rows?
- [ ] Are 1TB devices verified to display 1024GB (not 1GB)?
- [ ] Are legacy MB RAM devices properly represented as fractional GB?
- [ ] Are all converted prices explicitly labeled as converted Indian retail prices?
- [ ] Do currency conversions match the approved August 2024 reference rates ($1\text{ USD} = 83.90\text{ INR}$, $1\text{ USD} = 15,600\text{ IDR}$)?

### Dimension 2: Accessibility (WCAG 2.1 AA)
- [ ] Does text-to-background contrast meet or exceed 4.5:1 for body copy and 3:1 for large text?
- [ ] Can the entire application be operated without a mouse using `Tab`, `Shift+Tab`, `Enter`, and `Escape`?
- [ ] Are focus rings prominently visible (`2px solid #E63946`) on all interactive controls?
- [ ] Do complex D3 charts provide accessible tabular alternatives for screen-reader users?
- [ ] Does activating `prefers-reduced-motion` immediately replace the 3D scroll disassembly with the 2D tabbed schematic?

### Dimension 3: Visual & Responsive Layout QA
- [ ] Does the visual presentation strictly adhere to the Design Constitution (Dark Technical with Industrial Crimson accent)?
- [ ] Is excessive empty whitespace avoided in favor of structured technical density?
- [ ] Does typography pair Manrope (Display), IBM Plex Sans (Body), and IBM Plex Mono (Technical)?
- [ ] Is horizontal page scrolling strictly avoided on mobile viewports (`375px` to `430px`)?
- [ ] Do tables and filters on `/explore` collapse into an ergonomic mobile layout?

### Dimension 4: Performance & Core Web Vitals
- [ ] Largest Contentful Paint (LCP) $\le 2.5\text{s}$ on standard broadband.
- [ ] Cumulative Layout Shift (CLS) $\le 0.05$ during font and 3D asset loading.
- [ ] Interaction to Next Paint (INP) $\le 100\text{ms}$ during currency toggle and catalog filtering.
- [ ] 3D WebGL Hero maintains a steady 60 FPS on modern desktop GPUs.
- [ ] JavaScript initial entry chunk $\le 250\text{ KB}$ gzipped.
- [ ] 3D Draco-compressed GLB asset $\le 3.5\text{ MB}$.

### Dimension 5: Functional Verification
- [ ] Does changing the currency switcher (`USD`, `INR`, `IDR`) instantaneously update all prices across both `/` and `/explore`?
- [ ] Does the 3D Hero disassemble smoothly from 0% to 100% scroll progress?
- [ ] Does the manual scrubber slider control 3D disassembly independently of scrolling?
- [ ] Does the "Reassemble" button smoothly return the 3D model to 0% progress?
- [ ] Does the "Skip Teardown" button immediately scroll past the 3D section?
- [ ] In `/explore`, do combined filters (e.g., Brand + Price + RAM) return the exact matching subset without errors?
- [ ] Are console logs clean, with zero unhandled exceptions or React key warnings?

---

## 3. AUDIT TOOLS & MCP INTEGRATION

- **Chrome DevTools MCP & `a11y-debugging`:** Run automated accessibility audits and inspect accessibility trees.
- **`debug-optimize-lcp`:** Identify LCP candidate elements and verify fetch priority.
- **`memory-leak-debugging`:** Verify that Three.js textures and geometries are disposed of when navigating between `/` and `/explore`.
- **Lighthouse CLI / DevTools:** Measure performance and accessibility scores before final release sign-off.

---

## 4. REVIEW WORKFLOW

```
[STATIC CODE AUDIT] ──────── (TypeScript compile, ESLint clean, zero `any`)
       │
       ▼
[DATA INTEGRITY AUDIT] ───── (Unit tests on price conversion, storage, RAM)
       │
       ▼
[ACCESSIBILITY AUDIT] ────── (Keyboard traversal, WCAG contrast, reduced motion)
       │
       ▼
[RESPONSIVE LAYOUT AUDIT] ── (Mobile 375px, Tablet 768px, Desktop 1440px)
       │
       ▼
[PERFORMANCE PROFILING] ──── (Lighthouse, Core Web Vitals, WebGL FPS)
       │
       ▼
[PHASE COMPLETION SIGN-OFF] ─ (Submit verified completion report)
```

---

## 5. PROJECT CONTEXT & EXPLICIT LIMITATIONS

- **Context:** Quality review protects the credibility and technical excellence of the final product.
- **Limitations:** Never bypass a failing test or accessibility violation to accelerate delivery.
