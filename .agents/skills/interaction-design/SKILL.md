---
name: interaction-design
description: >-
  Governs interactive user experiences, scroll mechanics, 3D disassembly choreography,
  micro-interactions, keyboard accessibility, and reduced-motion states. Use whenever designing
  or coding interactive behaviors, 3D controls, or scroll transitions.
---

# Interaction Design Skill

This skill governs the choreography, physics, responsiveness, and accessibility of user interactions in **"What Are We Really Paying For When We Buy a Smartphone?"**.

---

## 1. WHEN TO ACTIVATE

Activate this skill whenever:
- Designing or implementing the 3D Hero scroll-driven component disassembly.
- Implementing the manual scrubber, reassemble button, or skip button.
- Binding mouse, pointer, or touch events to 3D meshes (raycasting, hover highlights, selection).
- Designing interactive micro-interactions (telemetry cards, drawer panels, filter dropdowns).
- Implementing keyboard navigation (`Tab`, `Enter`, `Escape`, arrow keys) and focus states.
- Handling `prefers-reduced-motion` alternatives.

---

## 2. INTERACTION PRINCIPLES

1. **User Agency Over Automation:** The user must always remain in complete control of the interface. Animations must respond directly to user action (scroll, drag, click) rather than running in unconstrained autonomous loops.
2. **Zero Scroll-Jacking:** Never hijack the browser's native window scroll physics, velocity, or momentum. Utilize standard CSS sticky positioning (`position: sticky`) within an extended scroll container (`350vh`).
3. **Multi-Modal Controls:** Always provide multiple pathways to achieve an interaction (e.g., disassemble via scroll OR manual scrubber slider; navigate via scroll OR skip button).
4. **Instant Tactile Feedback:** Interactive elements must respond immediately ($\le 50\text{ms}$) with subtle visual feedback (border illumination, coordinate shift, scale adjustment).
5. **Universal Accessibility:** Every interactive experience must remain fully operable via keyboard and accessible under reduced-motion constraints.

---

## 3. 3D HERO DISASSEMBLY CHOREOGRAPHY

The interactive disassembly maps normalized scroll progress $t \in [0, 1]$ to discrete physical component translations along the Z-axis:

$$\begin{array}{rll}
t \in [0.00, 0.20]: & \textbf{State 1: Fully Assembled} & \text{Phone is intact; camera rotates subtly to showcase finish} \\
t \in [0.20, 0.40]: & \textbf{State 2: Enclosure Lift} & \text{Front display panel (+Z) and rear glass (-Z) separate} \\
t \in [0.40, 0.65]: & \textbf{State 3: Internal Organs} & \text{Battery cell, camera array, and vapor chamber lift from frame} \\
t \in [0.65, 0.85]: & \textbf{State 4: Board Sub-Assembly}& \text{Motherboard, SoC heat shield, and speaker sub-assemblies emerge} \\
t \in [0.85, 1.00]: & \textbf{State 5: Exploded Technical}& \text{All 7 internal layers suspended at maximum separation with hotspot pins}
\end{array}$$

### Mandatory Controls Accompanying the 3D Hero
1. **The Skip Escape Hatch:** A floating action button (`// SKIP TEARDOWN [↓]`) in the top right that smoothly scrolls the viewport past the `350vh` track directly to Chapter 01.
2. **The Manual Scrubber:** A compact range slider positioned beneath the 3D canvas allowing users on trackpads or mobile devices to scrub the explosion progress $t$ without scrolling.
3. **The Reassemble Trigger:** A 1-click button (`// REASSEMBLE DEVICE`) that smoothly animates $t \to 0$ over $600\text{ms}$ with ease-out physics.
4. **Interactive Hotspot Pins:** Small numbered coordinate badges pinned in 3D space over key components. Clicking a pin isolates that component and opens its telemetry specification card.

---

## 4. REDUCED-MOTION & ACCESSIBILITY SPECIFICATIONS

When `window.matchMedia('(prefers-reduced-motion: reduce)')` is active:
- The `350vh` sticky scroll track is automatically collapsed to a standard single-screen section (`100vh` or auto-height).
- The 3D real-time WebGL canvas is replaced by an **Interactive 2D Exploded Technical Blueprint**.
- The blueprint features a clean schematic diagram with accessible tab controls allowing the user to step through the 7 components sequentially.
- All scroll-driven translations, parallax shifts, and rapid transitions are completely disabled.

---

## 5. INTERACTION DESIGN WORKFLOW

```
[DEFINE INTERACTION TRIGGER] ─── (Scroll, Click, Drag, Hover, Keypress)
       │
       ▼
[VERIFY BROWSER PHYSICS] ─────── (Ensure zero scroll-jacking; verify sticky support)
       │
       ▼
[ATTACH REVERSIBLE STATE] ────── (Progress t in [0, 1]; bind cancel / reset triggers)
       │
       ▼
[ADD ESCAPE CONTROLS] ────────── (Include Skip and Manual Scrubber buttons)
       │
       ▼
[TEST KEYBOARD & REDUCED-MOTION] (Verify Tab order, Enter/Space actuation, reduced-motion state)
```

---

## 6. QUALITY AUDIT CHECKLIST

Before approving any interactive component, verify:
- [ ] Is window scroll-jacking strictly avoided?
- [ ] Does the 3D disassembly container exit cleanly into the next chapter without layout jumps?
- [ ] Is an explicit "Skip" button visible during the 3D hero experience?
- [ ] Can the exploded view be scrubbed manually via slider?
- [ ] Is an explicit "Reassemble" button functional?
- [ ] Can users navigate all hotspots and controls via keyboard alone (`Tab` / `Enter` / `Space`)?
- [ ] Does activating `prefers-reduced-motion` immediately switch to the accessible 2D schematic?

---

## 7. PROJECT CONTEXT & EXPLICIT LIMITATIONS

- **Context:** Interactions must feel like operating an advanced analytical instrument.
- **Limitations:** Do not implement complex gesture multi-touch controls that interfere with standard mobile browser page navigation.
