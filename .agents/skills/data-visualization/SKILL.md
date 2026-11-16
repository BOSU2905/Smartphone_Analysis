---
name: data-visualization
description: >-
  Governs ethical, accessible, and responsive D3.js data visualizations, chart selection,
  axis integrity, tooltips, and statistical clarity. Use whenever designing or implementing
  interactive data graphics.
---

# Data Visualization Skill

This skill governs the selection, architecture, precision, and ethics of data visualizations in **"What Are We Really Paying For When We Buy a Smartphone?"**.

---

## 1. WHEN TO ACTIVATE

Activate this skill whenever:
- Designing or implementing D3.js data graphics (scatter plots, box plots, histograms, bar charts, efficiency frontiers).
- Configuring mathematical scales (linear, logarithmic, ordinal, quantile).
- Designing interactive hover states, crosshairs, and rich telemetry tooltips.
- Integrating real-time currency recalculations (`USD`, `INR`, `IDR`) into existing chart axes.
- Ensuring responsive chart resizing and accessible screen-reader table fallbacks.

---

## 2. ETHICAL VISUALIZATION PRINCIPLES

1. **Analytical Honesty:** Charts must communicate empirical patterns without distortion. Never manipulate axes to artificially exaggerate minor differences or flatten significant disparities.
2. **Zero Chart Junk:** Eliminate gratuitous 3D bars, decorative shadows, decorative radial gauges, or meaningless visual clutter. Every stroke, tick mark, and coordinate must represent data.
3. **Responsive Geometry:** Charts must adapt gracefully from ultra-wide monitors (`1440px+`) down to mobile viewports (`375px`) using SVG `viewBox` scaling or dynamic `ResizeObserver` loops.
4. **Accessible Pairing:** Every visual chart must be paired with an accessible summary and a hidden or togglable HTML data table for screen-reader users.

---

## 3. MANDATORY VISUALIZATION RULES & PROHIBITIONS

### Prohibited Chart Practices
- **NO Truncated Zero Baselines on Bar Charts:** Bar charts encode value via length; their value axes must strictly start at zero. Truncating the baseline to make a 5% difference look like a 500% difference is an ethical violation.
- **NO Gratuitous 3D Charts:** Never render 2D data (such as bar charts, scatter plots, or pie charts) in pseudo-3D. (Selective 3D is permitted *only* for true 3-variable spatial parameter surfaces).
- **NO Pie Charts with >4 Slices:** Pie and donut charts are mathematically inefficient for human angle perception. Use horizontal ranked bar charts instead.
- **NO Unlabeled Dual Axes:** Dual-axis charts must feature color-coded or clearly separated axis labels to avoid confusing readers regarding which curve maps to which scale.

### Mandatory Standards
- **Currency Responsiveness:** When the global currency toggle changes (`USD` -> `INR` -> `IDR`), D3 axis formatters (`d3.format`) and tick distributions must update smoothly within $\le 400\text{ms}$ without tearing or redrawing the entire SVG canvas.
- **Rich Telemetry Tooltips:** Hovering any data point must present:
  - Phone Model & Brand
  - Exact Retail Price in Active Currency
  - Core Specifications (SoC, RAM, Storage, Battery, Charging Wattage)
  - MySmartPrice Expert Rating (where available)
  - Excerpt from editorial review
- **Color Differentiation:** Categorical colors across brands or chipsets must be distinguishable by individuals with deuteranopia and protanopia. Verify with colorblindness simulation filters.

---

## 4. APPROVED CHART TAXONOMY FOR THIS PROJECT

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHART TAXONOMY                                    │
├────────────────────┬────────────────────┬───────────────────────────────────┤
│ Analytical Question│ Approved Chart     │ D3 Modules / Techniques           │
├────────────────────┼────────────────────┼───────────────────────────────────┤
│ Price vs Spec Value│ Scatter Plot +     │ d3-scale (log/linear), d3-zoom,   │
│ (Pareto Frontier)  │ Efficiency Curve   │ d3-selection, voronoi hover       │
├────────────────────┼────────────────────┼───────────────────────────────────┤
│ Brand Price Floors │ Horizontal Box Plot│ d3-scaleBand, IQR calculations,   │
│ & Distribution     │ / Violin Plot      │ median points, outlier markers    │
├────────────────────┼────────────────────┼───────────────────────────────────┤
│ SoC Distribution   │ Diverging Ranked   │ d3-scaleBand, d3-axis,            │
│ across Price Bands │ Stacked Bar Chart  │ categorical color mapping         │
├────────────────────┼────────────────────┼───────────────────────────────────┤
│ Memory Markup      │ Step Curve / Slope │ d3-shape (curveStepAfter),        │
│ (Cost per GB)      │ Comparison Chart   │ dual-line comparison              │
├────────────────────┼────────────────────┼───────────────────────────────────┤
│ Total Cost of      │ Multi-Year Area /  │ d3-area, d3-line, cumulative      │
│ Ownership (TCO)    │ Amortization Line  │ depreciation stacking             │
└────────────────────┴────────────────────┴───────────────────────────────────┘
```

---

## 5. DATA VISUALIZATION WORKFLOW

```
[INGEST SANITIZED DATA]
       │
       ▼
[DEFINE MATHEMATICAL SCALES] ──── (Linear, Logarithmic, Band; handle zero baselines)
       │
       ▼
[CONSTRUCT RESPONSIVE SVG] ────── (Bind ResizeObserver; set up viewBox coordinates)
       │
       ▼
[RENDER DATA GEOMETRY] ────────── (Bars, dots, paths with d3 transitions)
       │
       ▼
[ATTACH INTERACTIVE TELEMETRY] ── (Voronoi overlays, hover focus rings, rich tooltips)
       │
       ▼
[GENERATE ACCESSIBLE TABLE] ───── (Build accompanying HTML table for WCAG AA)
```

---

## 6. QUALITY AUDIT CHECKLIST

Before approving any chart component, verify:
- [ ] Do bar charts strictly maintain a zero-baseline?
- [ ] Are axes clearly labeled with units (e.g., *Price (USD $)*, *RAM (GB)*)?
- [ ] Does the chart update smoothly when the global currency toggle changes?
- [ ] Does hovering a data point display a rich telemetry tooltip?
- [ ] Are chart colors legible for color-vision-deficient users?
- [ ] Is an accessible tabular alternative provided for screen readers?
- [ ] Does the visualization scale cleanly on mobile viewports without horizontal clipping?

---

## 7. PROJECT CONTEXT & EXPLICIT LIMITATIONS

- **Context:** Visualizations are the empirical backbone of the website.
- **Limitations:** Do not burden the client with heavy SVG DOM trees exceeding 3,000 active nodes; use Canvas rendering or D3 virtualized rendering if plotting the entire catalog simultaneously.
