'use client';

import { Finalist } from '@/types';

interface FinalistsSectionProps {
  finalists: Finalist[];
  onViewScript: (finalist: Finalist) => void;
  onExportVideo: (finalist: Finalist) => void;
}

export default function FinalistsSection({ finalists, onViewScript, onExportVideo }: FinalistsSectionProps) {
  const sortedFinalists = [...finalists].sort((a, b) => a.ranking - b.ranking);

  const getRankingText = (ranking: number) => {
    return ['#1', '#2', '#3'][ranking - 1] || `#${ranking}`;
  };

  return (
    <div className="border-2 border-black bg-white mb-4">
      <div className="border-b-2 border-black bg-gray-50 px-3 py-2">
        <div className="text-[10px] md:text-xs font-bold uppercase tracking-wider">TOP FINALISTS</div>
      </div>

      <div className="p-3 md:p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {sortedFinalists.map((finalist) => (
            <div
              key={finalist.story.story_id}
              className="border-2 border-black bg-white p-4"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="border-2 border-black px-3 py-1 font-bold text-lg">
                  {getRankingText(finalist.ranking)}
                </div>
                <div className="text-right">
                  <div className="text-3xl md:text-4xl font-bold font-mono" style={{ color: finalist.writer.color }}>
                    {finalist.story.score.composite.toFixed(0)}
                  </div>
                  <div className="text-[10px] font-mono uppercase text-gray-600">SCORE</div>
                </div>
              </div>

              <div className="border-t-2 border-black pt-3 mb-3">
                <h3 className="text-sm md:text-base font-bold mb-1 uppercase tracking-wide">
                  {finalist.story.title}
                </h3>

                <div className="text-[10px] font-mono text-gray-600 mb-2">
                  BY {finalist.writer.name.toUpperCase()}
                </div>

                <p className="text-xs text-gray-800 mb-3 line-clamp-3">
                  {finalist.story.logline}
                </p>
              </div>

              <div className="border-t border-gray-300 pt-3 mb-3 text-[10px] font-mono text-gray-700 space-y-1">
                <div className="flex justify-between">
                  <span>ALIGNMENT:</span>
                  <span className="font-bold">{finalist.story.score.reader_alignment.toFixed(1)}</span>
                </div>
                <div className="flex justify-between">
                  <span>NOVELTY:</span>
                  <span className="font-bold">{finalist.story.score.novelty.toFixed(1)}</span>
                </div>
                <div className="flex justify-between">
                  <span>COHERENCE:</span>
                  <span className="font-bold">{finalist.story.score.coherence.toFixed(1)}</span>
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <button
                  onClick={() => onViewScript(finalist)}
                  className="w-full py-2 px-4 border-2 border-black bg-white hover:bg-gray-50 transition-colors text-xs font-bold uppercase tracking-wide"
                >
                  VIEW SCRIPT
                </button>
                <button
                  onClick={() => onExportVideo(finalist)}
                  className="w-full py-2 px-4 border-2 border-black transition-colors text-xs font-bold uppercase tracking-wide text-white"
                  style={{ backgroundColor: finalist.writer.color, borderColor: finalist.writer.color }}
                >
                  EXPORT TO VIDEO
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
