'use client';

import { Finalist } from '@/types';

interface FinalistsSectionProps {
  finalists: Finalist[];
  onViewScript: (finalist: Finalist) => void;
  onExportVideo: (finalist: Finalist) => void;
}

export default function FinalistsSection({ finalists, onViewScript, onExportVideo }: FinalistsSectionProps) {
  const sortedFinalists = [...finalists].sort((a, b) => a.ranking - b.ranking);

  const getRankingBadge = (ranking: number) => {
    const badges = ['🥇', '🥈', '🥉'];
    return badges[ranking - 1] || '🏅';
  };

  return (
    <div className="mt-12 mb-8">
      <h2 className="text-3xl font-bold mb-6">Top Finalists</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {sortedFinalists.map((finalist) => (
          <div
            key={finalist.story.story_id}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border-2 hover:shadow-xl transition-shadow"
            style={{ borderColor: finalist.writer.color }}
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-4xl">{getRankingBadge(finalist.ranking)}</span>
              <div className="text-right">
                <div className="text-3xl font-bold" style={{ color: finalist.writer.color }}>
                  {finalist.story.score.composite.toFixed(0)}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">composite score</div>
              </div>
            </div>

            <h3 className="text-xl font-bold mb-2" style={{ color: finalist.writer.color }}>
              {finalist.story.title}
            </h3>

            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              by <strong>{finalist.writer.name}</strong>
            </div>

            <p className="text-sm text-gray-700 dark:text-gray-300 italic mb-4">
              {finalist.story.logline}
            </p>

            <div className="mb-4 text-xs text-gray-500 dark:text-gray-400">
              <div>Reader Alignment: {finalist.story.score.reader_alignment.toFixed(1)}</div>
              <div>Novelty: {finalist.story.score.novelty.toFixed(1)}</div>
              <div>Coherence: {finalist.story.score.coherence.toFixed(1)}</div>
            </div>

            <div className="flex flex-col gap-2">
              <button
                onClick={() => onViewScript(finalist)}
                className="w-full py-2 px-4 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors text-sm font-medium"
              >
                View Full Script
              </button>
              <button
                onClick={() => onExportVideo(finalist)}
                className="w-full py-2 px-4 rounded transition-colors text-sm font-medium text-white"
                style={{ backgroundColor: finalist.writer.color }}
              >
                Export to Video
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
