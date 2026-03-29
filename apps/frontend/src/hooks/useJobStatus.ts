import { useState, useEffect, useCallback } from "react";
import { JobStatus, TERMINAL_STATES } from "../types/job";
import { JobsService, JobResponse } from "../services/api-client/jobs";

export function useJobStatus(jobId: string | null, intervalMs: number = 3000) {
  const [job, setJob] = useState<JobResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const poll = useCallback(async () => {
    if (!jobId) return;

    try {
      const response = await JobsService.getJobStatus(jobId);
      setJob(response);

      if (TERMINAL_STATES.includes(response.status)) {
        return; // stop polling
      }
    } catch (err: any) {
      setError(err.message);
    }
  }, [jobId]);

  useEffect(() => {
    if (!jobId) return;
    
    poll(); // Initial check

    const timer = setInterval(() => {
      if (job && TERMINAL_STATES.includes(job.status)) {
        clearInterval(timer);
        return;
      }
      poll();
    }, intervalMs);

    return () => clearInterval(timer);
  }, [jobId, poll, intervalMs, job]);

  return { job, error };
}
