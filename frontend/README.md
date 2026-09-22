# EOSync Frontend

Kommt in Phase 4. Erst wenn `POST /api/v1/search` echte Daten liefert.

Setup dann:

```bash
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

Geplante Struktur:

```
src/
├── api/client.ts        # fetch-Wrapper gegen das Backend
├── components/
│   ├── SearchBar.tsx
│   ├── SourceTabs.tsx
│   └── ExportButton.tsx
├── hooks/useGeneSearch.ts
└── pages/Results.tsx
```
