"use client";

import { JobResponse } from "../../../services/api-client/jobs";
import { JobStatus } from "../../../types/job";

interface JobStatusTrackerProps {
  job: JobResponse | null;
  error: string | null;
}

export function JobStatusTracker({ job, error }: JobStatusTrackerProps) {
  if (error) return <div className="p-4 bg-red-50 text-red-600 rounded">Error: {error}</div>;
  if (!job) return null;

  const getStatusColor = (status: JobStatus) => {
    switch (status) {
      case JobStatus.PENDING: return "bg-gray-100 text-gray-800";
      case JobStatus.PROCESSING: return "bg-blue-100 text-blue-800 animate-pulse";
      case JobStatus.COMPLETED: return "bg-green-100 text-green-800";
      case JobStatus.FAILED: return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="p-6 border rounded-lg bg-white shadow-sm mt-6">
      <div className="flex justify-between items-center mb-4">
        <h4 className="font-medium">OCR Job: {job.id.slice(0, 8)}...</h4>
        <span className={`px-3 py-1 rounded-full text-sm font-semibold capitalize ${getStatusColor(job.status)}`}>
          {job.status}
        </span>
      </div>
      
      {job.status === JobStatus.PROCESSING && (
        <p className="text-sm text-gray-500">Processing document content. This may take a few moments...</p>
      )}
    </div>
  );
}
