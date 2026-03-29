import { ApiClient } from "./client";
import { JobStatus } from "../../types/job";

export interface JobResponse {
  id: string;
  status: JobStatus;
  filename?: string;
}

export class JobsService extends ApiClient {
  static async createJob(uploadId: number): Promise<JobResponse> {
    return this.request<JobResponse>("/jobs/", {
      method: "POST",
      body: JSON.stringify({ upload_id: uploadId }),
    });
  }

  static async getJobStatus(jobId: string): Promise<JobResponse> {
    return this.request<JobResponse>(`/jobs/${jobId}`);
  }
}
