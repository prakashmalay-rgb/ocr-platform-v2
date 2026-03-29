"use client";

import { useEffect, useState } from "react";
import { ResultsService } from "../../../services/api-client/results";
import { UnifiedResult } from "../../../types/job";

interface ResultViewerProps {
  jobId: string;
}

export function ResultViewer({ jobId }: ResultViewerProps) {
  const [result, setResult] = useState<UnifiedResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchResult = async () => {
      setLoading(true);
      try {
        const data = await ResultsService.getResult(jobId);
        setResult(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [jobId]);

  if (loading) return <div>Loading results...</div>;
  if (!result) return null;

  return (
    <div className="mt-8 space-y-6">
      <div className="p-6 bg-gray-50 rounded-lg">
        <h4 className="text-lg font-semibold mb-3">Extracted Text</h4>
        <pre className="whitespace-pre-wrap text-sm text-gray-800 bg-white p-4 border rounded font-mono">
          {result.raw_text}
        </pre>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 bg-white border rounded shadow-sm">
          <span className="block text-xs text-gray-500 uppercase">Confidence</span>
          <span className="text-lg font-bold">{Math.round(result.confidence_score * 100)}%</span>
        </div>
        <div className="p-4 bg-white border rounded shadow-sm">
          <span className="block text-xs text-gray-500 uppercase">Engine</span>
          <span className="text-lg font-bold">{result.metadata.ocr_engine}</span>
        </div>
      </div>
    </div>
  );
}
