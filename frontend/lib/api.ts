// API client for Story Evolution Sandbox
// This file provides functions to fetch data from the backend API
// Falls back to mock data when API is unavailable

import { Writer, RoundData, Finalist } from '@/types';
import { WRITERS, ROUNDS, FINALISTS } from './mockData';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';
const USE_MOCK_DATA = !API_URL || process.env.NEXT_PUBLIC_USE_MOCK === 'true';

// Debug: Log API configuration
console.log('[API CONFIG] NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL);
console.log('[API CONFIG] API_URL:', API_URL);
console.log('[API CONFIG] USE_MOCK_DATA:', USE_MOCK_DATA);

// Helper function to handle API requests with fallback to mock data
async function fetchWithFallback<T>(
  endpoint: string,
  mockData: T,
  options?: RequestInit
): Promise<T> {
  if (USE_MOCK_DATA) {
    console.log(`[API] Using mock data for ${endpoint}`);
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300));
    return mockData;
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.warn(`[API] Failed to fetch ${endpoint}, using mock data:`, error);
    return mockData;
  }
}

/**
 * Fetch all writer agents
 */
export async function fetchWriters(): Promise<Writer[]> {
  return fetchWithFallback('/api/writers', WRITERS);
}

/**
 * Fetch all rounds data
 */
export async function fetchRounds(): Promise<RoundData[]> {
  return fetchWithFallback('/api/rounds', ROUNDS);
}

/**
 * Fetch top N finalists
 * @param n Number of finalists to fetch (default: 3)
 */
export async function fetchFinalists(n: number = 3): Promise<Finalist[]> {
  return fetchWithFallback(`/api/finalists?n=${n}`, FINALISTS);
}

/**
 * Health check for the backend API
 */
export async function checkHealth(): Promise<{ status: string; message: string }> {
  if (USE_MOCK_DATA) {
    return { status: 'mock', message: 'Using mock data' };
  }

  try {
    const response = await fetch(`${API_URL}/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (response.ok) {
      const data = await response.json();
      return { status: 'ok', message: data.message || 'API is healthy' };
    }

    return { status: 'error', message: 'API returned non-OK status' };
  } catch (error) {
    return {
      status: 'error',
      message: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Get API configuration info
 */
export function getApiConfig() {
  return {
    apiUrl: API_URL || 'none',
    useMockData: USE_MOCK_DATA,
    environment: process.env.NODE_ENV,
  };
}

/**
 * Generate video blueprint from script using AI
 * @param request Video export request with story details
 */
export async function generateVideoBlueprint(
  request: import('@/types').VideoExportRequest
): Promise<import('@/types').VideoBlueprint> {
  if (USE_MOCK_DATA) {
    console.log('[API] Using mock data for video export');
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Return mock blueprint
    return {
      story_id: request.story_id,
      title: request.title,
      target_length_seconds: request.target_length_seconds,
      visual_style: request.visual_style,
      aspect_ratio: request.aspect_ratio,
      characters: ['Character A', 'Character B'],
      overall_mood: 'dramatic',
      color_palette: 'dark blues and warm oranges',
      music_suggestion: 'tense orchestral score',
      beat_sheet: [
        {
          scene_number: 1,
          description: 'Opening scene establishes the mood',
          characters: ['Character A'],
          emotion: 'mystery',
          visual_cues: 'Dark, moody lighting. Rain on window.',
          camera_angle: 'wide shot',
          duration_seconds: 12
        },
        {
          scene_number: 2,
          description: 'Tension builds as conflict emerges',
          characters: ['Character A', 'Character B'],
          emotion: 'tension',
          visual_cues: 'Close-up on faces, dim interior lighting',
          camera_angle: 'close-up',
          duration_seconds: 18
        },
        {
          scene_number: 3,
          description: 'Climactic moment of revelation',
          characters: ['Character A', 'Character B'],
          emotion: 'dramatic',
          visual_cues: 'Sharp lighting change, dramatic reveal',
          camera_angle: 'medium shot',
          duration_seconds: 15
        }
      ]
    };
  }

  try {
    const response = await fetch(`${API_URL}/api/export-video`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Video export failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('[API] Failed to generate video blueprint:', error);
    throw error;
  }
}

/**
 * Export video blueprint in specific format (Runway, Pika, Sora)
 * @param request Video export request with format specification
 */
export async function exportVideoFormat(
  request: import('@/types').VideoExportRequest & { format: import('@/types').ExportFormat }
): Promise<any> {
  if (USE_MOCK_DATA) {
    console.log(`[API] Using mock data for ${request.format} export`);
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (request.format === 'sora') {
      return {
        prompt: `Title: ${request.title}\nDuration: ${request.target_length_seconds} seconds\nStyle: ${request.visual_style}\n\nScene Breakdown:\n\nScene 1: Opening scene...\nScene 2: Tension builds...\nScene 3: Climactic moment...`
      };
    }

    return { formatted_for: request.format, data: 'mock_export_data' };
  }

  try {
    const response = await fetch(`${API_URL}/api/export-video/format`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Format export failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`[API] Failed to export ${request.format} format:`, error);
    throw error;
  }
}
