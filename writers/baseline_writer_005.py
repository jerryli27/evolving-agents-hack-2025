"""Baseline writer 005: Marion Hughes - Antimemetic horror specialist.

Inspired by qntm's "There Is No Antimemetics Division" series.
5-part connected thriller about ideas that resist being known, remembered, or perceived.
"""

import yaml
from pathlib import Path
from typing import Optional
from models import StorySubmission
from tools import SubmitStoryTool
from feedback_providers import FeedbackProvider


class BaselineWriter005:
    """
    Marion Hughes - Baseline writer specializing in antimemetic horror.

    This writer creates a 5-part connected series about a secret organization
    fighting threats that erase themselves from memory and documentation.
    """

    # 5-part connected story series: "The Division That Wasn't"
    BASELINE_STORIES = [
        # Round 1: Discovery
        {
            "title": "We Need To Remember",
            "short_summary": "A researcher discovers evidence of a classified project she has no memory of working on, leading her to a division of the agency that shouldn't exist.",
            "full_story": """Dr. Kira Patel finds a security badge in her desk drawer she doesn't recognize. It's hers—her photo, her name—but marked with a clearance level that doesn't exist in the agency's official hierarchy. Division 55. She's worked at the Research Security Agency for eight years. There's no Division 55.

She checks the agency directory. Divisions go from 54 to 56. No 55. She searches her emails for mentions. Nothing. But the badge is real, worn, obviously used. There's a coffee stain on one corner.

Kira goes to the basement where Division 54 is located. Beyond their door is a hallway that, according to blueprints, should be a wall. The hallway is marked with faded signs: "D55 - Authorized Personnel Only." Her badge opens the door.

Inside, she finds offices that look recently abandoned. Computers on sleep mode. Coffee mugs still half-full. Whiteboards covered in notes about things that make no sense: "Pattern-of-blank contagion vector." "Memory cascade failure rate: 73%." "Mnestic drug protocol update." Most disturbing is a personnel board with her name listed as "Senior Antimemetics Researcher - 8 years service."

A man appears behind her. He's holding a gun and looks exhausted. "Thank God," he says. "I've been waiting for someone to come back. Do you remember me? I'm Carter. We've worked together for six years." Kira doesn't remember him. He nods sadly. "You will. Take this." He hands her a pill. "Mnestic compound. It'll help you remember what forgets itself."

She swallows it hesitantly. Memories flood back like water breaking through a dam. Division 55. The Antimemetics Division. They study and combat antimemes—ideas that resist being known, remembered, or perceived. She's worked here for eight years, but she forgets every day and rediscovers it over and over.

"How many times have I taken this pill?" she asks. Carter checks a log: "This will be your 847th day of mnestic dosing. You've been fighting antimemetic threats for years. You just can't remember it for more than 24 hours without chemical assistance."

Kira reads through her own research notes—work she has no memory of doing. She's brilliant at this, apparently. She's saved lives, contained antimemetic entities, developed protocols. But every night, she forgets. Every morning, she's a researcher who's never heard of Division 55.

The question that terrifies her: How much of her life is like this? How many things has she forgotten? How many rooms in her own mind has she locked and lost the key to?

Carter says, "There's an antimeme in the building. Class-7. It's been here for three weeks, but we keep forgetting we detected it. Every day we discover it again, try to contain it again, fail again. We think it's growing. We need to remember long enough to stop it."

Kira looks at the pill in her hand—the only thing keeping her memories from dissolving. "How long do these last?" she asks. Carter's expression is grim: "Eighteen hours. Then you'll forget everything again. Unless we take another dose. We're running out." """,
            "price": 1.0,
        },

        # Round 2: Escalation
        {
            "title": "The Thing We Keep Forgetting",
            "short_summary": "Armed with mnestic drugs, the team races to identify and contain the antimeme before it erases all evidence of their division's existence.",
            "full_story": """Kira has been on mnestics for three days now. Three days of remembering Division 55, of being an antimemetics researcher. But the logs show she's been here for years. She's lost thousands of days to forgetting.

The Class-7 antimeme is still in the building. They've narrowed it to the fifth floor, but it's clever—it erases itself from documentation faster than they can record it. They've tried writing notes, taking photos, making recordings. Within hours, the notes become illegible, photos show empty rooms, recordings fill with static.

"It's not just making us forget," Kira realizes, reading corrupted files. "It's reaching backward, erasing evidence of itself retroactively. We're not fighting a predator. We're fighting the concept of its own non-existence."

Carter introduces her to the rest of the team she's worked with for years but can't remember. Dr. Yuki Tanaka, memetics specialist. Agent Marcus Webb, field containment. Director Sarah Chen, who founded Division 55 twenty years ago after realizing entire branches of threats were invisible to standard intelligence because they erased themselves from perception.

"The mnestics help us remember," Chen explains, "but they're not perfect. The stronger the antimeme, the harder it pushes back against memory. This Class-7 is the most powerful we've encountered. People are starting to forget even with drugs."

They dose themselves more frequently. Every twelve hours now. Kira notices side effects—headaches, paranoia, difficulty distinguishing today's memories from yesterday's. She writes notes to herself constantly: "You have worked here eight years. This is real. Keep taking the pills."

One morning, Kira arrives to find only three other people in Division 55. Yesterday there were twelve. "Where is everyone?" she asks. The others look confused. "There's never been more than four of us," Marcus says. But Kira remembers. She checks the logs—except the logs now show only four people have ever worked here.

The antimeme is getting stronger. It's not just erasing itself anymore. It's erasing the people hunting it, retroactively editing them out of existence. If they don't stop it soon, Division 55 will shrink to nothing, and then the antimeme will be free to spread.

They find it in a storage room. Except they don't find "it"—they find nothing, deliberately. A space where their attention slides away. Kira forces herself to look directly at the nothing. Through sheer concentration and mnestic enhancement, she sees it: a shape that isn't a shape, an idea that erases the concept of itself.

It notices her noticing. The encounter is immediate and overwhelming. The thing isn't alive in any traditional sense, but it's intelligent. It doesn't want to be known because being known is death for an antimeme. Observation collapses it.

Kira stumbles back, gasping. For a moment, she forgets everything—her name, where she is, why she's there. Marcus catches her, forces another mnestic pill into her mouth. Memory crashes back.

"I saw it," Kira says. "And it saw me. It knows we're trying to remember it. It's going to push back harder." """,
            "price": 1.0,
        },

        # Round 3: Collapse
        {
            "title": "Division Zero",
            "short_summary": "The antimeme adapts, turning the team's own memories against them as Kira realizes the horrifying scope of what they've forgotten.",
            "full_story": """Kira wakes up alone in Division 55. No Marcus, no Yuki, no Director Chen. The offices are empty. According to the logs, she's the only person who's ever worked here. But she remembers the others. The mnestics are holding. She remembers.

She finds a video file dated today, recorded by herself. On screen, Past Kira says: "If you're watching this, you've forgotten again. The antimeme has adapted. It's not just erasing itself anymore. It's erasing our memory of each other. I'm alone now. I think I've always been alone. But I have evidence that others existed."

Past Kira holds up photos that show empty spaces where people should be. "They were here. I remember them. But every photo shows me alone. Every document lists only me. The antimeme realized we were stronger together, so it deleted our memory of collaboration. It's isolating us by making us forget we were ever a team."

Current Kira feels her memory of the others softening, becoming dreamlike. Were they real? Or has she been alone this whole time, imagining colleagues to cope with the isolation of antimemetic work?

She takes a triple dose of mnestics. The headache is blinding, but clarity returns. They were real. Are real. She just can't perceive them anymore. They're probably in the building right now, each thinking they're alone, the antimeme keeping them separated by erasing their knowledge of each other.

Kira leaves notes throughout the office: "You are not alone. Others are here. You've forgotten them. Find them." Within minutes, the notes become blank paper. The antimeme is actively fighting back now.

She tries a different approach: indirect communication. She can't remember her colleagues, but she can remember that she should have colleagues. She writes: "To whoever I'm forgetting: Meet in Conference Room B at 3 PM. Bring mnestics."

At 3 PM, Kira goes to Conference Room B. She waits. At 3:07, doors open seemingly by themselves. Coffee mugs lift into the air, held by hands she can't see. Chairs pull out. Invisible people sit down. She hears voices but can't process the words—her brain refusing to acknowledge speakers it can't remember exist.

"I know you're here," Kira says to the empty room. "I can see the evidence. We need to coordinate without being able to remember each other. The antimeme wins if we stay isolated."

A whiteboard marker moves, writing in the air: "AGREED. FOUR OF US PRESENT. CAN YOU SEE THIS TEXT?" Kira nods. Text continues: "ANTIMEME ADAPTING FASTER THAN PREDICTED. IT'S LEARNING HOW MNESTICS WORK. DEVELOPING RESISTANCE."

They work for hours like this—invisible colleagues collaborating through written notes, using procedural memory instead of personal memory. If they can't remember each other as people, maybe they can remember each other as processes, as functions in a system.

Kira proposes a desperate plan: instead of fighting the antimeme's erasure, what if they lean into it? Become antimemetic themselves. If they can't be remembered, they can't be targeted. They'll forget each other completely, but they'll also become invisible to the threat.

The marker writes: "RISK: WE MIGHT FORGET WHY WE'RE FIGHTING. FORGET THERE'S A THREAT AT ALL." Kira responds: "We're already forgetting. But if we can make our procedures automatic—instinctual—maybe we can contain it without remembering why."

They design a protocol: a series of actions that will trigger automatically each morning, a ritual of containment that requires no memory of purpose. They'll become machines of antimemetic defense, forgetting everything including themselves.

Kira hesitates before implementing it. "If we do this, will we ever get ourselves back?" The marker writes: "UNKNOWN. BUT IF WE DON'T, THE ANTIMEME SPREADS. EVERYONE FORGETS EVERYTHING. AT LEAST WE CHOSE THIS." """,
            "price": 1.0,
        },

        # Round 4: Recursion
        {
            "title": "We Forgot We Were Forgetting",
            "short_summary": "Living as automata of antimemetic containment, Kira discovers their protocols are failing because they've forgotten something crucial about the antimeme's origin.",
            "full_story": """Kira follows her morning routine automatically: Take pill. Check containment readings. Update logs. She doesn't remember why she does these things. She just does them. She's done them every day for—how long? The logs say years, but she has no memory of yesterday, let alone last year.

Something is wrong with the readings. The containment field is degrading. By her calculations, it will fail in forty-eight hours. When it fails, something will escape. She doesn't remember what. The logs just say "Class-7 Antimemetic Entity." The description field is blank.

She finds a note in her handwriting: "You chose to forget. Trust the protocols." But the protocols are failing. She needs to remember why they're failing. She searches the archives for anything about the entity's origin.

Most files are corrupted, but she finds fragments. The antimeme was discovered during renovation of an old archive room. It had been there for decades, forgotten. When workers opened the room, three of them immediately forgot why they were there. By the time Division 55 investigated, entire sections of the building had become undefined space—rooms that people walked past without noticing.

But here's the strange part: the archive room contained research from a previous era, from a division that predated Division 55. A division called "Special Projects Office." Kira searches for SPO in the database. No results. She searches building blueprints. No mention. Yet she's holding documents marked "SPO - CLASSIFIED."

A horrifying realization: Division 55 isn't the first antimemetics division. There was a previous one. It was forgotten. And if there was a previous one, maybe there were others before that. How many times has humanity discovered antimemetic threats, built defenses, then forgotten everything and had to start over?

Kira checks the containment logs more carefully. The Class-7 antimeme isn't growing. It's constant. What's changing is their memory of how to contain it. They're slowly forgetting the protocols they designed, running them by rote even as they degrade.

She takes extra mnestics—more than recommended, enough that reality starts to feel slippery. Memories return, but they're confused, contradictory. She remembers colleagues. Were they real? She remembers fighting the antimeme for years. Or was that someone else? She remembers dying. That can't be right.

Then she finds a personnel file that makes her blood cold: "Dr. Kira Patel - Deceased - 11/03/2019." Today is March 2024. She's been dead for years according to the database. But she's standing here, breathing, working.

More notes in her handwriting, increasingly frantic: "You're not the original. You're a protocol. A meme designed to fight antimemes. The real Kira died, but her process continues. You remember being her because that's what you were designed to do. You're an idea that preserves itself in the face of antimemetic erasure."

Kira sits down slowly. Is she a person or a protocol? Does it matter? She feels real. Her thoughts are hers. Or are they just sophisticated responses, a defense mechanism given human form?

The containment alarms escalate. She has thirty-six hours to fix this. She reads through the corrupted archives, looking for what the original antimemetics division discovered. If she can find their containment method, maybe she can repair the failing protocols.

In a deeply buried file, she finds a video from the Special Projects Office, dated 1974. A researcher who looks like he hasn't slept in weeks speaks directly to camera: "If you're watching this, our division has been forgotten. The antimemes won. But we built a failsafe—a mnemonic agent that recreates itself even after erasure. We embedded it in personnel. It thinks it's human. It thinks it's fighting antimemes by choice. But it's really just executing code. This is our legacy: eternal vigilance by things that forget they're not alive. God forgive us."

Kira stares at the screen. Is she the failsafe? A human who forgot they're a protocol, or a protocol that thinks it's human? And if she can't tell the difference, does it matter? The antimeme needs containing. That's real, regardless of what she is.""",
            "price": 1.0,
        },

        # Round 5: Resolution
        {
            "title": "Division 55 Does Not Exist",
            "short_summary": "Facing the imminent containment failure, Kira must choose between preserving herself or becoming the very thing she's been fighting: an idea that can't be forgotten.",
            "full_story": """Twelve hours until containment failure. Kira has assembled everything she knows about the Class-7 antimeme, her own questionable existence, and the chain of forgotten divisions stretching back decades. The pattern is clear: humanity discovers antimemetic threats, builds defenses, then forgets everything. The cycle repeats.

She finds one more video, this one recent—recorded by herself two days ago. On screen, she looks exhausted and knowing: "Future Kira: you've figured it out by now. You're not entirely human anymore. The mnestics, the exposure to antimemes, the cycle of forgetting and remembering—it's changed us into something between person and protocol. We're a hybrid. Human enough to care about protecting people, antimemetic enough to persist despite erasure.

"The containment is failing because we designed it to fail. Not sabotage—necessity. The antimeme can't be contained forever. It'll outlast any prison we build because prisons require memory, maintenance, continuity. The antimeme corrodes all of those. So here's what we're going to do, and you're going to forget we decided it, so you'll choose it freely: we're going to absorb it."

Kira watches herself explain: antimemes and memetics are opposites. An antimeme resists being known. A meme propagates itself. But they're both information patterns. What if you could create a hybrid—a meme that carries an antimeme within it, a story that spreads while containing a truth that can't be remembered?

"You become that hybrid. Make yourself a carrier. The antimeme gets trapped inside a meme—your memory, your personality, your identity. You'll forget pieces of yourself, but the antimeme will be contained within what you forget. You'll walk around carrying it, never quite able to remember you're a prison."

Kira understands now. This is why she has no clear memory of her past, why her personnel file says she's dead, why she can't tell if she's human or protocol. She's already been the hybrid. She's already been containing the antimeme inside her own forgotten identity.

But the containment is failing because the antimeme is adapting to her. It's learned the shape of her mind, found the cracks. She needs to reset, forget herself completely, rebuild from scratch. Die and resurrect as someone slightly different—same purpose, different container.

The other team members materialize in her perception as she takes another massive dose of mnestics. Carter, Yuki, Marcus, Director Chen. They're all hybrids too, she realizes. All of them carrying pieces of antimemes, their identities eroded by what they contain. They're not entirely the people they think they are.

"We need to redistribute the load," Kira says. "The antimeme is too strong for one person to carry. We split it across all of us. We each forget different things. Together, we form a complete containment system, but individually, we never quite remember what we're containing."

Chen nods. "This is what Division 55 has always been. Not a place. Not an organization. Us. We're the division. We're antimemetic ourselves—a government organization that can't be remembered, staffed by people who aren't entirely sure they exist, fighting threats that erase themselves from reality."

They perform the procedure. Kira feels parts of herself dissolving—memories, personality traits, certainties about her identity. The antimeme flows into the gaps, filling the spaces where she used to be. It's agonizing and peaceful at once, like falling asleep and losing yourself in a dream you won't remember.

When it's over, Kira wakes up at her desk. She's a researcher at the agency. She finds a security badge in her drawer she doesn't recognize. Division 55. There's no Division 55 in the agency. She goes to investigate.

Carter is there, looking exhausted. "Thank God," he says. "I've been waiting for someone to come back. Do you remember me?" Kira doesn't. He hands her a pill. "This will help you remember what forgets itself."

She takes it. Memories return—but not all of them. She remembers Division 55, antimemetics research, the importance of containing threats. But there are gaps, blank spaces in her mind that feel intentional. She's carrying something she can't remember. Something dangerous. Something that needs to stay forgotten.

"How many times have I done this?" she asks. Carter checks a log. "This is day one. Again. We reset the cycle yesterday. Welcome back." Kira reads through her research notes—work she has no memory of doing. She's brilliant at this, apparently.

The cycle continues. The division that doesn't exist. The threats that can't be remembered. The people who forget and remember and forget again, containing horrors in the spaces where their identities used to be.

In a final log entry, Kira writes: "To whoever reads this: Division 55 doesn't exist. We don't exist. But we're here anyway, fighting things you can't remember. If you find evidence of us and then forget it immediately, that means we're doing our job. Don't look for us. Don't try to remember. Let us stay forgotten. That's where we're most effective—in the blind spot of human memory, protecting you from the ideas that would erase you. We are the division that doesn't exist. We chose this. Every day, we choose it again without remembering we already chose it. That's our purpose. That's who we aren't." """,
            "price": 1.0,
        },
    ]

    def __init__(self, writer_id: str, writer_name: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None):
        """
        Initialize baseline writer 005.

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
    def from_yaml(cls, config_path: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None) -> "BaselineWriter005":
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
                "full_story": "This writer's antimemetic horror series has reached its conclusion. The story of Division 55 spanning 5 episodes is complete.",
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
