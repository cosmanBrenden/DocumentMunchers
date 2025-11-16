# Figma Electron App (Electron + React + TypeScript + Vite)

Quick setup:

1. Install dependencies

```bash
npm install
```

2. Run in development (starts Vite and Electron)

```bash
npm run dev
```

3. Build UI and package

```bash
npm run build
```

Project layout:

- `electron/` - Electron main and preload scripts
- `src/renderer` - Vite + React app (index.html, TSX entry, components)
- `dist/renderer` - built renderer output used by Electron in production

Notes:

- `preload.js` exposes a minimal `electronAPI` to the renderer. Use `window.electronAPI.send(...)` and `.receive(...)`.
- Adjust `electron-builder` config in package.json for packaging targets if needed.
