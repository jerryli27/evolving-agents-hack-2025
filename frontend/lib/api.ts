// API client for Story Evolution Sandbox
// This file provides functions to fetch data from the backend API
// Falls back to mock data when API is unavailable

import { Writer, RoundData, Finalist } from '@/types';
import { WRITERS, ROUNDS, FINALISTS } from './mockData';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';
const USE_MOCK_DATA = !API_URL || process.env.NEXT_PUBLIC_USE_MOCK === 'true';

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
