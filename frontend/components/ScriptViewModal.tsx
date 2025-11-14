'use client';

import { Finalist } from '@/types';

interface ScriptViewModalProps {
  finalist: Finalist;
  onClose: () => void;
}

export default function ScriptViewModal({ finalist, onClose }: ScriptViewModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div
          className="p-6 border-b-4"
          style={{ borderColor: finalist.writer.color }}
        >
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-3xl font-bold mb-2" style={{ color: finalist.writer.color }}>
                {finalist.story.title}
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-2">
                by <strong>{finalist.writer.name}</strong>
              </p>
              <p className="text-gray-700 dark:text-gray-300 italic">
                {finalist.story.logline}
              </p>
              <div className="mt-3 flex gap-4 text-sm">
                <span>
                  Composite Score: <strong style={{ color: finalist.writer.color }}>
                    {finalist.story.score.composite.toFixed(1)}
                  </strong>
                </span>
                <span>
                  Reader Alignment: <strong>{finalist.story.score.reader_alignment.toFixed(1)}</strong>
                </span>
                <span>
                  Novelty: <strong>{finalist.story.score.novelty.toFixed(1)}</strong>
                </span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="ml-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl"
            >
              ×
            </button>
          </div>
        </div>

        {/* Script Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
            <pre className="font-mono text-sm whitespace-pre-wrap leading-relaxed">
              {finalist.story.full_script}
            </pre>
          </div>

          {/* Reader Feedback */}
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3">Reader Feedback</h3>
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
              <p className="mb-3">{finalist.story.reader_feedback.summary}</p>
              <div className="flex flex-wrap gap-2">
                {finalist.story.reader_feedback.tags.map((tag, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
          <button
            onClick={onClose}
            className="py-2 px-6 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-lg font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
