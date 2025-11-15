"""Baseline writer 003: Sarah Kim - Family drama specialist.

Inspired by the style of Anne Tyler and Alice Munro.
5-part connected family saga about secrets, forgiveness, and generational bonds.
"""

import yaml
from pathlib import Path
from typing import Optional
from models import StorySubmission
from tools import SubmitStoryTool
from feedback_providers import FeedbackProvider


class BaselineWriter003:
    """
    Sarah Kim - Baseline writer specializing in intimate family dramas.

    This writer creates a 5-part connected series following three generations
    of a Korean-American family grappling with inheritance, memory, and identity.
    """

    # 5-part connected story series: "The House on Maple Street"
    BASELINE_STORIES = [
        # Round 1: The Inheritance
        {
            "title": "What We Inherit",
            "short_summary": "When their grandmother dies, three siblings return to childhood home and discover a locked room no one was ever allowed to enter.",
            "full_story": """Grace Kim hasn't been back to the Maple Street house in fifteen years, not since the fight with her mother that ended with slammed doors and unspoken estrangement. Now both her parents are gone, and Halmoni—her grandmother—has died at ninety-three, leaving the house to Grace and her siblings equally.

Grace's brother James arrives from Seattle with his husband. Her sister Min comes from Boston with her two teenagers. They've stayed in touch, mostly, but haven't all been together since their father's funeral a decade ago. The house feels smaller than remembered, filled with the accumulated debris of lives lived: Korean ceramics, old photograph albums, furniture that was old even when they were children.

Halmoni's will includes a strange clause: there's a locked bedroom on the second floor. She left three keys, one for each grandchild, with instructions to open it together. None of them remember ever being allowed in that room.

They climb the stairs, insert the three keys simultaneously. The door opens on a room frozen in time—a young woman's room from the 1950s. Poodle skirts in the closet. Records by crooners. But also: Korean textbooks, letters in Hangul, photographs of people they don't recognize.

In a trunk, they find a baby blanket embroidered with a name: "Soo-jin." Not Halmoni's name. Beneath it, documents that make no sense—orphanage papers, adoption records from Korea dated 1953. Grace reads through them slowly, her Korean rusty but adequate. "I think," she says quietly, "Halmoni had a daughter before she came to America. A daughter she left behind."

The revelation cracks open questions none of them knew to ask about their family's history, their grandmother's silence, and the inheritance that matters more than the house.""",
            "price": 1.0,
        },

        # Round 2: The Search
        {
            "title": "The Daughter Left Behind",
            "short_summary": "Determined to find their grandmother's lost daughter, the siblings uncover painful truths about war, sacrifice, and impossible choices.",
            "full_story": """Grace becomes obsessed with finding Soo-jin. She contacts adoption agencies, hires a genealogist in Seoul. James thinks she should let it go, but Grace can't. She remembers her grandmother's sad songs, her silences.

The genealogist finds records. Soo-jin was born in 1952 during the Korean War. Halmoni—then Park Mi-sun, twenty years old—was unmarried. The baby's father was American, a soldier who died in combat before learning about the pregnancy.

In post-war Korea, an unwed mother with a mixed-race child faced impossible stigma. Halmoni placed Soo-jin in an orphanage, intending to return. When the opportunity came to immigrate to America, she took it, leaving Soo-jin behind. She sent money for years. Then the letters stopped being answered.

Soo-jin was never adopted. She grew up in that orphanage, worked there as an adult, married, had children. She died in 2003.

But she had children. Two daughters. Grace, James, and Min have cousins in Korea who don't know they exist.

Min is angry. "Halmoni could have brought her." James defends their grandmother: "You don't know what it was like." Grace simply mourns a connection that almost was.

Grace sends a letter to the Korean cousins. Weeks later, an email arrives: "My mother never spoke of being adopted or having a mother in America. Are you certain? This changes everything.""",
            "price": 1.0,
        },

        # Round 3: The Meeting
        {
            "title": "Two Families",
            "short_summary": "The Korean and American branches of the family meet for the first time, forcing everyone to reconcile different versions of the same history.",
            "full_story": """Grace, James, and Min fly to Seoul. At Incheon Airport, they spot two women holding a sign: Lee Hye-jin and Lee Soo-young, daughters of the grandmother they never knew.

The first dinner is awkward, conducted through translation apps. Hye-jin speaks some English. They compare photographs. Soo-jin looks startlingly like Grace.

Hye-jin and Soo-young share their mother's story—how Soo-jin built a life from nothing. "She was happy," Soo-young insists. "She didn't need a mother who abandoned her."

The word "abandoned" lands heavily. Grace explains Halmoni's circumstances. Soo-young won't hear it. "For sixty years, she had money to search. She chose not to."

James asks: "Did your mother ever wonder about her birth family?" Hye-jin admits: "Always. She said she felt incomplete."

They visit Soo-jin's grave. Grace leaves flowers, whispers an apology for her grandmother who couldn't. They're mourning not just Soo-jin but all the relationships that could have been.

That evening, Soo-young breaks down. "I'm angry at your grandmother, but also at my mother for dying without knowing the truth." Grace holds her cousin's hand. Strangers, but grief makes them family.

Before leaving, Hye-jin gives them a box: drawings, school papers, a journal. And photographs—including one of Soo-jin as a baby with Halmoni. Someone at the orphanage kept it.

Grace finally understands: Halmoni kept the secret not from shame but from unbearable pain. Some losses are too great to speak aloud.""",
            "price": 1.0,
        },

        # Round 4: The Return
        {
            "title": "Rooms We Keep Locked",
            "short_summary": "Back in America, each sibling struggles with family secrets of their own, realizing they've inherited more than they knew from their grandmother's silence.",
            "full_story": """Returning home, Grace sees the house differently. The locked room makes sense—a shrine to grief too enormous to enter. She wonders what rooms she keeps locked in her own life.

For Grace, it's her marriage. She and Michael have been "fine" for years—politely distant. She stayed after his affair, but they never repaired. She's been living in her own locked room.

James calls, distressed. His husband wants children, but James is terrified. "What if I mess them up?" Grace hears their mother's voice in his fears—a mother who loved them but couldn't express it.

Min arrives with her teenagers. She's left her husband. "Twenty years of trying to be the perfect daughter-in-law," she says, crying. "I can't do it anymore." She's ashamed of "failing," even knowing it's not failure to leave unhappiness.

The three siblings sit in their grandmother's kitchen, realizing they've all inherited her silence. They learned to lock away pain, to endure rather than speak. The family disease of swallowing grief.

"We're selling the house," James says, "but carrying it with us." Min nods. "We need to learn to open our locked rooms before we become like Halmoni—full of love but unable to share it."

Trauma echoes across generations, but so can healing. They can choose differently.

That night, Grace calls Michael. "We need to talk. Really talk. About everything." She's opening the door she's kept locked for years.""",
            "price": 1.0,
        },

        # Round 5: The New Foundation
        {
            "title": "Building from Remains",
            "short_summary": "A year later, the family gathers again to lay the foundation for something new, built on truth instead of silence.",
            "full_story": """The Maple Street house sells to a young family. Grace keeps her grandmother's recipe box, photographs, and that picture of Halmoni holding baby Soo-jin.

Grace and Michael are in therapy, rebuilding. Some days uncertain, but trying honestly. James is starting adoption. "Terrified, but doing it anyway." Min has her own apartment now. Her daughter said: "Mom, you seem like yourself."

The Korean cousins—Hye-jin and Soo-young—visit America. The siblings pick them up, nervous and excited. They've been emailing, building a relationship across oceans.

They gather at Grace's for a memorial, lighting incense for Halmoni and Soo-jin. Hye-jin brings a letter Soo-jin wrote late in life but never sent.

Min translates: "To my mother: I understand now that love and leaving can exist together. I forgive you. I turned out okay. I have daughters who love me. That's enough."

They cry—for loss, for what almost was, but also in gratitude they found each other.

Later, Min's daughter asks: "Are we going to keep in touch?" Hye-jin smiles. "We're family. That's not a choice. It's just true."

Grace looks at this patchwork family—siblings and cousins, American and Korean—and thinks: This is what we inherit. Not just pain, but also the possibility of building something new. The house is gone, but they carry its foundation.

Outside, snow falls. The children run to see it. Inside, the adults watch them make new memories, writing a different ending. Sometimes the locked room opens not to reveal the past but to let in the future.""",
            "price": 1.0,
        },
    ]

    def __init__(self, writer_id: str, writer_name: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None):
        """
        Initialize baseline writer 003.

        Args:
            writer_id: Unique identifier for this writer
            writer_name: Human-readable name
            data_dir: Directory for storing data
            feedback_provider: Optional feedback provider
        """
        self.writer_id = writer_id
        self.writer_name = writer_name
        self.data_dir = data_dir
        self.submit_story_tool = SubmitStoryTool(data_dir, feedback_provider=feedback_provider)

    @classmethod
    def from_yaml(cls, config_path: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None) -> "BaselineWriter003":
        """Load from YAML configuration."""
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        return cls(
            writer_id=config_data["writer_id"],
            writer_name=config_data["writer_name"],
            data_dir=data_dir,
            feedback_provider=feedback_provider
        )

    def write_round(self, round_num: int) -> StorySubmission:
        """
        Execute a writing round with a hardcoded submission.

        Args:
            round_num: The current round number (1-5 for this series)

        Returns:
            The submitted story
        """
        # If round exceeds available stories, return empty template
        if round_num > len(self.BASELINE_STORIES):
            story_data = {
                "title": f"Round {round_num} - Series Complete",
                "short_summary": "The 5-part series has concluded.",
                "full_story": "This writer's connected family saga has reached its conclusion. The multi-generational story spanning 5 episodes is complete.",
                "price": 1.0,
            }
        else:
            story_data = self.BASELINE_STORIES[round_num - 1]

        # Submit the story and get feedback
        self.submit_story_tool.submit_story(
            writer_id=self.writer_id,
            writer_name=self.writer_name,
            title=story_data["title"],
            full_story=story_data["full_story"],
            round=round_num,
            short_summary=story_data["short_summary"],
            price=story_data["price"],
        )

        # Load and return the submission
        from tools.past_writings import PastWritingsTool
        past_writings_tool = PastWritingsTool(self.data_dir)
        history = past_writings_tool._load_history(self.writer_id)

        if history:
            writing = history.get_round_writing(round_num)
            if writing:
                return writing.submission

        # Fallback
        return StorySubmission(
            writer_id=self.writer_id,
            writer_name=self.writer_name,
            round=round_num,
            **story_data
        )

    def get_history(self):
        """Get the writer's complete history."""
        from tools.past_writings import PastWritingsTool
        past_writings_tool = PastWritingsTool(self.data_dir)
        return past_writings_tool._load_history(self.writer_id)
