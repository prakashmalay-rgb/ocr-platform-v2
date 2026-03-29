"use client";

import { useState } from "react";
import { UploadOrchestrator } from "../services/orchestrator";

interface UploadDropzoneProps {
  onJobCreated: (jobId: string) => void;
}

export function UploadDropzone({ onJobCreated }: UploadDropzoneProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);

    try {
      const job = await UploadOrchestrator.executeFullFlow(file);
      onJobCreated(job.id);
    } catch (err: any) {
      setError(err.message || "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-8 border-2 border-dashed border-gray-300 rounded-lg text-center">
      <h3 className="text-xl font-semibold mb-2">Upload Document</h3>
      <p className="text-sm text-gray-500 mb-4">PDF, PNG, JPG (Max 10MB)</p>
      
      <input
        type="file"
        id="file-upload"
        className="hidden"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      
      <label
        htmlFor="file-upload"
        className={`px-6 py-2 rounded-md font-medium cursor-pointer transition-colors ${
          isUploading ? "bg-gray-400" : "bg-blue-600 text-white hover:bg-blue-700"
        }`}
      >
        {isUploading ? "Uploading..." : "Select File"}
      </label>

      {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}
    </div>
  );
}
