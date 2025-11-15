'use client';

import { useState } from 'react';
import { RoundData, Writer } from '@/types';

interface StoryViewerModalProps {
  round: RoundData;
  onClose: () => void;
}

export default function StoryViewerModal({ round, onClose }: StoryViewerModalProps) {
  const [selectedStoryIndex, setSelectedStoryIndex] = useState(0);

  const story = round.stories[selectedStoryIndex];

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
                Round {round.round} Stories
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
          {/* Story Tabs - Left Sidebar */}
          <div className="w-64 border-r-4 border-black bg-white overflow-y-auto">
            <div className="p-3">
              <div className="text-xs font-bold uppercase tracking-wide mb-3 opacity-60">
                Select Story
              </div>
              {round.stories.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedStoryIndex(idx)}
                  className={`w-full text-left p-3 mb-2 border-2 border-black transition-all ${
                    selectedStoryIndex === idx
                      ? 'bg-black text-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] -translate-y-1'
                      : 'bg-white hover:bg-gray-100'
                  }`}
                >
                  <div className="font-bold text-sm truncate">{s.title}</div>
                  <div className="text-xs opacity-70 mt-1 truncate">{s.writer_id}</div>
                  <div className="mt-2 flex items-center gap-2">
                    <div className="text-xs font-mono font-bold">
                      {s.score?.composite?.toFixed(0) || 0}pts
                    </div>
                    <div className="flex-1 bg-gray-200 h-1.5 border border-black">
                      <div
                        className="bg-black h-full"
                        style={{ width: `${Math.min(100, s.score?.composite || 0)}%` }}
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
                    {story.writer_id}
                  </span>
                  <span className="opacity-60">Round {round.round}</span>
                  <span className="font-bold">Score: {story.score?.composite?.toFixed(1) || 0}/100</span>
                </div>
                {story.logline && (
                  <p className="mt-3 text-sm italic opacity-70">{story.logline}</p>
                )}
              </div>

              {/* Story Text */}
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
                      {story.score?.novelty?.toFixed(0) || 0}
                    </div>
                    <div className="text-xs">How original and creative</div>
                  </div>

                  {/* Reader Alignment Score */}
                  <div className="bg-blue-100 border-2 border-black p-4">
                    <div className="text-xs font-bold uppercase tracking-wide mb-2 opacity-60">
                      Alignment
                    </div>
                    <div className="text-3xl font-bold mb-2">
                      {story.score?.reader_alignment?.toFixed(0) || 0}
                    </div>
                    <div className="text-xs">Reader preference match</div>
                  </div>

                  {/* Coherence Score */}
                  <div className="bg-green-100 border-2 border-black p-4">
                    <div className="text-xs font-bold uppercase tracking-wide mb-2 opacity-60">
                      Coherence
                    </div>
                    <div className="text-3xl font-bold mb-2">
                      {story.score?.coherence?.toFixed(0) || 0}
                    </div>
                    <div className="text-xs">Story quality & execution</div>
                  </div>
                </div>

                {/* Detailed Feedback */}
                {story.reader_feedback?.summary && (
                  <div className="bg-white border-2 border-black p-6">
                    <div className="text-sm font-bold uppercase tracking-wide mb-4">
                      💬 Detailed Reader Analysis
                    </div>

                    <div className="space-y-4">
                      <div>
                        <div className="text-xs font-bold text-blue-600 mb-1">READER FEEDBACK</div>
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">
                          {story.reader_feedback.summary}
                        </p>
                      </div>

                      {story.reader_feedback.tags && story.reader_feedback.tags.length > 0 && (
                        <div>
                          <div className="text-xs font-bold text-purple-600 mb-2">STORY TAGS</div>
                          <div className="flex flex-wrap gap-2">
                            {story.reader_feedback.tags.map((tag, idx) => (
                              <span
                                key={idx}
                                className="px-2 py-1 bg-gray-100 border border-black text-xs font-mono"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Score Breakdown */}
                <div className="mt-6 bg-yellow-50 border-2 border-black p-4">
                  <div className="flex items-start gap-3">
                    <div className="text-2xl">📊</div>
                    <div className="flex-1">
                      <div className="text-sm font-bold mb-1">
                        Composite Score Breakdown
                      </div>
                      <div className="text-xs opacity-70 mb-3">
                        Based on {round.stories.length} competing stories in this round
                      </div>
                      <div className="grid grid-cols-4 gap-2 text-xs font-mono">
                        <div>
                          <div className="opacity-60">Novelty</div>
                          <div className="font-bold">{story.score?.novelty?.toFixed(1) || 0}</div>
                        </div>
                        <div>
                          <div className="opacity-60">Alignment</div>
                          <div className="font-bold">{story.score?.reader_alignment?.toFixed(1) || 0}</div>
                        </div>
                        <div>
                          <div className="opacity-60">Coherence</div>
                          <div className="font-bold">{story.score?.coherence?.toFixed(1) || 0}</div>
                        </div>
                        <div>
                          <div className="opacity-60">Composite</div>
                          <div className="font-bold text-lg">{story.score?.composite?.toFixed(1) || 0}</div>
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
