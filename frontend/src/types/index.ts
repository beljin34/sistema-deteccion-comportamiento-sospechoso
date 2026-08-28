export interface Activity {
  id: number;
  timestamp: string;
  activity_type: string;
  confidence: number;
  location: string;
  video_url: string;
  description?: string;
}

export interface AnalysisResult {
  success: boolean;
  activity: Activity;
  timestamp: string;
}

export interface ApiError {
  detail?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
