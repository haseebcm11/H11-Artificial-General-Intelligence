# H11-BROWSING Specification

## Overview
H11-BROWSING is an autonomous web interaction and content extraction agent designed for robust headless browser automation. It intelligently bridges the gap between raw DOM representations and LLM context constraints by applying semantic optimization.

## Core Capabilities
- **Semantic DOM Optimization**: Intelligently prunes irrelevant nodes (`<script>`, styles, invisible components) while retaining interactive pathways.
- **Headless Automation**: Interfaces with browser backends (Playwright, Puppeteer) via standardized protocol `HeadlessBrowser`.
- **Viewport Management**: Tracks dynamic changes via screenshots and state syncing after layout events (scrolling, clicking).
- **LLM-Oriented Context**: Outputs heavily filtered DOM representations designed specifically for reasoning models.

## Architecture
1. **Agent State**: `BrowserState` tracks the active URL, title, layout metrics, and an in-memory snapshot of the latest optimized DOM.
2. **DOM Optimizer**: Truncates arbitrary noise. Identifies ARIA roles and standard interactive tags to flag actionable elements.
3. **Action Dispatcher**: Translates declarative ActionTypes (`NAVIGATE`, `CLICK`, `TYPE`) into backend execution and automated state re-hydration.
