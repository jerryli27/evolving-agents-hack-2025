'use client';

import { Finalist } from '@/types';

interface ScriptViewModalProps {
  finalist: Finalist;
  onClose: () => void;
}

export default function ScriptViewModal({ finalist, onClose }: ScriptViewModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-50 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="border-b-2 border-black bg-black px-6 py-4">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold uppercase tracking-wider text-white mb-2">
                {finalist.story.title}
              </h2>
              <p className="text-white opacity-70 mb-2 font-mono text-sm">
                BY {finalist.writer.name.toUpperCase()}
              </p>
              <p className="text-white opacity-90 text-sm">
                {finalist.story.logline}
              </p>
            </div>
            <button
              onClick={onClose}
              className="ml-4 text-white hover:text-gray-300 text-2xl font-bold"
            >
              ×
            </button>
          </div>
        </div>

        {/* Scores Bar */}
        <div className="border-b-2 border-black bg-white px-6 py-3">
          <div className="flex gap-6 text-xs font-mono">
            <div>
              <span className="uppercase text-black opacity-60">COMPOSITE:</span>{' '}
              <strong className="text-black">{finalist.story.score.composite.toFixed(1)}</strong>
            </div>
            <div>
              <span className="uppercase text-black opacity-60">ALIGNMENT:</span>{' '}
              <strong className="text-black">{finalist.story.score.reader_alignment.toFixed(1)}</strong>
            </div>
            <div>
              <span className="uppercase text-black opacity-60">NOVELTY:</span>{' '}
              <strong className="text-black">{finalist.story.score.novelty.toFixed(1)}</strong>
            </div>
            <div>
              <span className="uppercase text-black opacity-60">COHERENCE:</span>{' '}
              <strong className="text-black">{finalist.story.score.coherence.toFixed(1)}</strong>
            </div>
          </div>
        </div>

        {/* Script Content */}
        <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
          <div className="bg-white border-2 border-black p-6 mb-4">
            <div className="border-b-2 border-black bg-black px-3 py-1.5 -mx-6 -mt-6 mb-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">
                Full Script
              </h3>
            </div>
            <pre className="font-mono text-sm whitespace-pre-wrap leading-relaxed text-black">
              {finalist.story.full_script}
            </pre>
          </div>

          {/* Reader Feedback */}
          <div className="bg-white border-2 border-black p-4">
            <div className="border-b-2 border-black bg-black px-3 py-1.5 -mx-4 -mt-4 mb-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">
                Reader Feedback
              </h3>
            </div>
            <p className="mb-3 text-sm text-black leading-relaxed">
              {finalist.story.reader_feedback.summary}
            </p>
            <div className="flex flex-wrap gap-2">
              {finalist.story.reader_feedback.tags.map((tag, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-black text-white text-xs font-mono uppercase tracking-wide"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t-2 border-black bg-white p-4 flex justify-end">
          <button
            onClick={onClose}
            className="py-3 px-6 bg-black text-white border-2 border-black hover:bg-gray-900 font-bold text-xs uppercase tracking-wide transition-all hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
