"""Baseline writer 002: Marcus Reid - Psychological suspense specialist.

Inspired by the style of Ruth Rendell and Patricia Highsmith.
5-part connected thriller series about identity, deception, and consequences.
"""

import yaml
from pathlib import Path
from typing import Optional
from models import StorySubmission
from tools import SubmitStoryTool
from feedback_providers import FeedbackProvider


class BaselineWriter002:
    """
    Marcus Reid - Baseline writer specializing in psychological suspense.

    This writer creates a 5-part connected series about a woman who assumes
    another's identity, with each story exploring the deepening consequences.
    """

    # 5-part connected story series: "The Replacement"
    BASELINE_STORIES = [
        # Round 1: The Switch
        {
            "title": "The Replacement",
            "short_summary": "After a chance encounter with her doppelgänger, a struggling artist makes a fateful decision that will change both their lives forever.",
            "full_story": """Claire sits in the hospital waiting room, exhausted from her overnight shift cleaning offices. Across from her sits a woman who could be her twin—same auburn hair, same angular face, same tired green eyes. The woman notices too, laughs nervously. "This is surreal."

They talk. The woman is Diane Ashworth, recently divorced, fleeing to her family's cottage to escape her life. Claire is Claire Novak, drowning in debt, working three jobs since her art career collapsed. They joke about switching lives—a fantasy that becomes less absurd as they talk.

Diane shows Claire photos of the cottage: secluded, peaceful, stocked with supplies. "I was going to disappear for six months," Diane says. "No one would look for me. I told everyone I was traveling to Europe." Claire's eviction notice burns in her pocket. Her credit cards are maxed. Her landlord is threatening legal action.

When Diane goes to the restroom, she leaves her purse. Claire sees the cottage keys, Diane's ID, her credit cards. She thinks of her cramped apartment, the debt collectors, the hopelessness. When Diane returns, Claire asks carefully: "What if we actually did switch? Just for a while."

Two weeks later, Claire drives to the cottage under Diane's name while Diane—using Claire's ID—checks into a meditation retreat in California that Claire had booked but couldn't afford. They'll trade back in six months. A clean break. No one hurt.

Claire settles into Diane's cottage, into Diane's life. The debt and desperation fade. She paints again. But late at night, she wonders: what if six months isn't enough? What if she never wants to trade back?""",
            "price": 1.0,
        },

        # Round 2: The Discovery
        {
            "title": "The Other Life",
            "short_summary": "Living as Diane, Claire discovers disturbing secrets about the woman whose identity she borrowed, secrets that someone is willing to kill to protect.",
            "full_story": """Claire has been Diane Ashworth for three months now. She's learned Diane's habits, her handwriting, her preferences. The cottage is paradise—until the day a man appears at the door.

"Diane," he says, relief flooding his face. "Thank God. I was worried when you didn't answer my messages." Claire has been ignoring Diane's phone, part of their agreement. But this man—tall, intense, claiming to be Diane's old friend Marcus—won't leave easily.

Claire plays along, hoping he'll go. Instead, Marcus lingers, watching her carefully. "You seem different," he says. "Calmer." Claire deflects, but Marcus keeps returning, bringing groceries, inviting her for walks. She begins to enjoy his company, guiltily.

One evening, Marcus arrives agitated. "Did you find it?" he asks. "The documentation? The proof?" Claire has no idea what he means. Marcus's friendly demeanor cracks. "Don't play games, Diane. You told me before you left that you had evidence about the embezzlement. Where is it?"

Claire searches the cottage after Marcus leaves. In a hollow book, she finds a flash drive and documents showing massive fraud at Diane's former workplace—her ex-husband's company. Diane wasn't running from divorce. She was running from criminals.

That night, someone breaks into the cottage. Claire hides, watching a figure search methodically, violently. When they leave, Claire finds a message spray-painted on the wall: "WE KNOW YOU'RE NOT HER."

The real Diane doesn't answer Claire's frantic calls. Claire is trapped in an identity that's far more dangerous than she knew, hunted by people who've somehow discovered she's an impostor. But how?""",
            "price": 1.0,
        },

        # Round 3: The Confrontation
        {
            "title": "Two Faces",
            "short_summary": "The real Diane returns unexpectedly, forcing Claire to confront the life she's stolen and the danger she's brought to both of them.",
            "full_story": """Claire wakes to find Diane at the door—gaunt, panicked, furious. "What have you done?"

Claire explains about Marcus, the break-in, the documents. Diane cuts her off. "Marcus? I don't know any Marcus." The blood drains from Claire's face.

Diane never went to California. Someone intercepted her at the airport, held her in a warehouse demanding the evidence. She escaped three days ago. "You were supposed to be invisible," Diane says bitterly. "Instead you've been parading as me, making yourself visible."

That evening, Marcus appears. He looks from Diane to Claire, smiling slowly. "Two Dianes. Fascinating." He pulls out a gun. "Which one has the evidence?"

They must work together now. The embezzlement scheme connects to organized crime and corrupt police. In the chaos of Marcus searching, they escape into the woods. Running through darkness, Claire realizes: there's no going back. She's permanently entangled in Diane's nightmare, both of them marked for death.""",
            "price": 1.0,
        },

        # Round 4: The Trap
        {
            "title": "Reflections",
            "short_summary": "On the run and out of options, Claire and Diane devise a desperate plan to turn their identical appearance into a weapon against their pursuers.",
            "full_story": """Hiding in a motel, Claire and Diane plan survival. They can't go to police—Diane's documents implicate two detectives. Their only advantage: their pursuers don't realize there are two of them.

"We use it," Claire says. "Make them see Diane everywhere." They craft a plan: appear in multiple places simultaneously, create contradicting alibis, drive their hunters into paranoia.

It works. Marcus reports seeing Diane in Boston while his team corners her in Providence. Security footage shows her in two cities at once. The organization fractures, suspecting betrayal.

But Claire and Diane fracture too. Living as each other, they blur together. In reflections, they can't tell which one they're seeing. "I could have stayed disappeared," Diane says one night. "Let you take all of this." She resents Claire—for the switch, for the danger, for how easily Claire slipped into her existence.

They arrange to meet the organization's leader. Both women will appear—the shock should let them broadcast the evidence. But the night before, Claire wakes to find Diane gone and a note: "I'm sorry. Only room for one of us. —D" Diane plans to let Claire die in her place.""",
            "price": 1.0,
        },

        # Round 5: The Resolution
        {
            "title": "Identity",
            "short_summary": "The final confrontation forces both women to decide who they really are and what price they're willing to pay for survival.",
            "full_story": """Claire races to the warehouse where Diane agreed to meet the organization. She knows it's a trap—Diane intends to sacrifice her. But Claire has spent months being Diane; she knows how Diane thinks.

She arrives early. Diane is already there, nervous. "You shouldn't have come," Diane says. "Neither should you," Claire responds. Twin faces, twin desperation.

Marcus arrives with four others. "Two Dianes. I suppose we kill you both." But his team is paranoid from weeks of contradictory sightings.

Claire executes her plan: she's uploaded all evidence to news outlets with dead-man's switches. If they don't check in hourly, everything goes public. She's sent personalized packages to each hunter—evidence of their specific crimes.

"We've made ourselves too valuable to die," Claire says. "Every hour we live, your secrets stay hidden. The moment we disappear, you all go down." Information as ammunition. The organization fractures. Marcus turns on his superior. In the chaos, Claire and Diane escape.

Months later, after testimony and witness protection, they meet one final time. Different haircuts, different lives ahead. New identities, ironically. "I almost killed you," Diane admits. "We both did what we had to," Claire responds.

They part ways, two women who shared a face and briefly shared a life. Claire—now Emily—starts over. This time, she knows who she is. She paints her own truth. In the mirror, finally, she sees only herself.""",
            "price": 1.0,
        },
    ]

    def __init__(self, writer_id: str, writer_name: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None):
        """
        Initialize baseline writer 002.

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
    def from_yaml(cls, config_path: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None) -> "BaselineWriter002":
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
                "full_story": "This writer's connected story series has reached its conclusion. The identity thriller spanning 5 episodes is complete.",
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
