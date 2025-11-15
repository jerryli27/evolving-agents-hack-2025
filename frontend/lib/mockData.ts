// Mock data for Story Evolution Sandbox
import { Writer, RoundData, Story, Finalist } from '@/types';

export const WRITERS: Writer[] = [
  {
    writer_id: 'writer_1',
    name: 'Melodrama Maven',
    description: 'Specializes in emotional arcs and tearjerker moments',
    style_dna: 'high-emotion, character-driven, romantic tension',
    total_score: 425,
    color: '#3B82F6', // blue
  },
  {
    writer_id: 'writer_2',
    name: 'Plot Twister',
    description: 'Master of unexpected turns and shocking reveals',
    style_dna: 'suspense, plot-heavy, twist endings',
    total_score: 458,
    color: '#EF4444', // red
  },
  {
    writer_id: 'writer_3',
    name: 'Comedy Genius',
    description: 'Light-hearted romantic comedy specialist',
    style_dna: 'witty dialogue, rom-com beats, feel-good',
    total_score: 392,
    color: '#10B981', // green
  },
  {
    writer_id: 'writer_4',
    name: 'Dark Realist',
    description: 'Gritty, realistic drama with moral complexity',
    style_dna: 'dark, psychological, morally ambiguous',
    total_score: 441,
    color: '#8B5CF6', // purple
  },
  {
    writer_id: 'writer_5',
    name: 'Fantasy Weaver',
    description: 'Magical realism and fantastical elements',
    style_dna: 'magical-realism, whimsical, dreamlike',
    total_score: 378,
    color: '#F59E0B', // amber
  },
];

const SAMPLE_SCRIPTS = {
  round_1: {
    writer_1: {
      title: 'The Last Message',
      logline: 'A woman receives mysterious texts from her deceased husband.',
      excerpt: `FADE IN:\n\nINT. APARTMENT - NIGHT\n\nSARAH (32) sits alone, staring at her phone. A notification chimes.\n\nThe message reads: "I miss you."\n\nHer hands tremble. The sender: her husband who died six months ago.`,
      full_script: `FADE IN:\n\nINT. APARTMENT - NIGHT\n\nSARAH (32) sits alone, staring at her phone. A notification chimes.\n\nThe message reads: "I miss you."\n\nHer hands tremble. The sender: her husband who died six months ago.\n\nSARAH\n(whispering)\nThis can't be real...\n\nAnother message appears: "Check the drawer."\n\nSarah walks to the bedroom, opens the nightstand drawer. Inside: a photo of them on their wedding day, with a note on the back in his handwriting.\n\n"Happy Anniversary. I knew you'd forget, so I set this up. Love always."\n\nTears stream down her face as she realizes the texts were scheduled before he died.\n\nFADE OUT.`,
    },
    writer_2: {
      title: 'The Interview',
      logline: 'A job interview takes a sinister turn when the applicant recognizes the interviewer.',
      excerpt: `INT. CORPORATE OFFICE - DAY\n\nMARK (28) enters a sleek conference room. JESSICA (35), perfectly composed, extends her hand.\n\nJESSICA\nPlease, have a seat.\n\nMark's eyes widen slightly. He knows her from somewhere.`,
      full_script: `INT. CORPORATE OFFICE - DAY\n\nMARK (28) enters a sleek conference room. JESSICA (35), perfectly composed, extends her hand.\n\nJESSICA\nPlease, have a seat.\n\nMark's eyes widen slightly. He knows her from somewhere.\n\nJESSICA (CONT'D)\nYou seem nervous. First interview?\n\nMARK\nNo, I... Have we met before?\n\nJessica smiles coldly.\n\nJESSICA\nTen years ago. You were drunk. You hit my daughter with your car.\n\nMark's face drains of color.\n\nJESSICA (CONT'D)\nShe survived. Barely. I've waited a long time for this moment.\n\nShe slides a folder across the table. Inside: photos of Mark from that night.\n\nJESSICA (CONT'D)\nNow, let's discuss your... qualifications.\n\nFADE OUT.`,
    },
    writer_3: {
      title: 'Coffee Shop Chaos',
      logline: 'Two baristas accidentally swap phones and discover they have eerily similar lives.',
      excerpt: `INT. BUSY COFFEE SHOP - MORNING\n\nALEX and JAMIE, both wearing identical green aprons, reach for their phones during break.\n\nALEX\nWait... this isn't my phone.\n\nThey look at each other, phones in hand, and burst out laughing.`,
      full_script: `INT. BUSY COFFEE SHOP - MORNING\n\nALEX and JAMIE, both wearing identical green aprons, reach for their phones during break.\n\nALEX\nWait... this isn't my phone.\n\nThey look at each other, phones in hand, and burst out laughing.\n\nJAMIE\nSame case, same crack in the corner.\n\nALEX\nSame terrible taste.\n\nThey swap phones back, but Jamie's screen lights up with a text.\n\nJAMIE\nUh... your mom just texted you about bringing a date to dinner.\n\nALEX\n(groaning)\nShe won't stop. What about you?\n\nJAMIE\n(checking phone)\nMy mom wants to know when I'm bringing someone home.\n\nThey look at each other. A beat.\n\nALEX\nAre you thinking what I'm thinking?\n\nJAMIE\nFake dating scheme to get our moms off our backs?\n\nALEX\nWant to get coffee after work and plan this out?\n\nJAMIE\n(looking around)\nWe work at a coffee shop.\n\nALEX\nRight. Want to get... not coffee?\n\nThey both laugh.\n\nFADE OUT.`,
    },
    writer_4: {
      title: 'The Confession',
      logline: 'A priest hears a confession that forces him to choose between his vows and justice.',
      excerpt: `INT. CONFESSION BOOTH - EVENING\n\nFATHER MICHAEL (50s) sits in the dimly lit booth. On the other side, a VOICE speaks.\n\nVOICE\nForgive me, Father, for I have sinned.\n\nFATHER MICHAEL\nThe Lord is listening, my child.\n\nVOICE\nI killed someone. And I'm going to do it again.`,
      full_script: `INT. CONFESSION BOOTH - EVENING\n\nFATHER MICHAEL (50s) sits in the dimly lit booth. On the other side, a VOICE speaks.\n\nVOICE\nForgive me, Father, for I have sinned.\n\nFATHER MICHAEL\nThe Lord is listening, my child.\n\nVOICE\nI killed someone. And I'm going to do it again.\n\nFather Michael stiffens.\n\nFATHER MICHAEL\nMy child, you must turn yourself in—\n\nVOICE\nBut that would break the seal of confession, wouldn't it? You can't tell anyone what I've said here.\n\nFATHER MICHAEL\n(struggling)\nIf you're planning to harm someone—\n\nVOICE\nShe deserves it. Just like the first one did.\n\nThe voice is familiar. Father Michael's eyes widen in recognition.\n\nVOICE (CONT'D)\nSee you at Sunday mass, Father.\n\nFootsteps recede. Father Michael sits frozen, torn between his sacred vows and the knowledge of an impending murder.\n\nFADE OUT.`,
    },
    writer_5: {
      title: 'The Memory Shop',
      logline: 'A mysterious shop sells memories, but each purchase comes with an unexpected cost.',
      excerpt: `INT. ANTIQUE SHOP - DAY\n\nLILY (26) enters a shop she's never noticed before. Shelves lined with glowing vials.\n\nSHOPKEEPER (ageless, ethereal)\nLooking for something specific?\n\nLILY\nWhat is this place?\n\nSHOPKEEPER\nWe sell memories. Happiness, love, adventure... what do you desire?`,
      full_script: `INT. ANTIQUE SHOP - DAY\n\nLILY (26) enters a shop she's never noticed before. Shelves lined with glowing vials.\n\nSHOPKEEPER (ageless, ethereal)\nLooking for something specific?\n\nLILY\nWhat is this place?\n\nSHOPKEEPER\nWe sell memories. Happiness, love, adventure... what do you desire?\n\nLILY\nThis is insane. Memories can't be bought.\n\nSHOPKEEPER\n(smiling)\nEverything has a price.\n\nThe Shopkeeper hands her a violet vial labeled "First Love."\n\nSHOPKEEPER (CONT'D)\nDrink this, and you'll experience falling in love for the first time again.\n\nLILY\nWhat's the cost?\n\nSHOPKEEPER\nOne memory of equal value. You choose which.\n\nLily hesitates, then drinks. Her eyes glow violet. She gasps, overwhelmed with joy.\n\nWhen she opens her eyes, the Shopkeeper is gone. So is her memory of her mother's face.\n\nLILY\n(panicking)\nNo, no, no...\n\nShe runs out. The shop vanishes behind her.\n\nFADE OUT.`,
    },
  },
  // Additional rounds would be added here with evolving stories
};

function generateStory(writerId: string, round: number): Story {
  const writer = WRITERS.find(w => w.writer_id === writerId)!;

  // Base scores that evolve over rounds
  const baseScores: Record<string, number[]> = {
    writer_1: [72, 78, 85, 82, 91],
    writer_2: [85, 89, 92, 95, 97],
    writer_3: [68, 71, 75, 79, 84],
    writer_4: [80, 84, 88, 91, 88],
    writer_5: [65, 70, 72, 76, 80],
  };

  const composite = baseScores[writerId][round - 1];

  // Deterministic variance based on writer and round (no Math.random to avoid hydration issues)
  const writerNum = parseInt(writerId.split('_')[1]);
  const variance = ((writerNum * round * 7) % 10) - 5; // Deterministic -5 to +5
  const noveltyVar = ((writerNum * round * 13) % 20) - 10; // Deterministic -10 to +10
  const coherenceVar = ((writerNum * round * 11) % 10) - 5; // Deterministic -5 to +5

  const score = {
    composite,
    reader_alignment: Math.min(100, Math.max(0, composite + variance)),
    novelty: Math.min(100, Math.max(0, composite + noveltyVar)),
    coherence: Math.min(100, Math.max(0, composite + coherenceVar)),
  };

  // Get the appropriate script content
  const scriptData = round === 1 ?
    SAMPLE_SCRIPTS.round_1[writerId as keyof typeof SAMPLE_SCRIPTS.round_1] :
    {
      title: `${writer.name} - Round ${round}`,
      logline: `Evolved story from ${writer.name} showing growth and adaptation.`,
      excerpt: `This is the evolved excerpt for round ${round}...`,
      full_script: `This is the full evolved script for round ${round}...`,
    };

  return {
    story_id: `story_${writerId}_r${round}`,
    writer_id: writerId,
    round,
    title: scriptData.title,
    logline: scriptData.logline,
    excerpt: scriptData.excerpt,
    full_script: scriptData.full_script,
    score,
    reader_feedback: generateFeedback(writer.name, round, score),
  };
}

function generateFeedback(writerName: string, round: number, score: any) {
  const feedbackTemplates = [
    {
      summary: 'Strong emotional resonance but pacing could be improved.',
      tags: ['emotional', 'pacing issues', 'character development'],
    },
    {
      summary: 'Excellent twist execution, readers were genuinely surprised.',
      tags: ['plot twist', 'suspenseful', 'engaging'],
    },
    {
      summary: 'Dialogue feels natural and characters are relatable.',
      tags: ['great dialogue', 'relatable', 'authentic'],
    },
    {
      summary: 'Dark tone works well, but ending feels rushed.',
      tags: ['atmospheric', 'rushed ending', 'compelling'],
    },
    {
      summary: 'Creative concept but needs stronger character motivation.',
      tags: ['creative', 'weak motivation', 'imaginative'],
    },
  ];

  const writerIndex = parseInt(writerName.split('_')[1] || '0') - 1;
  const feedback = feedbackTemplates[writerIndex] || feedbackTemplates[0];

  return {
    ...feedback,
    detailed_comments: `Round ${round} feedback: Score improved by ${(score.composite - 70).toFixed(1)} points. ${feedback.summary}`,
  };
}

export const ROUNDS: RoundData[] = [1, 2, 3, 4, 5].map(round => ({
  round,
  stories: WRITERS.map(writer => generateStory(writer.writer_id, round)),
}));

export const FINALISTS: Finalist[] = [
  {
    story: generateStory('writer_2', 5),
    writer: WRITERS[1],
    ranking: 1,
  },
  {
    story: generateStory('writer_4', 5),
    writer: WRITERS[3],
    ranking: 2,
  },
  {
    story: generateStory('writer_1', 5),
    writer: WRITERS[0],
    ranking: 3,
  },
];

// Helper function to transform round data into chart format
export function transformToChartData(rounds: RoundData[], metric: string): any[] {
  return rounds.map(round => {
    const dataPoint: any = { round: round.round };
    round.stories.forEach(story => {
      dataPoint[story.writer_id] = story.score[metric as keyof typeof story.score];
    });
    return dataPoint;
  });
}
