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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Story Evolution Sandbox
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Writer agents evolving short drama IP over rounds
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <div className="flex flex-wrap gap-6 items-center">
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Metric for Y-axis
              </label>
              <select
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value as MetricType)}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="composite">Composite Score</option>
                <option value="reader_alignment">Reader Alignment</option>
                <option value="novelty">Novelty</option>
                <option value="coherence">Coherence</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="finalistsOnly"
                checked={showFinalistsOnly}
                onChange={(e) => setShowFinalistsOnly(e.target.checked)}
                className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
              />
              <label htmlFor="finalistsOnly" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Show only finalists
              </label>
            </div>

            <div className="text-sm text-gray-500 dark:text-gray-400">
              {displayedWriters.length} writer{displayedWriters.length !== 1 ? 's' : ''} • {ROUNDS.length} rounds
            </div>
          </div>
        </div>

        {/* Chart Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">
            Evolution Trajectory
          </h2>
          <EvolutionChart
            data={chartData}
            writers={displayedWriters}
            metric={selectedMetric}
            onPointClick={handlePointClick}
          />
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-3 text-center">
            Click on any point or line to view writer details
          </p>
        </div>

        {/* Writers Legend */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">Writers</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {displayedWriters.map((writer) => (
              <button
                key={writer.writer_id}
                onClick={() => setSelectedWriter(writer)}
                className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-left border border-transparent hover:border-gray-200 dark:hover:border-gray-600"
              >
                <div
                  className="w-4 h-4 rounded-full mt-1 flex-shrink-0"
                  style={{ backgroundColor: writer.color }}
                />
                <div>
                  <div className="font-semibold text-gray-900 dark:text-gray-100">{writer.name}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">{writer.description}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                    Total: {writer.total_score}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Finalists Section */}
        <FinalistsSection
          finalists={FINALISTS}
          onViewScript={handleViewScript}
          onExportVideo={handleExportVideo}
        />

        {/* How it Works */}
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 mt-8 border border-blue-200 dark:border-blue-800">
          <h3 className="text-lg font-semibold mb-3 text-blue-900 dark:text-blue-100">
            How It Works
          </h3>
          <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
            <li>• <strong>5 Writer Agents</strong> each with unique style DNA compete over 5 rounds</li>
            <li>• <strong>Reader/Critic Agents</strong> score stories on alignment, novelty, and coherence</li>
            <li>• Writers <strong>evolve</strong> their approach based on feedback each round</li>
            <li>• Top 3 stories become <strong>finalists</strong> ready for AI video generation</li>
            <li>• Export winning scripts as <strong>structured prompts</strong> for video models like Sora</li>
          </ul>
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
