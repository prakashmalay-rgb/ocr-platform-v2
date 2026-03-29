"use client";

import { useState } from "react";
import { UploadDropzone } from "../features/upload/components/UploadDropzone";
import { JobStatusTracker } from "../features/jobs/components/JobStatusTracker";
import { ResultViewer } from "../features/results/components/ResultViewer";
import { useJobStatus } from "../hooks/useJobStatus";
import { JobStatus } from "../types/job";

export default function Home() {
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const { job, error } = useJobStatus(activeJobId);

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto space-y-12">
      <header className="border-b pb-6">
        <h1 className="text-3xl font-bold text-gray-900">OCR Platform V2</h1>
        <p className="text-gray-500">Secure, high-load document processing.</p>
      </header>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Step 1: Upload and Process</h2>
        <UploadDropzone onJobCreated={setActiveJobId} />
      </section>

      {activeJobId && (
        <section className="space-y-4">
          <h2 className="text-xl font-semibold">Step 2: Tracking & Results</h2>
          <JobStatusTracker job={job} error={error} />
          {job?.status === JobStatus.COMPLETED && (
            <ResultViewer jobId={activeJobId} />
          )}
        </section>
      )}
    </main>
  );
}
