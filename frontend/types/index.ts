// Core data types for the Story Evolution Sandbox

export interface Score {
  reader_alignment: number;
  novelty: number;
  coherence: number;
  composite: number;
}

export interface Story {
  story_id: string;
  writer_id: string;
  round: number;
  title: string;
  logline: string;
  excerpt: string;
  full_script: string;
  score: Score;
  reader_feedback: ReaderFeedback;
}

export interface ReaderFeedback {
  summary: string;
  tags: string[];
  detailed_comments?: string;
}

export interface Writer {
  writer_id: string;
  name: string;
  description: string;
  style_dna: string;
  total_score: number;
  color: string; // For chart visualization
}

export interface RoundData {
  round: number;
  stories: Story[];
}

export interface Finalist {
  story: Story;
  writer: Writer;
  ranking: number;
}

export type MetricType = 'composite' | 'reader_alignment' | 'novelty' | 'coherence';

export interface ChartDataPoint {
  round: number;
  [key: string]: number; // writer_id -> score
}

export interface VideoBeatSheet {
  scene_number: number;
  description: string;
  characters: string[];
  emotion: string;
  visual_cues: string;
  camera_angle?: string;
  duration_seconds?: number;
}

export interface VideoBlueprint {
  story_id: string;
  title: string;
  target_length_seconds: number;
  visual_style: string;
  aspect_ratio: string;
  beat_sheet: VideoBeatSheet[];
  characters: string[];
  overall_mood: string;
  color_palette?: string;
  music_suggestion?: string;
}

export interface VideoExportRequest {
  story_id: string;
  title: string;
  script: string;
  target_length_seconds: number;
  visual_style: string;
  aspect_ratio: string;
}

export type ExportFormat = 'blueprint' | 'runway' | 'pika' | 'sora';
