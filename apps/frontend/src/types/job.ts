export enum JobStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  COMPLETED = "completed",
  FAILED = "failed",
}

export const TERMINAL_STATES = [JobStatus.COMPLETED, JobStatus.FAILED];

export interface UnifiedResult {
  version: string;
  job_id: string;
  metadata: {
    pages: number;
    ocr_engine: string;
    timestamp: string;
    processing_time_ms: number;
  };
  raw_text: string;
  structured_data: Record<string, any>;
  confidence_score: number;
}
