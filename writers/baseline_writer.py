"""Baseline writer implementation with hardcoded submissions."""

import yaml
import json
from pathlib import Path
from typing import Optional
from models import StorySubmission
from tools import SubmitStoryTool
from feedback_providers import FeedbackProvider


class BaselineWriter:
    """
    A baseline writer with hardcoded story submissions for benchmarking.

    These stories are plot synopses based on quality fictional works,
    not too well-known to avoid immediate recognition.
    """

    # Hardcoded story submissions for up to 10 rounds
    # Based on real fictional works, adapted into drama synopses
    BASELINE_STORIES = [
        # Round 1 - Inspired by "The Yellow Wallpaper" by Charlotte Perkins Gilman
        {
            "title": "The Pattern",
            "short_summary": "A woman confined to rest in an old mansion bedroom becomes obsessed with the wallpaper's mysterious pattern, spiraling into psychological turmoil.",
            "full_story": """Sarah arrives at a remote estate for a therapeutic retreat, prescribed by her physician husband after a difficult year. Confined to the upstairs bedroom with its peculiar yellow wallpaper, she's forbidden from working or stimulating her mind. As days pass, Sarah becomes fixated on the wallpaper's bizarre pattern—something seems trapped within it.

Against her husband's wishes, she begins documenting the pattern's changes. She notices a shape moving behind the surface design, a figure that creeps and crawls. Her husband dismisses her concerns as hysteria, insisting she rest more.

Sarah's obsession intensifies. She sees the figure more clearly now—a woman, desperate to escape. Night after night, Sarah watches the woman struggle against the pattern's bars. She begins to understand: the woman IS her, trapped by well-meaning concern that has become a cage.

On the final night, Sarah tears down the wallpaper in a frenzy, freeing the woman within. When her husband enters to find the room destroyed and Sarah crawling along the baseboards, she tells him calmly: "I've finally gotten out. And you can't put me back." He faints, and Sarah continues her methodical crawling over him, finally free.""",
            "price": 1.0,
        },
        # Round 2 - Inspired by "The Ones Who Walk Away from Omelas" by Ursula K. Le Guin
        {
            "title": "The Cost of Paradise",
            "short_summary": "A utopian city's prosperity depends on the suffering of one child. A young teacher discovers this truth and must decide whether to stay or walk away.",
            "full_story": """Elena has lived in Harmony Falls her entire life, a city where no one locks their doors, children play freely in parks, and prosperity seems endless. Crime is nonexistent, illness rare, happiness abundant. She's always accepted this as natural—until she becomes a teacher and learns what sustains it.

The city's council escorts her to the basement of the municipal building. There, in a small, windowless room, sits a seven-year-old child—filthy, malnourished, never spoken to, never comforted. The council explains: the city's good fortune is mystically bound to this child's misery. Everyone learns of it eventually. Most accept it as the price of their paradise.

Elena returns home shaken. She tries to resume her life, teaching her bright students, attending festivals. But the child's hollow eyes haunt her. She argues with neighbors who shrug: "What can we do? Helping the child would doom us all."

One morning, Elena packs a single bag. At the city limits, she finds others—people of all ages who couldn't accept the bargain. They don't speak, just nod in recognition. Together, they walk into the wilderness beyond, toward an uncertain future. Behind them, Harmony Falls gleams in the sunlight, perfect and damned.""",
            "price": 1.0,
        },
        # Round 3 - Inspired by "The Lottery" by Shirley Jackson
        {
            "title": "The Drawing",
            "short_summary": "A small town's annual tradition seems quaint until a newcomer discovers what really happens to the lottery winner.",
            "full_story": """June moves to Millbrook for a fresh start, charmed by its neighborly warmth and pastoral beauty. Everyone mentions the upcoming Summer Drawing—an old tradition, they say with odd smiles. When pressed for details, they change the subject.

The morning of the Drawing, the entire town gathers in the square. Children collect stones from the riverbed while parents chat nervously. The mayor draws names from an ancient wooden box. June notices Tessie Hutchinson's hands trembling when the mayor calls her family's name.

Another round of drawing follows—this time only the Hutchinsons participate. Tessie gets the marked slip. Her face drains of color. "This isn't fair!" she screams. The mayor intones: "The Drawing keeps our crops strong, our children healthy. It's always been this way."

The townsfolk, including Tessie's husband and children, pick up the stones. June stands frozen in horror as understanding dawns. Someone presses a stone into her hand. The crowd closes around Tessie, whose protests are drowned by the thuds of impact.

Later, at the community potluck, neighbors compliment the berry pies and discuss next week's farmer's market. No one mentions Tessie's name. June leaves her stone on a doorstep and drives away that night, never to return.""",
            "price": 1.0,
        },
        # Round 4 - Inspired by "The Metamorphosis" by Franz Kafka
        {
            "title": "The Change",
            "short_summary": "A devoted salesman wakes to find himself inexplicably transformed, forcing his family to confront who they really are.",
            "full_story": """Marcus wakes one Tuesday to discover he cannot move his body properly. Looking down, he sees not his familiar form but something fundamentally wrong—twisted, inhuman. He should be terrified, but his first thought is: "I'll miss my sales quota."

For years, Marcus has supported his parents and younger sister, working a soul-crushing job he hates. His family knocks on his locked door, demanding he hurry—they need him at work, need his paycheck. He tries to respond, but only produces guttural sounds.

When they finally break in and see him, his mother faints, his father curses, his sister screams. They barricade him in his room. Days pass. His sister slides food under the door, increasingly resentful. His father takes a job—something unthinkable when Marcus could provide.

Marcus discovers he can climb walls, hide in corners, exist in the darkness he's metaphorically inhabited for years. His family prospers without his burden. They laugh again, make plans. But they keep him locked away, ashamed.

One day, Marcus hears them discussing moving to a smaller apartment—one without room for him. That night, he slips away through a crack in the wall. His sister finds the empty room in the morning and cries, not from loss, but relief.""",
            "price": 1.0,
        },
        # Round 5 - Inspired by "The Tell-Tale Heart" by Edgar Allan Poe
        {
            "title": "The Sound",
            "short_summary": "A caretaker's meticulous plan to commit the perfect crime unravels as guilt manifests through an impossible sound.",
            "full_story": """Daniel has cared for the old man for three years. He bears him no ill will—loves him, even. But he cannot stand the old man's eye, that pale, filmy eye that watches him with what Daniel perceives as judgment. He decides the eye must be closed forever.

For seven nights, Daniel opens the bedroom door at midnight, shining his lantern on that horrible eye. On the eighth night, the old man wakes. Daniel strikes, swift and certain. He dismembers the body and hides it beneath the floorboards. The house is spotless, beyond suspicion.

Police arrive—a neighbor reported a shriek. Daniel welcomes them confidently, shows them around. They find nothing suspicious. Daniel suggests they rest in the very room where the body lies hidden. He's so clever, he thinks. So careful.

But as they chat, Daniel hears it—a low, rhythmic thumping. The old man's heart, beating beneath the floor. Impossible, yet undeniable. It grows louder, faster. The officers show no sign of hearing it, but Daniel knows they must. They're toying with him.

The sound becomes unbearable. "I admit it!" Daniel screams, tearing up the floorboards. "There! Beneath! Can't you hear that damned beating?" The officers exchange glances. The room is silent except for Daniel's ragged breathing and the heart that only he can hear.""",
            "price": 1.0,
        },
        # Round 6 - Inspired by "The Lady with the Dog" by Anton Chekhov
        {
            "title": "By the Sea",
            "short_summary": "A brief vacation romance between two unhappily married people evolves into something that changes their understanding of love and themselves.",
            "full_story": """Dmitri considers himself a connoisseur of brief affairs—a cynical Moscow banker who seduces vacationing women with practiced ease. In Yalta, he targets Anna, a young woman walking alone with her white dog, her provincial innocence obvious.

Their affair begins predictably. But afterward, Anna weeps—not coquettishly, but with genuine shame. "I've deceived myself," she says. "I wanted to live, truly live, and this is what I become." Her honesty unsettles Dmitri.

He returns to Moscow, expecting to forget her. But Anna haunts him. For the first time in his cynical life, he cannot move on. Months later, he travels to her provincial town, watches her at the theater with her husband—a man with remarkable side-whiskers who represents everything Dmitri finds contemptible.

They begin meeting secretly, in hotels in different cities. What started as a game has become necessity. Dmitri looks at his reflection—gray at the temples now—and realizes he's fallen in love for the first time at forty. They have no solution. She cannot leave her life; he cannot leave his.

The story ends with them in a hotel room, knowing their most difficult times lie ahead, yet unable to imagine existence apart. Love, Dmitri realizes, is not the conquest he imagined but a shared, complex burden that makes life finally meaningful.""",
            "price": 1.0,
        },
        # Round 7 - Inspired by "Bartleby, the Scrivener" by Herman Melville
        {
            "title": "I Would Prefer Not To",
            "short_summary": "A lawyer hires a peculiar copyist whose passive resistance to all requests slowly consumes everyone around him.",
            "full_story": """The lawyer prides himself on managing difficult employees—Turkey, who drinks at noon, and Nippers, who suffers from indigestion and ambition. When he hires Bartleby, the pale, quiet man seems like a relief. Bartleby copies documents mechanically, without complaint, almost without pause.

Then the lawyer asks Bartleby to review a document—standard procedure. "I would prefer not to," Bartleby responds calmly. Not refuse, not decline—prefer not to. The lawyer is too baffled to insist.

It happens again. And again. Bartleby stops copying entirely. He simply stands at his window, staring at a brick wall. "I would prefer not to leave," he says when the lawyer demands he work or depart. The lawyer tries reasoning, bribing, threatening. Nothing penetrates Bartleby's polite resistance.

The lawyer moves his entire office to escape Bartleby, who simply remains in the empty building. The new tenants have Bartleby arrested. The lawyer visits him in prison, tries to help, but Bartleby refuses meals. "I would prefer not to dine today," he says.

Bartleby dies curled against a prison wall. The lawyer learns he once worked in the Dead Letter Office, handling undeliverable mail—years of reading others' failed connections. The lawyer returns to his practice, but Bartleby's passive presence has changed something fundamental in how he views ambition, meaning, and his own complicity in a system that grinds people down.""",
            "price": 1.0,
        },
        # Round 8 - Inspired by "The Swimmer" by John Cheever
        {
            "title": "The Journey Home",
            "short_summary": "A man decides to swim home through his neighbors' pools, but the journey reveals the life he's been denying has fallen apart.",
            "full_story": """Ned stands at the Westerhazys' pool on a beautiful Sunday, struck by a whimsical idea: he'll swim home through every neighbor's pool, a water-route spanning the county. He dubs it the "Lucinda River" after his wife. The day is gorgeous, he's strong, life is good.

The first pools are welcoming—friends offer drinks, admire his athleticism. But Ned notices odd reactions. The Levys' pool is empty. Someone mentions, "After your misfortunes..." but Ned laughs it off, confused. Why would they think he'd had misfortunes?

As the afternoon wears on, Ned grows colder, weaker. The sky darkens. A party he crashes treats him with pity, not warmth. His former mistress turns cruel: "You showed up drunk at my door, begging for money." Ned has no memory of this.

The final pools are harsh—public, crowded, chlorinated. Ned is shivering, exhausted. Neighbors avoid him or whisper. At the Gilmartins', they ask about his house—"Is it true you sold it?"

Ned staggers to his home finally. The house is dark, locked, empty. For Sale sign on the lawn. The beautiful day has become a cold night. The Lucinda River was never a triumphant journey—it was denial, his mind protecting him from the collapse of his life. Standing before his abandoned house, reality crashes over Ned like ice water.""",
            "price": 1.0,
        },
        # Round 9 - Inspired by "The School" by Donald Barthelme
        {
            "title": "Everything Dies",
            "short_summary": "A teacher's class experiences a series of deaths—plants, animals, people—leading to an existential crisis about meaning and mortality.",
            "full_story": """Edgar teaches third grade at a progressive elementary school. This year has been marked by an unusual string of deaths. First, the herb garden—every plant withered despite careful attention. Then the classroom salamander, then the gerbils.

The tropical fish died in a bizarre overnight freeze. The puppy brought for show-and-tell got hit by a car in the parking lot. The children handled each loss with surprising resilience, asking increasingly sophisticated questions about death. Edgar tried to answer honestly.

Then things escalated beyond the classroom. The grandmother visiting their class for a storytelling session had a heart attack during recess. One student's father died in a construction accident. Another student, beloved Sarah with the bright laugh, was killed in a car crash on a field trip.

The children stop pretending. They confront Edgar directly: "Is death just something that happens? Is there a meaning? Do we just disappear?" Edgar, shaken himself, struggles to provide comfort or answers. He can't lie to them about death having purpose he doesn't believe in.

In desperation, Edgar and his co-teacher decide to give the children life instead of explanations. They bring in a couple of pet rabbits—male and female. "Let's see what happens," Edgar says. Within weeks, there are babies. The children laugh, amazed. Life persists, Edgar realizes, not because it means something, but because it simply does.""",
            "price": 1.0,
        },
        # Round 10 - Inspired by "The Housebreaker of Shady Hill" by John Cheever
        {
            "title": "The Good Neighbor",
            "short_summary": "A suburban father, desperate after losing his job, commits a crime that forces him to confront who he's become in pursuit of maintaining appearances.",
            "full_story": """Johnny Cash lives in Shady Hill, an affluent suburb where everyone knows everyone's business. He's lost his job but told no one, continuing his charade of morning commutes while secretly job-hunting. His savings deplete rapidly—mortgage, private schools, country club dues.

One evening, dropping off Junior at a birthday party, Johnny finds himself alone in the host's bedroom. A jewelry box sits open. Before thinking, he pockets a diamond brooch worth thousands. The theft is discovered the next day. Police interview neighbors. Johnny's wife Christina mentions how nervous Johnny's been lately.

Johnny sells the brooch but is consumed by guilt. At the next neighborhood party, everyone discusses the break-in. Johnny can barely speak. He imagines everyone knows. The husband of the woman he robbed shakes his hand warmly—they're friends, for God's sake.

Johnny begins stealing more—wallet from a coat, cash from a desk during dinner parties. He tells himself it's temporary, until he lands a new position. But each theft makes him hate himself more, hate Shady Hill more, hate the desperation that's made him violate every principle he claimed to hold.

Finally, Johnny gets a job offer—good salary, fresh start. He could simply move on. Instead, he anonymously returns money to his victims with notes: "From someone who lost his way." The responses thank the mysterious benefactor for restoring their faith in humanity. Johnny, knowing his secret, realizes he can never truly live in Shady Hill again.""",
            "price": 1.0,
        },
    ]

    def __init__(self, writer_id: str, writer_name: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None):
        """
        Initialize a baseline writer.

        Args:
            writer_id: Unique identifier for this writer
            writer_name: Human-readable name
            data_dir: Directory for storing data
            feedback_provider: Optional feedback provider (defaults to MockFeedbackProvider)
        """
        self.writer_id = writer_id
        self.writer_name = writer_name
        self.data_dir = data_dir
        self.submit_story_tool = SubmitStoryTool(data_dir, feedback_provider=feedback_provider)

    @classmethod
    def from_yaml(cls, config_path: str, data_dir: str = "data/writings", feedback_provider: Optional[FeedbackProvider] = None) -> "BaselineWriter":
        """
        Load a baseline writer from a YAML configuration file.

        Args:
            config_path: Path to the YAML config file
            data_dir: Directory for storing data
            feedback_provider: Optional feedback provider (defaults to MockFeedbackProvider)

        Returns:
            BaselineWriter instance
        """
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
            round_num: The current round number

        Returns:
            The submitted story
        """
        # If round exceeds available stories, return empty template
        if round_num > len(self.BASELINE_STORIES):
            story_data = {
                "title": f"Round {round_num} - No Story",
                "short_summary": "",
                "full_story": "",
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

        # Fallback if something goes wrong
        return StorySubmission(**story_data)

    def get_history(self):
        """Get the writer's complete history."""
        from tools.past_writings import PastWritingsTool
        past_writings_tool = PastWritingsTool(self.data_dir)
        return past_writings_tool._load_history(self.writer_id)
