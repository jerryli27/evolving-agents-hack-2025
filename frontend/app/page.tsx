'use client';

import { useState, useMemo } from 'react';
import EvolutionChart from '@/components/EvolutionChart';
import WriterDetailPanel from '@/components/WriterDetailPanel';
import FinalistsSection from '@/components/FinalistsSection';
import ExportVideoModal from '@/components/ExportVideoModal';
import ScriptViewModal from '@/components/ScriptViewModal';
import { WRITERS, ROUNDS, FINALISTS, transformToChartData } from '@/lib/mockData';
import { Writer, Story, Finalist, MetricType } from '@/types';

export default function Home() {
  const [selectedMetric, setSelectedMetric] = useState<MetricType>('composite');
  const [showFinalistsOnly, setShowFinalistsOnly] = useState(false);
  const [selectedWriter, setSelectedWriter] = useState<Writer | null>(null);
  const [exportingFinalist, setExportingFinalist] = useState<Finalist | null>(null);
  const [viewingScript, setViewingScript] = useState<Finalist | null>(null);

  // Filter writers if showing finalists only
  const displayedWriters = useMemo(() => {
    if (showFinalistsOnly) {
      const finalistWriterIds = new Set(FINALISTS.map(f => f.writer.writer_id));
      return WRITERS.filter(w => finalistWriterIds.has(w.writer_id));
    }
    return WRITERS;
  }, [showFinalistsOnly]);

  // Transform data for chart
  const chartData = useMemo(() => {
    return transformToChartData(ROUNDS, selectedMetric);
  }, [selectedMetric]);

  // Get stories for selected writer
  const selectedWriterStories = useMemo(() => {
    if (!selectedWriter) return [];
    return ROUNDS.flatMap(round =>
      round.stories.filter(story => story.writer_id === selectedWriter.writer_id)
    );
  }, [selectedWriter]);

  const handlePointClick = (writerId: string, round: number) => {
    const writer = WRITERS.find(w => w.writer_id === writerId);
    if (writer) {
      setSelectedWriter(writer);
    }
  };

  const handleExportVideo = (finalist: Finalist) => {
    setExportingFinalist(finalist);
  };

  const handleViewScript = (finalist: Finalist) => {
    setViewingScript(finalist);
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b-2 border-black bg-white sticky top-0 z-40">
        <div className="max-w-[95vw] mx-auto px-4 py-3 md:py-4">
          <h1 className="text-xl md:text-2xl font-bold tracking-tight uppercase text-black">
            STORY EVOLUTION SANDBOX
          </h1>
          <p className="text-[10px] md:text-xs text-gray-700 mt-1 font-mono">
            Writer agents evolving short drama IP over rounds
          </p>
        </div>
      </header>

      <main className="max-w-[95vw] mx-auto px-2 md:px-4 py-4 md:py-6">
        {/* Controls */}
        <div className="border-2 border-black bg-white mb-4">
          <div className="border-b-2 border-black bg-gray-50 px-3 py-2">
            <div className="text-[10px] md:text-xs font-bold uppercase tracking-wider">CONTROLS</div>
          </div>
          <div className="p-3 md:p-4">
            <div className="flex flex-col md:flex-row gap-4 md:gap-6">
              <div className="flex-1">
                <label className="block text-[10px] md:text-xs font-bold uppercase tracking-wide mb-2 text-gray-700">
                  METRIC
                </label>
                <select
                  value={selectedMetric}
                  onChange={(e) => setSelectedMetric(e.target.value as MetricType)}
                  className="w-full p-2 border-2 border-black bg-white text-sm font-mono focus:outline-none focus:ring-2 focus:ring-black"
                >
                  <option value="composite">COMPOSITE SCORE</option>
                  <option value="reader_alignment">READER ALIGNMENT</option>
                  <option value="novelty">NOVELTY</option>
                  <option value="coherence">COHERENCE</option>
                </select>
              </div>

              <div className="flex items-end gap-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    id="finalistsOnly"
                    checked={showFinalistsOnly}
                    onChange={(e) => setShowFinalistsOnly(e.target.checked)}
                    className="w-4 h-4 border-2 border-black"
                  />
                  <span className="text-xs md:text-sm font-mono text-black">
                    FINALISTS ONLY
                  </span>
                </label>
              </div>

              <div className="flex items-end">
                <div className="text-xs font-mono text-gray-600 border border-gray-300 px-2 py-1">
                  {displayedWriters.length} WRITER{displayedWriters.length !== 1 ? 'S' : ''} | {ROUNDS.length} ROUNDS
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chart Section */}
        <div className="mb-4">
          <div className="border-2 border-black bg-white">
            <div className="border-b-2 border-black bg-gray-50 px-3 py-2">
              <div className="text-[10px] md:text-xs font-bold uppercase tracking-wider">EVOLUTION TRAJECTORY</div>
            </div>
            <EvolutionChart
              data={chartData}
              writers={displayedWriters}
              metric={selectedMetric}
              onPointClick={handlePointClick}
            />
            <div className="border-t-2 border-black px-3 py-2 bg-gray-50">
              <p className="text-[10px] md:text-xs font-mono text-center text-gray-600">
                Click on any point to view writer details
              </p>
            </div>
          </div>
        </div>

        {/* Writers Legend */}
        <div className="border-2 border-black bg-white mb-4">
          <div className="border-b-2 border-black bg-gray-50 px-3 py-2">
            <div className="text-[10px] md:text-xs font-bold uppercase tracking-wider">WRITERS</div>
          </div>
          <div className="p-3 md:p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {displayedWriters.map((writer) => (
                <button
                  key={writer.writer_id}
                  onClick={() => setSelectedWriter(writer)}
                  className="flex items-start gap-3 p-3 border-2 border-black hover:bg-gray-50 transition-colors text-left"
                >
                  <div
                    className="w-3 h-3 border border-black mt-1 flex-shrink-0"
                    style={{ backgroundColor: writer.color }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-sm text-black uppercase tracking-wide truncate">{writer.name}</div>
                    <div className="text-xs text-gray-700 mt-0.5 line-clamp-2">{writer.description}</div>
                    <div className="text-[10px] font-mono text-gray-500 mt-1">
                      TOTAL: {writer.total_score}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Finalists Section */}
        <FinalistsSection
          finalists={FINALISTS}
          onViewScript={handleViewScript}
          onExportVideo={handleExportVideo}
        />

        {/* How it Works */}
        <div className="border-2 border-black bg-white mt-4">
          <div className="border-b-2 border-black bg-gray-50 px-3 py-2">
            <div className="text-[10px] md:text-xs font-bold uppercase tracking-wider">HOW IT WORKS</div>
          </div>
          <div className="p-4">
            <ul className="space-y-2 text-xs md:text-sm font-mono text-gray-800">
              <li>→ <strong>5 WRITER AGENTS</strong> each with unique style DNA compete over 5 rounds</li>
              <li>→ <strong>READER/CRITIC AGENTS</strong> score stories on alignment, novelty, and coherence</li>
              <li>→ Writers <strong>EVOLVE</strong> their approach based on feedback each round</li>
              <li>→ Top 3 stories become <strong>FINALISTS</strong> ready for AI video generation</li>
              <li>→ Export winning scripts as <strong>STRUCTURED PROMPTS</strong> for video models</li>
            </ul>
          </div>
        </div>
      </main>

      {/* Modals */}
      {selectedWriter && (
        <WriterDetailPanel
          writer={selectedWriter}
          stories={selectedWriterStories}
          onClose={() => setSelectedWriter(null)}
        />
      )}

      {exportingFinalist && (
        <ExportVideoModal
          finalist={exportingFinalist}
          onClose={() => setExportingFinalist(null)}
        />
      )}

      {viewingScript && (
        <ScriptViewModal
          finalist={viewingScript}
          onClose={() => setViewingScript(null)}
        />
      )}
    </div>
  );
}
