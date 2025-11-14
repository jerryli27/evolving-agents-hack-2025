'use client';

import { useState, useEffect } from 'react';
import { Finalist, VideoBlueprint, ExportFormat } from '@/types';
import { generateVideoBlueprint, exportVideoFormat } from '@/lib/api';

interface ExportVideoModalProps {
  finalist: Finalist;
  onClose: () => void;
}

export default function ExportVideoModal({ finalist, onClose }: ExportVideoModalProps) {
  const [videoLength, setVideoLength] = useState<number>(60);
  const [visualStyle, setVisualStyle] = useState<string>('TikTok vertical drama');
  const [aspectRatio, setAspectRatio] = useState<string>('9:16');
  const [blueprint, setBlueprint] = useState<VideoBlueprint | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState<string | null>(null);
  const [exportFormat, setExportFormat] = useState<ExportFormat>('blueprint');

  // Generate blueprint on mount or when settings change
  useEffect(() => {
    generateBlueprint();
  }, [videoLength, visualStyle, aspectRatio]);

  const generateBlueprint = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await generateVideoBlueprint({
        story_id: finalist.story.story_id,
        title: finalist.story.title,
        script: finalist.story.full_script,
        target_length_seconds: videoLength,
        visual_style: visualStyle,
        aspect_ratio: aspectRatio,
      });

      setBlueprint(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate video blueprint');
      console.error('Blueprint generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (!blueprint) return;
    const json = JSON.stringify(blueprint, null, 2);
    navigator.clipboard.writeText(json);
    setCopied('json');
    setTimeout(() => setCopied(null), 2000);
  };

  const handleCopyFormat = async (format: ExportFormat) => {
    if (!blueprint) return;

    try {
      const result = await exportVideoFormat({
        story_id: finalist.story.story_id,
        title: finalist.story.title,
        script: finalist.story.full_script,
        target_length_seconds: videoLength,
        visual_style: visualStyle,
        aspect_ratio: aspectRatio,
        format: format,
      });

      const textToCopy = format === 'sora'
        ? result.prompt
        : JSON.stringify(result, null, 2);

      navigator.clipboard.writeText(textToCopy);
      setCopied(format);
      setTimeout(() => setCopied(null), 2000);
    } catch (err) {
      console.error(`Error exporting ${format} format:`, err);
    }
  };

  const visualStyles = [
    'TikTok vertical drama',
    'Cinematic widescreen',
    'Film noir aesthetic',
    'Romantic soft lighting',
    'Sci-fi futuristic',
    'Documentary realism',
    'Anime style',
    'Horror atmosphere',
  ];

  const aspectRatios = [
    { value: '9:16', label: '9:16 (TikTok/Reels)' },
    { value: '16:9', label: '16:9 (YouTube/Landscape)' },
    { value: '1:1', label: '1:1 (Square)' },
    { value: '4:5', label: '4:5 (Instagram)' },
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-50 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="border-b-2 border-black bg-black px-6 py-3 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-bold uppercase tracking-wider text-white">
              AI Video Export
            </h2>
            <p className="text-xs text-white opacity-70 font-mono">
              {finalist.story.title} by {finalist.writer.name}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-300 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column: Controls */}
            <div className="space-y-4">
              <div className="bg-white border-2 border-black p-4">
                <h3 className="text-sm font-bold uppercase tracking-wide mb-4 text-black">
                  Settings
                </h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wide mb-2 text-black">
                      Duration
                    </label>
                    <select
                      value={videoLength}
                      onChange={(e) => setVideoLength(Number(e.target.value))}
                      className="w-full p-2 border-2 border-black font-mono text-sm"
                      disabled={loading}
                    >
                      <option value={30}>30 seconds</option>
                      <option value={60}>60 seconds</option>
                      <option value={90}>90 seconds</option>
                      <option value={120}>2 minutes</option>
                      <option value={180}>3 minutes</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wide mb-2 text-black">
                      Visual Style
                    </label>
                    <select
                      value={visualStyle}
                      onChange={(e) => setVisualStyle(e.target.value)}
                      className="w-full p-2 border-2 border-black font-mono text-sm"
                      disabled={loading}
                    >
                      {visualStyles.map(style => (
                        <option key={style} value={style}>{style}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wide mb-2 text-black">
                      Aspect Ratio
                    </label>
                    <select
                      value={aspectRatio}
                      onChange={(e) => setAspectRatio(e.target.value)}
                      className="w-full p-2 border-2 border-black font-mono text-sm"
                      disabled={loading}
                    >
                      {aspectRatios.map(ar => (
                        <option key={ar.value} value={ar.value}>{ar.label}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* Blueprint Metadata */}
              {blueprint && !loading && (
                <div className="bg-white border-2 border-black p-4">
                  <h3 className="text-sm font-bold uppercase tracking-wide mb-3 text-black">
                    AI Analysis
                  </h3>
                  <div className="space-y-3 text-sm font-mono">
                    <div>
                      <div className="text-xs uppercase text-black opacity-60 mb-1">Characters</div>
                      <div className="text-black">{blueprint.characters.join(', ')}</div>
                    </div>
                    <div>
                      <div className="text-xs uppercase text-black opacity-60 mb-1">Overall Mood</div>
                      <div className="text-black">{blueprint.overall_mood}</div>
                    </div>
                    {blueprint.color_palette && (
                      <div>
                        <div className="text-xs uppercase text-black opacity-60 mb-1">Color Palette</div>
                        <div className="text-black">{blueprint.color_palette}</div>
                      </div>
                    )}
                    {blueprint.music_suggestion && (
                      <div>
                        <div className="text-xs uppercase text-black opacity-60 mb-1">Music</div>
                        <div className="text-black">{blueprint.music_suggestion}</div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Middle Column: Beat Sheet */}
            <div className="lg:col-span-2">
              {loading && (
                <div className="bg-white border-2 border-black p-8 text-center">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-black border-t-transparent mb-4"></div>
                  <div className="text-sm font-mono text-black">Generating AI-powered beat sheet...</div>
                </div>
              )}

              {error && (
                <div className="bg-white border-2 border-black p-4 text-red-600 text-sm font-mono">
                  Error: {error}
                </div>
              )}

              {blueprint && !loading && (
                <div className="bg-white border-2 border-black">
                  <div className="border-b-2 border-black bg-black px-4 py-2">
                    <h3 className="text-sm font-bold uppercase tracking-wide text-white">
                      Beat Sheet ({blueprint.beat_sheet.length} scenes)
                    </h3>
                  </div>

                  <div className="p-4 max-h-[500px] overflow-y-auto space-y-3">
                    {blueprint.beat_sheet.map((beat) => (
                      <div
                        key={beat.scene_number}
                        className="border-2 border-black p-3 bg-gray-50"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="font-bold text-sm text-black">
                            SCENE {beat.scene_number}
                            {beat.duration_seconds && (
                              <span className="ml-2 text-xs opacity-60">
                                ({beat.duration_seconds}s)
                              </span>
                            )}
                          </div>
                          <div className="text-xs px-2 py-1 bg-black text-white font-mono uppercase">
                            {beat.emotion}
                          </div>
                        </div>

                        <div className="text-sm text-black mb-3 leading-relaxed">
                          {beat.description}
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                          <div>
                            <div className="uppercase text-black opacity-60 mb-1">Characters</div>
                            <div className="text-black">{beat.characters.join(', ')}</div>
                          </div>
                          {beat.camera_angle && (
                            <div>
                              <div className="uppercase text-black opacity-60 mb-1">Camera</div>
                              <div className="text-black">{beat.camera_angle}</div>
                            </div>
                          )}
                        </div>

                        <div className="mt-2 text-xs">
                          <div className="uppercase text-black opacity-60 mb-1">Visual Direction</div>
                          <div className="text-black font-mono">{beat.visual_cues}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer - Export Actions */}
        <div className="border-t-2 border-black bg-white p-4">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleCopyJSON}
              disabled={!blueprint || loading}
              className="flex-1 min-w-[150px] py-3 px-4 bg-black text-white border-2 border-black hover:bg-gray-900 disabled:opacity-50 disabled:cursor-not-allowed font-bold text-xs uppercase tracking-wide transition-all hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5"
            >
              {copied === 'json' ? '✓ COPIED!' : '📋 JSON'}
            </button>

            <button
              onClick={() => handleCopyFormat('runway')}
              disabled={!blueprint || loading}
              className="flex-1 min-w-[150px] py-3 px-4 bg-white text-black border-2 border-black hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-bold text-xs uppercase tracking-wide transition-all hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5"
            >
              {copied === 'runway' ? '✓ COPIED!' : '🎬 RUNWAY'}
            </button>

            <button
              onClick={() => handleCopyFormat('pika')}
              disabled={!blueprint || loading}
              className="flex-1 min-w-[150px] py-3 px-4 bg-white text-black border-2 border-black hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-bold text-xs uppercase tracking-wide transition-all hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5"
            >
              {copied === 'pika' ? '✓ COPIED!' : '⚡ PIKA'}
            </button>

            <button
              onClick={() => handleCopyFormat('sora')}
              disabled={!blueprint || loading}
              className="flex-1 min-w-[150px] py-3 px-4 bg-white text-black border-2 border-black hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-bold text-xs uppercase tracking-wide transition-all hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5"
            >
              {copied === 'sora' ? '✓ COPIED!' : '🎥 SORA'}
            </button>
          </div>

          <div className="mt-3 text-xs text-black opacity-60 text-center font-mono">
            Beat sheet generated by Claude AI • Export to your preferred video platform
          </div>
        </div>
      </div>
    </div>
  );
}
