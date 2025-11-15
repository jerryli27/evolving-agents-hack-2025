# Story Evolution Sandbox - Frontend

A React/Next.js dashboard for visualizing and interacting with evolving writer agents that create short drama scripts.

## Features

### P0 - MVP (Completed)

✅ **Evolution Visualization**
- Multi-line chart showing writer performance over 5 rounds
- Switchable metrics (Composite, Reader Alignment, Novelty, Coherence)
- Interactive hover tooltips with writer details
- Click on points to view writer details

✅ **Writer Detail Panel**
- Full writer profile with style DNA
- Round-by-round story evolution
- Mini sparkline visualization
- Script excerpts and reader feedback
- Score breakdowns per round

✅ **Finalists Section**
- Top 3 performing writers displayed
- Ranking badges and scores
- Full script viewing
- Export to video functionality

✅ **Export to Video Pipeline**
- Configurable video length (30s/60s/90s/120s)
- Visual style selection
- Auto-generated beat sheet from script
- Copy as JSON or text prompt for AI video tools

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx          # Main dashboard page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── EvolutionChart.tsx      # Multi-line chart component
│   ├── WriterDetailPanel.tsx  # Writer details side panel
│   ├── FinalistsSection.tsx   # Top 3 finalists display
│   ├── ExportVideoModal.tsx   # Video export interface
│   └── ScriptViewModal.tsx    # Full script viewer
├── lib/
│   └── mockData.ts       # Sample data (to be replaced with API)
└── types/
    └── index.ts          # TypeScript type definitions
```

## Data Model

### Writers
Each writer has:
- Unique ID and name
- Description and style DNA
- Color for visualization
- Total score across rounds

### Stories
Each story includes:
- Title and logline
- Full script and excerpt
- Scores (composite, reader_alignment, novelty, coherence)
- Reader feedback with tags

### Rounds
5 rounds of evolution where:
- Writers create new stories
- Readers score and provide feedback
- Writers adapt based on feedback

## Key Interactions

1. **View Evolution**: Chart shows how each writer's scores evolve
2. **Explore Writers**: Click any point or legend to see writer details
3. **Read Scripts**: View full scripts from finalist cards
4. **Export to Video**: Generate structured prompts for AI video generation

## Next Steps (P1)

- [ ] Replace mock data with real API calls
- [ ] Add loading and error states
- [ ] Implement real reader feedback
- [ ] Backend-powered beat sheet generation

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **State**: React hooks (useState, useMemo)

## API Endpoints (Future)

```
GET /api/writers          # List all writers
GET /api/rounds           # Get all rounds data
GET /api/finalists?n=3    # Get top N finalists
POST /api/export-video    # Generate video blueprint
```

## Mock Data

Currently uses hardcoded data in `lib/mockData.ts` with:
- 5 unique writer personalities (Melodrama Maven, Plot Twister, Comedy Genius, Dark Realist, Fantasy Weaver)
- 5 rounds of evolution with realistic score progression
- Sample scripts with full content for Round 1
- Reader feedback with tags and summaries

Replace with API calls when backend is ready.

## Design Decisions

- **Responsive**: Works on mobile, tablet, and desktop
- **Dark mode**: Supports system dark mode preference
- **Accessibility**: Semantic HTML and proper labeling
- **Performance**: useMemo for expensive calculations
- **Type safety**: Full TypeScript coverage

## Learn More

This project was bootstrapped with Next.js. To learn more about Next.js:

- [Next.js Documentation](https://nextjs.org/docs)
- [Learn Next.js](https://nextjs.org/learn)
