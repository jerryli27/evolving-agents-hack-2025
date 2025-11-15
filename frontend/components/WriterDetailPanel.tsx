'use client';

import { Story, Writer } from '@/types';
import { useState } from 'react';

interface WriterDetailPanelProps {
  writer: Writer;
  stories: Story[];
  onClose: () => void;
}

export default function WriterDetailPanel({ writer, stories, onClose }: WriterDetailPanelProps) {
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);

  const sortedStories = [...stories].sort((a, b) => a.round - b.round);

  return (
    <div className="fixed right-0 top-0 h-full w-full md:w-[600px] bg-white dark:bg-gray-900 shadow-2xl overflow-y-auto z-50 border-l border-gray-200 dark:border-gray-700">
      <div className="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 p-6 z-10">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h2 className="text-2xl font-bold mb-2" style={{ color: writer.color }}>
              {writer.name}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-2">{writer.description}</p>
            <div className="text-sm text-gray-500 dark:text-gray-500">
              <span className="font-semibold">Style DNA:</span> {writer.style_dna}
            </div>
            <div className="mt-3 text-lg font-semibold">
              Total Score: <span style={{ color: writer.color }}>{writer.total_score}</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="ml-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Mini Sparkline */}
        <div className="mt-4 flex items-end h-16 gap-1">
          {sortedStories.map((story, idx) => {
            const height = (story.score.composite / 100) * 100;
            return (
              <div
                key={idx}
                className="flex-1 rounded-t transition-all hover:opacity-70"
                style={{
                  backgroundColor: writer.color,
                  height: `${height}%`,
                  minHeight: '10%',
                }}
                title={`Round ${story.round}: ${story.score.composite.toFixed(1)}`}
              />
            );
          })}
        </div>
      </div>

      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4">Story Evolution</h3>

        {selectedStory ? (
          // Story Detail View
          <div className="mb-4">
            <button
              onClick={() => setSelectedStory(null)}
              className="text-blue-600 dark:text-blue-400 hover:underline mb-4 flex items-center gap-1"
            >
              ← Back to rounds
            </button>
            <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
              <h4 className="text-lg font-bold mb-2">{selectedStory.title}</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 italic mb-4">
                {selectedStory.logline}
              </p>

              <div className="mb-4">
                <h5 className="font-semibold mb-2">Script Excerpt:</h5>
                <div className="bg-white dark:bg-gray-900 p-4 rounded border border-gray-200 dark:border-gray-700 font-mono text-sm whitespace-pre-wrap">
                  {selectedStory.excerpt}
                </div>
              </div>

              <div className="mb-4">
                <h5 className="font-semibold mb-2">Scores:</h5>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>Composite: <strong>{selectedStory.score.composite.toFixed(1)}</strong></div>
                  <div>Reader Alignment: <strong>{selectedStory.score.reader_alignment.toFixed(1)}</strong></div>
                  <div>Novelty: <strong>{selectedStory.score.novelty.toFixed(1)}</strong></div>
                  <div>Coherence: <strong>{selectedStory.score.coherence.toFixed(1)}</strong></div>
                </div>
              </div>

              <div>
                <h5 className="font-semibold mb-2">Reader Feedback:</h5>
                <p className="text-sm mb-2">{selectedStory.reader_feedback.summary}</p>
                <div className="flex flex-wrap gap-2">
                  {selectedStory.reader_feedback.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ) : (
          // Rounds List View
          <div className="space-y-3">
            {sortedStories.map((story) => (
              <div
                key={story.story_id}
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-semibold text-gray-500 dark:text-gray-400">
                        Round {story.round}
                      </span>
                      <span className="text-lg font-bold">{story.title}</span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 italic">
                      {story.logline}
                    </p>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-2xl font-bold" style={{ color: writer.color }}>
                      {story.score.composite.toFixed(0)}
                    </div>
                    <div className="text-xs text-gray-500">score</div>
                  </div>
                </div>

                <button
                  onClick={() => setSelectedStory(story)}
                  className="mt-2 text-sm text-blue-600 dark:text-blue-400 hover:underline"
                >
                  View script excerpt →
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
