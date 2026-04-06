import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { OcrInterface } from '../../../components/features/OcrInterface';

interface ToolPageProps {
  params: {
    slug: string;
  };
}

/**
 * Dynamic Tool SEO Map (Sample of 180+).
 * In production, this would be fetched from a DB or JSON manifest.
 */
const TOOL_METADATA: Record<string, { title: string; description: string; h1: string }> = {
  'image-to-text': {
    title: 'Free Image to Text Converter | Accurate AI OCR',
    description: 'Convert images to text online for free with 100% accuracy. No sign-up required.',
    h1: 'Image to Text Converter',
  },
  'pdf-to-text': {
    title: 'PDF to Text Converter | Extract Text from PDF Online',
    description: 'Fast and reliable PDF to text conversion using advanced AI processing.',
    h1: 'PDF to Text Converter',
  },
  'excel-to-image': {
    title: 'Excel to Image Converter | Export Sheets to Photos',
    description: 'Convert your Excel spreadsheets into high-quality images instantly.',
    h1: 'Excel to Image Converter',
  },
  'word-to-pdf': {
    title: 'Word to PDF Converter | High Fidelity Document Export',
    description: 'Preserve formatting perfectly when converting Word docs to PDF online.',
    h1: 'Word to PDF Converter',
  },
  'jpg-to-ocr': {
    title: 'JPG to OCR Converter | Searchable Document Creation',
    description: 'Make your JPG images searchable with high-precision text recognition.',
    h1: 'JPG to OCR Converter',
  },
};

export async function generateMetadata({ params }: ToolPageProps): Promise<Metadata> {
  const tool = TOOL_METADATA[params.slug];

  if (!tool) {
    return { title: 'Online OCR Tool' };
  }

  return {
    title: tool.title,
    description: tool.description,
    openGraph: {
      title: tool.title,
      description: tool.description,
    },
    // Only point to production for canonical if content is 100% matched
    alternates: {
      canonical: `https://www.ocr-extraction.com/tools/${params.slug}`,
    },
  };
}

export default function ToolPage({ params }: ToolPageProps) {
  const tool = TOOL_METADATA[params.slug];

  if (!tool) {
    notFound();
  }

  return (
    <main className="flex-1 w-full bg-slate-50/30">
      <section className="relative overflow-hidden pt-20 pb-32 sm:pt-32 lg:pt-48">
        <div className="container px-4 mx-auto text-center">
          <span className="inline-block px-4 py-1.5 mb-6 text-sm font-semibold tracking-wide text-primary bg-primary/10 rounded-full">
            Free AI Tool
          </span>
          <h1 className="mb-6 text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl max-w-4xl mx-auto leading-[1.1]">
            {tool.h1}
          </h1>
          <p className="mb-10 text-lg leading-relaxed text-slate-600 max-w-2xl mx-auto">
            Experience the world&apos;s most accurate {tool.h1.toLowerCase()} converter. 
            Transform your documents instantly with zero registration and 100% data privacy.
          </p>

          <div className="mx-auto max-w-5xl">
            <OcrInterface />
          </div>
        </div>
      </section>

      {/* Feature section for SEO value */}
      <section className="py-20 bg-white border-y border-slate-100">
        <div className="container px-4 mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold mb-6">How it works</h2>
          <div className="grid gap-8 sm:grid-cols-3">
            <div>
              <div className="text-2xl font-bold text-primary mb-2">01</div>
              <p className="font-medium">Upload File</p>
            </div>
            <div>
              <div className="text-2xl font-bold text-primary mb-2">02</div>
              <p className="font-medium">AI Processing</p>
            </div>
            <div>
              <div className="text-2xl font-bold text-primary mb-2">03</div>
              <p className="font-medium">Download Result</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
