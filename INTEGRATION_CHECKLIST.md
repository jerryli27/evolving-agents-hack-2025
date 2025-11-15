# Integration Checklist: Connecting Writer & Reader Agents

This document outlines exactly what you need from your teammates to integrate their writer agent and reader agent implementations with the frontend.

---

## 🎯 Quick Summary

You need your teammates to provide:
1. **Writer Agent** that generates stories with specific format
2. **Reader/Critic Agent** that scores stories and provides feedback
3. **Evolution Orchestrator** that runs 5 rounds of competition
4. **API Endpoints** that return data in the expected JSON format

---

## 📋 Data Contracts (What Format You Need)

Your frontend expects data in these exact TypeScript interfaces. Share these with your teammates:

### 1. Writer Data Structure

```typescript
interface Writer {
  writer_id: string;           // e.g., "writer_1"
  name: string;                // e.g., "Melodrama Maven"
  description: string;         // e.g., "Specializes in emotional arcs and tearjerker moments"
  style_dna: string;           // e.g., "high-emotion, character-driven, romantic tension"
  total_score: number;         // Sum of all composite scores across rounds
  color: string;               // Hex color for chart visualization, e.g., "#3B82F6"
}
```

**Example JSON:**
```json
{
  "writer_id": "writer_1",
  "name": "Melodrama Maven",
  "description": "Specializes in emotional arcs and tearjerker moments",
  "style_dna": "high-emotion, character-driven, romantic tension",
  "total_score": 425.3,
  "color": "#3B82F6"
}
```

### 2. Story Data Structure

```typescript
interface Story {
  story_id: string;            // e.g., "story_1_round_3"
  writer_id: string;           // e.g., "writer_1"
  round: number;               // 1-5
  title: string;               // e.g., "The Last Goodbye"
  logline: string;             // 1-2 sentence summary
  excerpt: string;             // First paragraph or teaser
  full_script: string;         // Complete script text
  score: {
    composite: number;         // Overall score (0-100)
    reader_alignment: number;  // How well it aligns with reader preferences (0-100)
    novelty: number;           // How original/creative (0-100)
    coherence: number;         // How logical/well-structured (0-100)
  };
  reader_feedback: {
    summary: string;           // 2-3 sentence critique
    tags: string[];            // e.g., ["emotional", "engaging", "plot-twist"]
    detailed_comments?: string; // Optional longer feedback
  };
}
```

**Example JSON:**
```json
{
  "story_id": "story_1_round_1",
  "writer_id": "writer_1",
  "round": 1,
  "title": "Shattered Glass Hearts",
  "logline": "A young architect discovers that every building she designs mysteriously affects the love lives of its occupants.",
  "excerpt": "Maya traced her fingers along the blueprint, unaware that the curved walls she was drawing would soon curve the path of two strangers toward an inevitable collision...",
  "full_script": "INT. ARCHITECT'S OFFICE - DAY\n\nMAYA (28, ambitious, wearing designer glasses) hunches over her drafting table...\n\n[Full script continues for 800-1200 words]",
  "score": {
    "composite": 85.2,
    "reader_alignment": 82.5,
    "novelty": 88.0,
    "coherence": 86.0
  },
  "reader_feedback": {
    "summary": "Strong emotional hook with an intriguing supernatural premise. Character voice is clear and engaging, though pacing could be tightened in the middle section.",
    "tags": ["emotional", "supernatural", "romance", "engaging"],
    "detailed_comments": "The opening effectively establishes Maya's character..."
  }
}
```

### 3. Round Data Structure

```typescript
interface RoundData {
  round: number;               // 1-5
  stories: Story[];            // All 5 writers' stories for this round
}
```

**Example JSON:**
```json
{
  "round": 1,
  "stories": [
    { /* story from writer_1 */ },
    { /* story from writer_2 */ },
    { /* story from writer_3 */ },
    { /* story from writer_4 */ },
    { /* story from writer_5 */ }
  ]
}
```

### 4. Finalist Data Structure

```typescript
interface Finalist {
  story: Story;                // The winning story (from final round)
  writer: Writer;              // The writer's info
  ranking: number;             // 1, 2, or 3
}
```

**Example JSON:**
```json
{
  "story": { /* full story object from round 5 */ },
  "writer": { /* full writer object */ },
  "ranking": 1
}
```

---

## 🔌 Required API Endpoints

Your teammates need to implement these endpoints in `backend/main.py`:

### 1. GET `/api/writers`

**Returns:** List of all 5 writer agents with their cumulative stats

**Response Format:**
```json
[
  {
    "writer_id": "writer_1",
    "name": "Melodrama Maven",
    "description": "Specializes in emotional arcs...",
    "style_dna": "high-emotion, character-driven...",
    "total_score": 425.3,
    "color": "#3B82F6"
  },
  // ... 4 more writers
]
```

**Current Status:** ✅ Template exists, needs real data

---

### 2. GET `/api/rounds`

**Returns:** All 5 rounds with all stories generated

**Response Format:**
```json
[
  {
    "round": 1,
    "stories": [
      { /* writer_1's story */ },
      { /* writer_2's story */ },
      { /* writer_3's story */ },
      { /* writer_4's story */ },
      { /* writer_5's story */ }
    ]
  },
  // ... rounds 2-5
]
```

**Current Status:** ✅ Template exists, needs real data

---

### 3. GET `/api/finalists`

**Query Param:** `n` (optional, default 3)

**Returns:** Top N finalist stories with rankings

**Response Format:**
```json
[
  {
    "story": { /* winning story */ },
    "writer": { /* winning writer */ },
    "ranking": 1
  },
  {
    "story": { /* second place story */ },
    "writer": { /* second place writer */ },
    "ranking": 2
  },
  {
    "story": { /* third place story */ },
    "writer": { /* third place writer */ },
    "ranking": 3
  }
]
```

**Current Status:** ✅ Template exists, needs real data

---

### 4. POST `/api/export-video` (Already Implemented ✅)

This is for your AI video export feature - already done!

---

## 🏗️ Backend Architecture They Need to Build

### Recommended File Structure

```
backend/
├── main.py                     # FastAPI app with endpoints (template exists)
├── services/
│   ├── video_export.py        # ✅ Done
│   ├── writer_agent.py        # ❌ NEED FROM TEAMMATES
│   ├── critic_agent.py        # ❌ NEED FROM TEAMMATES
│   └── orchestrator.py        # ❌ NEED FROM TEAMMATES
├── storage/
│   └── simple_db.py           # ❌ Optional - for caching results
└── data/
    └── evolution_results.json # ❌ Where they save results
```

---

## ✅ Integration Checklist for Teammates

Share this checklist with your teammates:

### Writer Agent (`backend/services/writer_agent.py`)

- [ ] **Create WriterAgent class** that:
  - Takes a writer persona (name, description, style_dna)
  - Uses Claude API to generate short drama scripts
  - Generates 800-1200 word scripts in proper format
  - Can learn from previous feedback and improve

- [ ] **Script Requirements:**
  - Title: Catchy, short drama title
  - Logline: 1-2 sentence hook
  - Excerpt: First 100-200 characters as teaser
  - Full Script: 800-1200 words, proper screenplay format
  - Genre: Short drama (TikTok/YouTube Shorts style)

- [ ] **Evolution Capability:**
  - Round 1: Generate initial story from persona
  - Rounds 2-5: Read previous feedback and improve

**Example Implementation Skeleton:**
```python
class WriterAgent:
    def __init__(self, writer_id: str, name: str, description: str, style_dna: str):
        self.writer_id = writer_id
        self.name = name
        self.description = description
        self.style_dna = style_dna
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def generate_story(self, round: int, previous_feedback: Optional[str] = None) -> Story:
        """Generate a story for the given round"""
        prompt = self._create_prompt(round, previous_feedback)
        # Use Claude to generate story
        # Parse into Story format
        # Return Story object
        pass
```

---

### Critic/Reader Agent (`backend/services/critic_agent.py`)

- [ ] **Create CriticAgent class** that:
  - Takes a story as input
  - Returns scores (composite, reader_alignment, novelty, coherence)
  - Generates feedback summary and tags
  - Is consistent across rounds (same quality story = same score)

- [ ] **Scoring Rubric:**
  - **Reader Alignment (0-100):** How well it hooks the audience
  - **Novelty (0-100):** Originality and creative storytelling
  - **Coherence (0-100):** Plot structure, pacing, logic
  - **Composite (0-100):** Weighted average or formula

- [ ] **Feedback Format:**
  - Summary: 2-3 sentences of constructive critique
  - Tags: 3-5 descriptive tags (emotional, engaging, plot-twist, etc.)
  - Detailed comments: Optional longer analysis

**Example Implementation Skeleton:**
```python
class CriticAgent:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def score_story(self, story_text: str, title: str) -> dict:
        """Score a story and provide feedback"""
        prompt = self._create_scoring_prompt(story_text, title)
        # Use Claude to analyze story
        # Parse scores and feedback
        # Return formatted dict
        pass
```

---

### Evolution Orchestrator (`backend/services/orchestrator.py`)

- [ ] **Create Orchestrator class** that:
  - Runs 5 rounds of competition
  - Manages 5 writer agents
  - Coordinates writing → critiquing → learning loop
  - Stores results in memory or JSON file
  - Calculates final rankings

- [ ] **Evolution Flow:**
  ```
  For each round (1-5):
    1. Each writer generates a story
    2. Critic scores all 5 stories
    3. Writers receive feedback
    4. Store round results

  After round 5:
    1. Calculate total scores
    2. Rank top 3 finalists
    3. Save complete results
  ```

**Example Implementation Skeleton:**
```python
class EvolutionOrchestrator:
    def __init__(self):
        self.writers = self._create_writers()
        self.critic = CriticAgent()
        self.rounds_data = []

    def _create_writers(self) -> List[WriterAgent]:
        """Create 5 unique writer agents with different styles"""
        return [
            WriterAgent("writer_1", "Melodrama Maven", "...", "high-emotion..."),
            WriterAgent("writer_2", "Plot Twist Master", "...", "surprise-driven..."),
            # ... 3 more
        ]

    async def run_evolution(self) -> dict:
        """Run all 5 rounds and return complete results"""
        for round_num in range(1, 6):
            round_data = await self._run_round(round_num)
            self.rounds_data.append(round_data)

        finalists = self._calculate_finalists()
        return {
            "writers": [w.to_dict() for w in self.writers],
            "rounds": self.rounds_data,
            "finalists": finalists
        }

    async def _run_round(self, round_num: int) -> RoundData:
        """Run a single round"""
        stories = []
        for writer in self.writers:
            story_text = await writer.generate_story(round_num)
            scores = await self.critic.score_story(story_text)
            story = Story(writer_id=writer.writer_id, round=round_num, **scores)
            stories.append(story)
        return {"round": round_num, "stories": stories}
```

---

### Update API Endpoints (`backend/main.py`)

- [ ] **Import orchestrator:**
  ```python
  from services.orchestrator import EvolutionOrchestrator

  orchestrator = EvolutionOrchestrator()
  ```

- [ ] **Run evolution on startup (or on-demand):**
  ```python
  @app.on_event("startup")
  async def startup_event():
      global evolution_results
      # Check if results exist in cache
      if not os.path.exists("data/evolution_results.json"):
          evolution_results = await orchestrator.run_evolution()
          # Save to JSON
      else:
          # Load from JSON
          with open("data/evolution_results.json") as f:
              evolution_results = json.load(f)
  ```

- [ ] **Update GET endpoints:**
  ```python
  @app.get("/api/writers")
  def get_writers():
      return evolution_results["writers"]

  @app.get("/api/rounds")
  def get_rounds():
      return evolution_results["rounds"]

  @app.get("/api/finalists")
  def get_finalists(n: int = 3):
      return evolution_results["finalists"][:n]
  ```

---

## 🧪 Testing Integration

### Step 1: Test Backend Locally

Your teammates should be able to run:

```bash
cd backend
uvicorn main:app --reload
```

Then visit: http://localhost:8000/docs

They should see:
- ✅ GET `/api/writers` returns 5 writers
- ✅ GET `/api/rounds` returns 5 rounds with stories
- ✅ GET `/api/finalists` returns top 3

### Step 2: Connect Frontend to Backend

Once their backend is working:

1. **Set environment variable:**
   ```bash
   # In frontend/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. **Remove mock mode:**
   ```bash
   # Comment out or remove
   # NEXT_PUBLIC_USE_MOCK=true
   ```

3. **Test frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Verify:**
   - Chart shows real evolution trajectories
   - Finalists show actual AI-generated stories
   - Click "View Script" shows real scripts
   - Export to Video works with real scripts

---

## 📊 Sample Test Data

For initial testing, your teammates can use this sample data structure:

```json
{
  "writers": [
    {
      "writer_id": "writer_1",
      "name": "Melodrama Maven",
      "description": "Creates emotionally charged romantic dramas",
      "style_dna": "high-emotion, character-driven, romantic tension",
      "total_score": 425.3,
      "color": "#3B82F6"
    }
    // ... 4 more
  ],
  "rounds": [
    {
      "round": 1,
      "stories": [/* 5 stories */]
    }
    // ... 4 more rounds
  ],
  "finalists": [/* top 3 */]
}
```

---

## 🚨 Common Integration Issues

### Issue 1: CORS Errors

**Solution:** Already configured in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: Type Mismatches

**Solution:** Use Pydantic models to validate data:
```python
from pydantic import BaseModel

class Writer(BaseModel):
    writer_id: str
    name: str
    description: str
    style_dna: str
    total_score: float
    color: str
```

### Issue 3: Slow Response Times

**Solution:** Cache evolution results:
- Run evolution once
- Save to JSON file
- Load from cache on subsequent requests
- Re-run only when needed

---

## 📞 Questions to Ask Your Teammates

Before they start coding, confirm:

1. ✅ **Do they have access to Anthropic API key?**
   - They need it for Claude API
   - Should be in `.env` file

2. ✅ **Have they seen the data structures above?**
   - Share this document with them
   - Make sure they understand the JSON format

3. ✅ **What's their timeline?**
   - When will writer agent be done?
   - When will critic agent be done?
   - When can you integrate?

4. ✅ **Are they using Pydantic for data validation?**
   - Recommended to avoid type errors
   - Already installed in requirements.txt

5. ✅ **How are they storing results?**
   - In-memory? (Lost on restart)
   - JSON file? (Persists)
   - Database? (Overkill for hackathon)

---

## 🎯 Minimum Viable Integration

If time is tight, here's the bare minimum needed:

### Absolute Minimum:
1. **One working writer agent** that generates stories
2. **One working critic agent** that scores stories
3. **Script that runs 5 rounds** and saves to JSON
4. **Load JSON from backend API endpoints**

### Nice to Have:
- 5 diverse writer personas
- Sophisticated scoring algorithm
- Learning/improvement between rounds
- Real-time evolution (not pre-cached)

---

## 🎉 Success Criteria

You know integration is complete when:

- ✅ Frontend loads without errors
- ✅ Chart shows 5 different colored lines evolving
- ✅ Click on a line shows writer details
- ✅ Top 3 finalists appear with real AI stories
- ✅ "View Script" shows actual generated scripts
- ✅ "Export to Video" creates beat sheets from real scripts
- ✅ Everything looks professional and demo-ready

---

## 📧 Template Message for Teammates

Feel free to copy/paste this to your teammates:

---

**Subject: Integration Requirements for Writer/Critic Agents**

Hey team! I've finished the frontend and need your backend to provide data in a specific format.

**Quick Summary:**
- I need 3 API endpoints: `/api/writers`, `/api/rounds`, `/api/finalists`
- Each returns JSON in a specific structure (see attached doc)
- You need to build: Writer Agent, Critic Agent, Evolution Orchestrator

**Detailed Guide:**
See `INTEGRATION_CHECKLIST.md` in the repo for complete specs.

**Key Data Structures:**
- Writer: {writer_id, name, description, style_dna, total_score, color}
- Story: {story_id, writer_id, round, title, logline, excerpt, full_script, score, reader_feedback}
- Round: {round, stories[]}
- Finalist: {story, writer, ranking}

**Timeline:**
When can you have this ready? I'm ready to integrate as soon as you have working endpoints.

**Testing:**
Run `uvicorn main:app --reload` and visit http://localhost:8000/docs to test your endpoints.

Let me know if you have questions!

---

Good luck with the integration! 🚀
