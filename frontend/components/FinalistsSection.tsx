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
    <div className="border-2 border-black bg-white mb-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div className="border-b-2 border-black bg-black px-4 py-2.5">
        <div className="text-xs md:text-sm font-bold uppercase tracking-wider text-white">TOP FINALISTS</div>
      </div>

      <div className="p-4 md:p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
          {sortedFinalists.map((finalist) => (
            <div
              key={finalist.story.story_id}
              className="border-2 border-black bg-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
            >
              <div className="p-5">
                <div className="flex items-start justify-between mb-4">
                  <div className="border-2 border-black px-4 py-2 font-bold text-xl bg-white">
                    {getRankingText(finalist.ranking)}
                  </div>
                  <div className="text-right">
                    <div className="text-4xl md:text-5xl font-bold font-mono" style={{ color: finalist.writer.color }}>
                      {finalist.story.score.composite.toFixed(0)}
                    </div>
                    <div className="text-[10px] font-mono uppercase text-black mt-1 opacity-60">SCORE</div>
                  </div>
                </div>

                <div className="border-t-2 border-black pt-4 mb-4">
                  <h3 className="text-base md:text-lg font-bold mb-2 uppercase tracking-wide text-black">
                    {finalist.story.title}
                  </h3>

                  <div className="text-xs font-mono text-black mb-3 opacity-70">
                    BY {finalist.writer.name.toUpperCase()}
                  </div>

                  <p className="text-sm text-black leading-relaxed line-clamp-3">
                    {finalist.story.logline}
                  </p>
                </div>

                <div className="border-t border-gray-300 pt-4 mb-4 text-xs font-mono text-black space-y-2">
                  <div className="flex justify-between">
                    <span className="opacity-70">ALIGNMENT:</span>
                    <span className="font-bold">{finalist.story.score.reader_alignment.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="opacity-70">NOVELTY:</span>
                    <span className="font-bold">{finalist.story.score.novelty.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="opacity-70">COHERENCE:</span>
                    <span className="font-bold">{finalist.story.score.coherence.toFixed(1)}</span>
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                  <button
                    onClick={() => onViewScript(finalist)}
                    className="w-full py-3 px-4 border-2 border-black bg-white hover:bg-gray-50 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5 transition-all text-xs font-bold uppercase tracking-wide"
                  >
                    VIEW SCRIPT
                  </button>
                  <button
                    onClick={() => onExportVideo(finalist)}
                    className="w-full py-3 px-4 border-2 border-black hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5 transition-all text-xs font-bold uppercase tracking-wide text-white"
                    style={{ backgroundColor: finalist.writer.color, borderColor: 'black' }}
                  >
                    EXPORT TO VIDEO
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
