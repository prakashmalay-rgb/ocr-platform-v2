import { ApiClient } from "./client";
import { UnifiedResult } from "../../types/job";

export class ResultsService extends ApiClient {
  static async getResult(jobId: string): Promise<UnifiedResult> {
    const job = await this.request<any>(`/jobs/${jobId}`);
    if (job.result_json) {
      return typeof job.result_json === "string" ? JSON.parse(job.result_json) : job.result_json;
    }
    throw new Error("Results not available or job failed");
  }
}
