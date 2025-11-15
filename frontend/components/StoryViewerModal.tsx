'use client';

import { useState } from 'react';
import { RoundData } from '@/types';

interface StoryViewerModalProps {
  round: RoundData;
  onClose: () => void;
}

export default function StoryViewerModal({ round, onClose }: StoryViewerModalProps) {
  const [selectedWriter, setSelectedWriter] = useState(0);

  const story = round.stories[selectedWriter];

  // Split story into paragraphs for easier reading
  const paragraphs = story.full_script.split('\n\n').filter(p => p.trim());

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-50 border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="border-b-4 border-black bg-black px-6 py-4">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold uppercase tracking-wider text-white mb-1">
                Round {round.round_number} Stories
              </h2>
              <p className="text-sm text-white opacity-70 font-mono">
                {round.stories.length} writers competing • AI-generated feedback
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-300 text-3xl font-bold leading-none"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden flex">
          {/* Writer Tabs - Left Sidebar */}
          <div className="w-64 border-r-4 border-black bg-white overflow-y-auto">
            <div className="p-3">
              <div className="text-xs font-bold uppercase tracking-wide mb-3 opacity-60">
                Select Writer
              </div>
              {round.stories.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedWriter(idx)}
                  className={`w-full text-left p-3 mb-2 border-2 border-black transition-all ${
                    selectedWriter === idx
                      ? 'bg-black text-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] -translate-y-1'
                      : 'bg-white hover:bg-gray-100'
                  }`}
                >
                  <div className="font-bold text-sm truncate">{s.writer_name}</div>
                  <div className="text-xs opacity-70 mt-1">{s.title}</div>
                  <div className="mt-2 flex items-center gap-2">
                    <div className="text-xs font-mono font-bold">
                      {(s.total_score * 100).toFixed(0)}pts
                    </div>
                    <div className="flex-1 bg-gray-200 h-1.5 border border-black">
                      <div
                        className="bg-black h-full"
                        style={{ width: `${s.total_score * 100}%` }}
                      />
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Story Content - Main Area */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-6">
              {/* Story Header */}
              <div className="mb-6 pb-6 border-b-2 border-black">
                <h3 className="text-3xl font-bold mb-2">{story.title}</h3>
                <div className="flex items-center gap-4 text-sm font-mono">
                  <span className="px-3 py-1 bg-black text-white">
                    {story.writer_name}
                  </span>
                  <span className="opacity-60">Round {round.round_number}</span>
                  <span className="font-bold">Score: {(story.total_score * 100).toFixed(1)}/100</span>
                </div>
              </div>

              {/* Story Text with Inline Feedback */}
              <div className="mb-8">
                <div className="text-sm font-bold uppercase tracking-wide mb-4 opacity-60">
                  Story
                </div>
                <div className="space-y-4">
                  {paragraphs.map((para, idx) => (
                    <div key={idx} className="group relative">
                      <p className="text-base leading-relaxed text-gray-800 bg-white border-2 border-black p-4">
                        {para}
                      </p>
                      {/* Show feedback hints on hover */}
                      {idx === 0 && (
                        <div className="absolute -right-2 -top-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <div className="bg-yellow-300 border-2 border-black px-2 py-1 text-xs font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                            💭 Opening
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Reader Feedback Section */}
              <div className="border-t-4 border-black pt-6">
                <h4 className="text-xl font-bold uppercase tracking-wide mb-4">
                  🤖 Reader Agent Feedback
                </h4>

                <div className="grid grid-cols-3 gap-4 mb-6">
                  {/* Novelty Score */}
                  <div className="bg-purple-100 border-2 border-black p-4">
                    <div className="text-xs font-bold uppercase tracking-wide mb-2 opacity-60">
                      Novelty
                    </div>
                    <div className="text-3xl font-bold mb-2">
                      {(story.novelty_score * 100).toFixed(0)}
                    </div>
                    <div className="text-xs">How original and creative</div>
                  </div>

                  {/* Relevance Score */}
                  <div className="bg-blue-100 border-2 border-black p-4">
                    <div className="text-xs font-bold uppercase tracking-wide mb-2 opacity-60">
                      Relevance
                    </div>
                    <div className="text-3xl font-bold mb-2">
                      {(story.relevance_score * 100).toFixed(0)}
                    </div>
                    <div className="text-xs">Story coherence & focus</div>
                  </div>

                  {/* Quality Score */}
                  <div className="bg-green-100 border-2 border-black p-4">
                    <div className="text-xs font-bold uppercase tracking-wide mb-2 opacity-60">
                      Quality
                    </div>
                    <div className="text-3xl font-bold mb-2">
                      {(story.quality_score * 100).toFixed(0)}
                    </div>
                    <div className="text-xs">Writing & execution</div>
                  </div>
                </div>

                {/* Detailed Feedback */}
                <div className="bg-white border-2 border-black p-6">
                  <div className="text-sm font-bold uppercase tracking-wide mb-4">
                    💬 Detailed Reader Analysis
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="text-xs font-bold text-purple-600 mb-1">NOVELTY FEEDBACK</div>
                      <p className="text-sm leading-relaxed">
                        {story.novelty_score >= 0.7
                          ? `Exceptional creativity! The story introduces fresh perspectives and unique narrative choices that stand out from typical genre conventions.`
                          : story.novelty_score >= 0.5
                          ? `Good originality with some fresh ideas, though certain elements feel familiar. Consider pushing creative boundaries further.`
                          : `The narrative follows conventional patterns. Readers would benefit from more unexpected twists and unique character development.`
                        }
                      </p>
                    </div>

                    <div>
                      <div className="text-xs font-bold text-blue-600 mb-1">RELEVANCE FEEDBACK</div>
                      <p className="text-sm leading-relaxed">
                        {story.relevance_score >= 0.7
                          ? `Excellent coherence! Every element serves the narrative. The story maintains strong thematic focus throughout.`
                          : story.relevance_score >= 0.5
                          ? `Generally coherent with some tangential elements. Tightening the narrative focus could enhance impact.`
                          : `Some sections drift from the central narrative. Recommend refocusing on core story elements and removing distractions.`
                        }
                      </p>
                    </div>

                    <div>
                      <div className="text-xs font-bold text-green-600 mb-1">QUALITY FEEDBACK</div>
                      <p className="text-sm leading-relaxed">
                        {story.quality_score >= 0.7
                          ? `Outstanding execution! Strong prose, well-developed characters, and compelling pacing create an engaging reading experience.`
                          : story.quality_score >= 0.5
                          ? `Solid writing with room for polish. Character development and pacing are adequate but could be enhanced.`
                          : `Technical execution needs improvement. Focus on character depth, pacing, and prose quality in revision.`
                        }
                      </p>
                    </div>
                  </div>
                </div>

                {/* Reader Market Simulation */}
                <div className="mt-6 bg-yellow-50 border-2 border-black p-4">
                  <div className="flex items-start gap-3">
                    <div className="text-2xl">📊</div>
                    <div className="flex-1">
                      <div className="text-sm font-bold mb-1">
                        Predicted Market Performance
                      </div>
                      <div className="text-xs opacity-70 mb-3">
                        Based on {round.stories.length} reader agents simulating diverse preferences
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="text-lg font-bold font-mono">
                          {(story.sold_percentage * 100).toFixed(1)}%
                        </div>
                        <div className="text-xs">
                          of simulated readers would purchase this story
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t-4 border-black bg-white px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="text-xs opacity-60 font-mono">
              Story generated by AI writer agent • Feedback from AI reader agents
            </div>
            <button
              onClick={onClose}
              className="px-6 py-2 bg-black text-white border-2 border-black hover:bg-gray-900 font-bold text-sm uppercase"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
