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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b-2 border-black bg-white sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 md:py-5">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight uppercase text-black">
                STORY EVOLUTION SANDBOX
              </h1>
              <p className="text-xs md:text-sm text-black mt-1 font-mono opacity-70">
                Writer agents evolving short drama IP over rounds
              </p>
            </div>
            <div className="hidden md:block text-right">
              <div className="font-mono text-xs text-black">
                <div className="font-bold">{WRITERS.length} WRITERS</div>
                <div className="opacity-70">{ROUNDS.length} ROUNDS</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 md:py-8">
        {/* Controls */}
        <div className="border-2 border-black bg-white mb-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
          <div className="border-b-2 border-black bg-black px-4 py-2.5">
            <div className="text-xs md:text-sm font-bold uppercase tracking-wider text-white">CONTROLS</div>
          </div>
          <div className="p-4 md:p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wide mb-2.5 text-black">
                  DISPLAY METRIC
                </label>
                <select
                  value={selectedMetric}
                  onChange={(e) => setSelectedMetric(e.target.value as MetricType)}
                  className="w-full p-3 border-2 border-black bg-white text-sm font-mono focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black transition-all"
                >
                  <option value="composite">COMPOSITE SCORE</option>
                  <option value="reader_alignment">READER ALIGNMENT</option>
                  <option value="novelty">NOVELTY</option>
                  <option value="coherence">COHERENCE</option>
                </select>
              </div>

              <div className="flex items-end">
                <label className="flex items-center gap-3 cursor-pointer p-3 border-2 border-black bg-white hover:bg-gray-50 transition-colors w-full">
                  <input
                    type="checkbox"
                    id="finalistsOnly"
                    checked={showFinalistsOnly}
                    onChange={(e) => setShowFinalistsOnly(e.target.checked)}
                    className="w-5 h-5 border-2 border-black accent-black"
                  />
                  <span className="text-sm font-mono font-bold text-black uppercase">
                    FINALISTS ONLY
                  </span>
                </label>
              </div>

              <div className="flex items-end">
                <div className="text-sm font-mono text-black border-2 border-black px-4 py-3 w-full bg-white">
                  <span className="font-bold">{displayedWriters.length}</span> WRITER{displayedWriters.length !== 1 ? 'S' : ''} × <span className="font-bold">{ROUNDS.length}</span> ROUNDS
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chart Section */}
        <div className="mb-6">
          <div className="border-2 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <div className="border-b-2 border-black bg-black px-4 py-2.5">
              <div className="text-xs md:text-sm font-bold uppercase tracking-wider text-white">EVOLUTION TRAJECTORY</div>
            </div>
            <EvolutionChart
              data={chartData}
              writers={displayedWriters}
              metric={selectedMetric}
              onPointClick={handlePointClick}
            />
            <div className="border-t-2 border-black px-4 py-3 bg-gray-50">
              <p className="text-xs font-mono text-center text-black">
                → Click on any point to view writer details
              </p>
            </div>
          </div>
        </div>

        {/* Writers Legend */}
        <div className="border-2 border-black bg-white mb-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
          <div className="border-b-2 border-black bg-black px-4 py-2.5">
            <div className="text-xs md:text-sm font-bold uppercase tracking-wider text-white">WRITER AGENTS</div>
          </div>
          <div className="p-4 md:p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {displayedWriters.map((writer) => (
                <button
                  key={writer.writer_id}
                  onClick={() => setSelectedWriter(writer)}
                  className="flex items-start gap-3 p-4 border-2 border-black hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5 transition-all text-left bg-white"
                >
                  <div
                    className="w-4 h-4 border-2 border-black mt-0.5 flex-shrink-0"
                    style={{ backgroundColor: writer.color }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-sm text-black uppercase tracking-wide">{writer.name}</div>
                    <div className="text-xs text-black mt-1 opacity-80 line-clamp-2">{writer.description}</div>
                    <div className="text-xs font-mono text-black mt-2 pt-2 border-t border-gray-200">
                      TOTAL SCORE: <span className="font-bold">{writer.total_score}</span>
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
        <div className="border-2 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
          <div className="border-b-2 border-black bg-black px-4 py-2.5">
            <div className="text-xs md:text-sm font-bold uppercase tracking-wider text-white">HOW IT WORKS</div>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm font-mono text-black">
              <div className="space-y-3">
                <div className="flex gap-3">
                  <span className="font-bold">01.</span>
                  <div><strong>5 WRITER AGENTS</strong> each with unique style DNA compete</div>
                </div>
                <div className="flex gap-3">
                  <span className="font-bold">02.</span>
                  <div><strong>READER/CRITIC AGENTS</strong> score on alignment, novelty, coherence</div>
                </div>
                <div className="flex gap-3">
                  <span className="font-bold">03.</span>
                  <div>Writers <strong>EVOLVE</strong> based on feedback each round</div>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex gap-3">
                  <span className="font-bold">04.</span>
                  <div>Top 3 stories selected as <strong>FINALISTS</strong></div>
                </div>
                <div className="flex gap-3">
                  <span className="font-bold">05.</span>
                  <div>Export as <strong>STRUCTURED PROMPTS</strong> for AI video models</div>
                </div>
              </div>
            </div>
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
