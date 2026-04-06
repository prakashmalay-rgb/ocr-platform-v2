"use client";

import { useState } from "react";
import { UploadDropzone } from "../../features/upload/components/UploadDropzone";
import { JobStatusTracker } from "../../features/jobs/components/JobStatusTracker";
import { ResultViewer } from "../../features/results/components/ResultViewer";
import { useJobStatus } from "../../hooks/useJobStatus";
import { JobStatus } from "../../types/job";

export function OcrInterface() {
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const { job, error } = useJobStatus(activeJobId);

  return (
    <div className="space-y-12">
      <section className="layered-card p-4 sm:p-8 bg-white max-w-2xl mx-auto">
        <div className="mb-6 text-center">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            Upload and Process
          </h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Convert any image or PDF to editable text in seconds.
          </p>
        </div>
        <UploadDropzone onJobCreated={setActiveJobId} />
      </section>

      {activeJobId && (
        <section className="layered-card p-4 sm:p-8 bg-white max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-slate-900">Processing Your File</h2>
            <p className="mt-1 text-sm text-slate-500">Status updates live...</p>
          </div>
          <JobStatusTracker job={job} error={error} />
          {job?.status === JobStatus.COMPLETED && (
            <div className="mt-8 border-t border-slate-100 pt-8">
              <ResultViewer jobId={activeJobId} />
            </div>
          )}
        </section>
      )}
    </div>
  );
}
