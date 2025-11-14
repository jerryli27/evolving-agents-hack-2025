'use client';

import { useState } from 'react';
import { Finalist, VideoBlueprint, VideoBeatSheet } from '@/types';

interface ExportVideoModalProps {
  finalist: Finalist;
  onClose: () => void;
}

export default function ExportVideoModal({ finalist, onClose }: ExportVideoModalProps) {
  const [videoLength, setVideoLength] = useState<number>(60);
  const [visualStyle, setVisualStyle] = useState<string>('TikTok vertical drama');
  const [copied, setCopied] = useState<'json' | 'text' | null>(null);

  // Generate a simple beat sheet from the script
  const generateBeatSheet = (): VideoBeatSheet[] => {
    const script = finalist.story.full_script;
    const scenes = script.split('\n\n').filter(s => s.trim().length > 0);

    // Create 3-5 key beats from the script
    const numBeats = Math.min(5, Math.max(3, Math.ceil(scenes.length / 2)));
    const beatSheet: VideoBeatSheet[] = [];

    for (let i = 0; i < numBeats; i++) {
      const sceneIndex = Math.floor((i * scenes.length) / numBeats);
      const scene = scenes[sceneIndex] || scenes[0];

      // Extract simple description from scene
      const description = scene.substring(0, 100).trim() + '...';

      beatSheet.push({
        scene_number: i + 1,
        description: description.replace(/\n/g, ' '),
        characters: ['Main Character'], // Simplified
        emotion: i === 0 ? 'mysterious' : i === numBeats - 1 ? 'dramatic' : 'tense',
        visual_cues: i === 0 ? 'Dark, moody lighting' : i === numBeats - 1 ? 'Climactic reveal' : 'Medium close-up',
      });
    }

    return beatSheet;
  };

  const beatSheet = generateBeatSheet();

  const videoBlueprint: VideoBlueprint = {
    story_id: finalist.story.story_id,
    title: finalist.story.title,
    target_length_seconds: videoLength,
    visual_style: visualStyle,
    beat_sheet: beatSheet,
  };

  const handleCopyJSON = () => {
    const json = JSON.stringify(videoBlueprint, null, 2);
    navigator.clipboard.writeText(json);
    setCopied('json');
    setTimeout(() => setCopied(null), 2000);
  };

  const handleCopyText = () => {
    const textPrompt = `
VIDEO PROMPT FOR AI GENERATION
===============================

Title: ${finalist.story.title}
Duration: ${videoLength} seconds
Visual Style: ${visualStyle}

STORY LOGLINE:
${finalist.story.logline}

BEAT SHEET:
${beatSheet.map(beat => `
Scene ${beat.scene_number}:
- Description: ${beat.description}
- Characters: ${beat.characters.join(', ')}
- Emotion: ${beat.emotion}
- Visual: ${beat.visual_cues}
`).join('\n')}

FULL SCRIPT:
${finalist.story.full_script}
    `.trim();

    navigator.clipboard.writeText(textPrompt);
    setCopied('text');
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold mb-2">Export to Video</h2>
            <p className="text-gray-600 dark:text-gray-400">
              {finalist.story.title} by {finalist.writer.name}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left: Script */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Full Script</h3>
              <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg h-[500px] overflow-y-auto border border-gray-200 dark:border-gray-700">
                <pre className="font-mono text-sm whitespace-pre-wrap">
                  {finalist.story.full_script}
                </pre>
              </div>
            </div>

            {/* Right: Video Blueprint */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Video Blueprint</h3>

              <div className="space-y-4 mb-4">
                {/* Controls */}
                <div>
                  <label className="block text-sm font-medium mb-1">Target Length</label>
                  <select
                    value={videoLength}
                    onChange={(e) => setVideoLength(Number(e.target.value))}
                    className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800"
                  >
                    <option value={30}>30 seconds</option>
                    <option value={60}>60 seconds</option>
                    <option value={90}>90 seconds</option>
                    <option value={120}>120 seconds</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Visual Style</label>
                  <select
                    value={visualStyle}
                    onChange={(e) => setVisualStyle(e.target.value)}
                    className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800"
                  >
                    <option>TikTok vertical drama</option>
                    <option>Cinematic widescreen</option>
                    <option>Film noir aesthetic</option>
                    <option>Romantic soft lighting</option>
                    <option>Sci-fi futuristic</option>
                    <option>Documentary realism</option>
                  </select>
                </div>
              </div>

              {/* Beat Sheet */}
              <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 max-h-[350px] overflow-y-auto">
                <h4 className="font-semibold mb-3">Auto-generated Beat Sheet</h4>
                <div className="space-y-3">
                  {beatSheet.map((beat) => (
                    <div
                      key={beat.scene_number}
                      className="bg-white dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-700"
                    >
                      <div className="font-semibold mb-1">Scene {beat.scene_number}</div>
                      <div className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                        {beat.description}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
                        <div>
                          <strong>Characters:</strong> {beat.characters.join(', ')}
                        </div>
                        <div>
                          <strong>Emotion:</strong> {beat.emotion}
                        </div>
                        <div>
                          <strong>Visual:</strong> {beat.visual_cues}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700 flex gap-3">
          <button
            onClick={handleCopyJSON}
            className="flex-1 py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            {copied === 'json' ? '✓ Copied!' : 'Copy JSON for Video Model'}
          </button>
          <button
            onClick={handleCopyText}
            className="flex-1 py-3 px-6 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
          >
            {copied === 'text' ? '✓ Copied!' : 'Copy Text Prompt'}
          </button>
          <button
            onClick={onClose}
            className="py-3 px-6 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-lg font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
