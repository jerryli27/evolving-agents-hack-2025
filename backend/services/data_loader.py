"""Data loader to transform end-to-end simulation results into API format."""

import json
from pathlib import Path
from typing import Dict, List, Optional

# Writer metadata to enrich the data
WRITER_METADATA = {
    "baseline_001": {
        "description": "Specializes in psychological horror and existential narratives",
        "style_dna": "dark, philosophical, character-driven",
        "color": "#6366F1"  # Indigo
    },
    "baseline_002": {
        "description": "Master of identity crisis and surreal transformations",
        "style_dna": "surreal, introspective, metaphorical",
        "color": "#8B5CF6"  # Violet
    },
    "baseline_003": {
        "description": "Explores family dynamics and inherited trauma",
        "style_dna": "emotional, generational, character-focused",
        "color": "#EC4899"  # Pink
    },
    "baseline_004": {
        "description": "Crafts philosophical mysteries and existential questions",
        "style_dna": "cerebral, mysterious, thought-provoking",
        "color": "#F59E0B"  # Amber
    },
    "baseline_005": {
        "description": "Weaves ambitious sci-fi concepts with memory themes",
        "style_dna": "complex, sci-fi, ambitious",
        "color": "#10B981"  # Emerald
    }
}


class CompetitionDataLoader:
    """Loads and transforms competition data for the API."""

    def __init__(self, data_dir: str = "data/end_to_end_v0.1"):
        # Handle relative path - if running from backend/, go up one level
        data_path = Path(data_dir)
        if not data_path.exists():
            # Try going up one level (when running from backend/)
            data_path = Path("..") / data_dir
        if not data_path.exists():
            # Try absolute path from project root
            project_root = Path(__file__).parent.parent.parent
            data_path = project_root / data_dir

        self.data_dir = data_path
        self._writers_cache = None
        self._rounds_cache = None

    def load_writers(self) -> List[Dict]:
        """Load all writers with their metadata and total scores."""
        if self._writers_cache is not None:
            return self._writers_cache

        writers = []

        for json_file in sorted(self.data_dir.glob("*.json")):
            with open(json_file) as f:
                data = json.load(f)

            writer_id = data["writer_id"]
            writer_name = data["writer_name"]

            # Calculate total score across all rounds
            total_score = 0
            for writing in data["writings"]:
                if writing.get("feedback"):
                    # Convert 0-1 scale to 0-100 scale
                    total_score += writing["feedback"]["aggregated_total_score"] * 100

            # Get metadata or use defaults
            metadata = WRITER_METADATA.get(writer_id, {
                "description": "A talented writer exploring unique narrative styles",
                "style_dna": "experimental, varied, evolving",
                "color": "#64748B"  # Slate gray default
            })

            writer = {
                "writer_id": writer_id,
                "name": writer_name,
                "description": metadata["description"],
                "style_dna": metadata["style_dna"],
                "total_score": round(total_score, 1),
                "color": metadata["color"]
            }

            writers.append(writer)

        # Sort by total score descending
        writers.sort(key=lambda x: x["total_score"], reverse=True)

        self._writers_cache = writers
        return writers

    def load_rounds(self) -> List[Dict]:
        """Load all rounds with stories and scores."""
        if self._rounds_cache is not None:
            return self._rounds_cache

        # First, load all writer data
        all_writers_data = {}
        for json_file in sorted(self.data_dir.glob("*.json")):
            with open(json_file) as f:
                data = json.load(f)
                all_writers_data[data["writer_id"]] = data

        # Organize by rounds
        rounds_dict = {}

        for writer_id, writer_data in all_writers_data.items():
            for writing in writer_data["writings"]:
                submission = writing["submission"]
                feedback = writing.get("feedback")
                round_num = submission["round"]

                if round_num not in rounds_dict:
                    rounds_dict[round_num] = []

                # Transform to frontend format
                story = {
                    "story_id": f"{writer_id}_r{round_num}",
                    "writer_id": writer_id,
                    "round": round_num,
                    "title": submission["title"],
                    "logline": submission.get("short_summary", ""),
                    "excerpt": submission["full_story"][:200] + "..." if len(submission["full_story"]) > 200 else submission["full_story"],
                    "full_script": submission["full_story"],
                    "score": {
                        # Convert 0-1 scale to 0-100 scale
                        "composite": round(feedback["aggregated_total_score"] * 100, 1) if feedback else 0,
                        "reader_alignment": round(feedback["aggregated_relevance_score"] * 100, 1) if feedback else 0,
                        "novelty": round(feedback["aggregated_novelty_score"] * 100, 1) if feedback else 0,
                        "coherence": round(feedback["aggregated_quality_score"] * 100, 1) if feedback else 0
                    } if feedback else {},
                    "reader_feedback": {
                        "summary": feedback["aggregated_qualitative_feedback"] if feedback else "",
                        "tags": self._extract_tags(submission["title"], submission.get("short_summary", "")),
                        "detailed_comments": feedback["aggregated_qualitative_feedback"] if feedback else ""
                    } if feedback else {}
                }

                rounds_dict[round_num].append(story)

        # Convert to list format
        rounds = []
        for round_num in sorted(rounds_dict.keys()):
            rounds.append({
                "round": round_num,
                "stories": rounds_dict[round_num]
            })

        self._rounds_cache = rounds
        return rounds

    def load_finalists(self, n: int = 3) -> List[Dict]:
        """Load top N finalist stories based on score."""
        rounds = self.load_rounds()
        writers = self.load_writers()

        # Create writer lookup
        writer_lookup = {w["writer_id"]: w for w in writers}

        # Collect all stories with scores
        all_stories = []
        for round_data in rounds:
            for story in round_data["stories"]:
                if story.get("score", {}).get("composite", 0) > 0:
                    all_stories.append(story)

        # Sort by composite score descending
        all_stories.sort(key=lambda x: x.get("score", {}).get("composite", 0), reverse=True)

        # Get top N
        finalists = []
        for i, story in enumerate(all_stories[:n], 1):
            writer = writer_lookup.get(story["writer_id"], {})
            finalists.append({
                "story": story,
                "writer": writer,
                "ranking": i
            })

        return finalists

    def _extract_tags(self, title: str, summary: str) -> List[str]:
        """Extract tags based on keywords in title and summary."""
        text = (title + " " + summary).lower()
        tags = []

        # Keyword mapping
        keywords = {
            "emotional": ["love", "heart", "emotion", "feel", "tear"],
            "dark": ["dark", "horror", "death", "murder", "kill"],
            "philosophical": ["question", "exist", "meaning", "truth", "reality"],
            "mysterious": ["mystery", "secret", "hidden", "unknown", "strange"],
            "family": ["family", "mother", "father", "parent", "child"],
            "sci-fi": ["future", "technology", "ai", "space", "time"],
            "psychological": ["mind", "mental", "psycho", "memory", "identity"],
            "surreal": ["dream", "surreal", "bizarre", "weird", "abstract"],
            "engaging": ["twist", "reveal", "surprise", "discover"]
        }

        for tag, words in keywords.items():
            if any(word in text for word in words):
                tags.append(tag)

        # Always add at least 2-3 tags
        if len(tags) < 2:
            tags.extend(["engaging", "dramatic"])

        return tags[:4]  # Limit to 4 tags


# Global instance
_loader = None

def get_loader(data_dir: str = "data/end_to_end_v0.1") -> CompetitionDataLoader:
    """Get or create the global data loader instance."""
    global _loader
    if _loader is None:
        _loader = CompetitionDataLoader(data_dir)
    return _loader
