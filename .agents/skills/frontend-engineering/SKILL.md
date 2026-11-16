---
name: frontend-engineering
description: >-
  Governs Vite, React, TypeScript architecture, component hierarchy, state management,
  bundle size, and build pipelines. Use whenever scaffolding frontend projects, writing
  React components, or configuring web tooling.
---

# Frontend Engineering Skill

This skill governs the software architecture, TypeScript type safety, build pipelines, and performance optimization for **"What Are We Really Paying For When We Buy a Smartphone?"**.

---

## 1. WHEN TO ACTIVATE

Activate this skill whenever:
- Scaffolding or configuring the Vite, React, and TypeScript web project.
- Defining TypeScript data models and interfaces for the smartphone dataset.
- Implementing React components, custom hooks, and context providers.
- Integrating Three.js / React Three Fiber and D3.js into React component lifecycles.
- Managing client-side routing between the Homepage (`/`) and the Catalog (`/explore`).
- Profiling bundle sizes, code splitting, and production build hygiene.

---

## 2. APPROVED TECHNICAL STACK & DIRECTORY CONVENTIONS

```
web/
├── index.html                   # HTML entry point with Google Fonts preconnect
├── package.json                 # Pinned dependencies (Vite, React 18, Three, D3)
├── tsconfig.json                # TypeScript strict configuration
├── vite.config.ts               # Vite bundler config with chunk-splitting rules
└── src/
    ├── main.tsx                 # React application mounting
    ├── App.tsx                  # Top-level routing shell (/ and /explore)
    ├── types/                   # Strict TypeScript domain interfaces
    │   ├── smartphone.ts        # Model entity, specs, ratings, price types
    │   └── currency.ts          # Currency union type ('USD' | 'INR' | 'IDR')
    ├── context/
    │   └── CurrencyContext.tsx  # Global currency state provider & conversion math
    ├── hooks/
    │   ├── useScrollProgress.ts # Normalized scroll progress tracker
    │   ├── useReducedMotion.ts  # Media query listener for accessibility
    │   └── useFilteredCatalog.ts# Client-side filtering & sorting engine
    ├── components/
    │   ├── layout/              # Navigation, Footer, Chapter framing
    │   ├── hero3d/              # React Three Fiber canvas, meshes, controls
    │   ├── charts/              # D3.js visualization components
    │   └── telemetry/           # Spec cards, drawer panels, metric chips
    ├── views/
    │   ├── HomeResearchView.tsx # Main chapter-based research journey
    │   └── ExploreCatalogView.tsx# Independent /explore catalog & filter tool
    └── data/
        ├── smartphones_cleaned.json # Pre-sanitized 2,256 model records
        └── market_summary.json  # Pre-aggregated market statistics
```

---

## 3. STRICT CODING CONVENTIONS & RULES

1. **Strict TypeScript (Zero `any`):** Every entity in the dataset must conform to a strongly typed interface:
   ```typescript
   export type Currency = 'USD' | 'INR' | 'IDR';

   export interface SmartphoneRecord {
     id: string;
     model_name: string;
     brand: string;
     price_inr: number;
     price_usd: number;
     price_idr: number;
     ram_gb: number;
     storage_gb: number;
     battery_mah: number;
     charging_watts: number | null;
     display_type: 'AMOLED' | 'OLED' | 'IPS' | 'LCD' | 'TFT' | 'Other';
     refresh_rate_hz: number | null;
     screen_size_inches: number | null;
     chipset_vendor: 'Snapdragon' | 'MediaTek' | 'Apple' | 'Exynos' | 'Unisoc' | 'Tensor' | 'Other';
     chipset_model: string;
     os: 'Android' | 'iOS' | 'Other';
     expert_rating: number | null; // 0.0 to 10.0 scale
     user_rating_score: number | null; // 0.0 to 5.0 scale
     user_rating_count: number | null;
     review_snippet: string | null;
     review_url: string | null;
   }
   ```
2. **Global Currency Context:** Currency must be managed via a lightweight React Context (`CurrencyContext`) exposing:
   ```typescript
   interface CurrencyContextType {
     currency: Currency;
     setCurrency: (c: Currency) => void;
     formatPrice: (priceInr: number) => string;
     convertPrice: (priceInr: number) => number;
   }
   ```
   Updating currency must immediately propagate to all components without re-mounting data trees.
3. **Defensive Data Handling:** Legacy records may have null values for charging wattage, refresh rate, or ratings. Components must never crash on null attributes; always provide sensible fallbacks (e.g., render `"N/A"` or omit optional badge).
4. **Lazy Loading Heavy Modules:** The 3D WebGL Hero and D3 chart engines must be code-split using `React.lazy()` and `Suspense`:
   ```typescript
   const HeroTeardownCanvas = React.lazy(() => import('./components/hero3d/HeroTeardownCanvas'));
   ```
5. **Zero Memory Leaks:** WebGL geometries and textures in Three.js must be explicitly disposed of in `useEffect` cleanup handlers when components unmount.

---

## 4. BUNDLE SIZE & BUILD TARGETS

- **Entry Chunk (JS):** $\le 250\text{ KB}$ gzipped.
- **Three.js Chunk:** Code-split into a separate vendor chunk, loaded on-demand.
- **D3 Chunk:** Only import modular sub-packages (`d3-scale`, `d3-axis`, `d3-selection`, `d3-shape`); never import the monolithic `d3` package.
- **Production Build:** `npm run build` must produce static HTML, CSS, and JS artifacts requiring zero backend Node.js runtime.

---

## 5. QUALITY AUDIT CHECKLIST

Before approving any frontend PR or component, verify:
- [ ] Does `npm run build` compile cleanly with zero TypeScript errors?
- [ ] Are all dataset records typed without using `any`?
- [ ] Does the currency toggle instantaneously update all visible prices?
- [ ] Are Three.js canvas components lazy-loaded with an appropriate fallback?
- [ ] Do Three.js components dispose of geometries and materials on unmount?
- [ ] Is the initial entry bundle kept under 250 KB gzipped?
- [ ] Is the application deployable as a static build to any static CDN?

---

## 6. PROJECT CONTEXT & EXPLICIT LIMITATIONS

- **Context:** The frontend is an editorial engine designed for longevity, speed, and zero operational maintenance.
- **Limitations:** Do not introduce heavy state-management libraries (Redux, MobX); native React Context and custom hooks are completely sufficient.
