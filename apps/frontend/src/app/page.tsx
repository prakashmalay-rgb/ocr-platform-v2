import { OcrInterface } from "../components/features/OcrInterface";

export default function Home() {
  return (
    <main className="flex-1 w-full bg-slate-50/30">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-32 sm:pt-32 lg:pt-48">
        <div className="container px-4 mx-auto text-center">
          <span className="inline-block px-4 py-1.5 mb-6 text-sm font-semibold tracking-wide text-primary bg-primary/10 rounded-full">
            AI-Powered Extraction
          </span>
          <h1 className="mb-6 text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl max-w-4xl mx-auto leading-[1.1]">
            Free <span className="text-primary italic">OCR To Text</span> Converter
          </h1>
          <p className="mb-10 text-lg leading-relaxed text-slate-600 max-w-2xl mx-auto">
            Experience the world&apos;s most accurate image-to-text converter. Transform PDF, JPG, and PNG documents into editable formats instantly with 100% precision.
          </p>

          <div className="mx-auto max-w-5xl">
            {/* The OCR Interface - Client Component */}
            <OcrInterface />
          </div>
        </div>
      </section>

      {/* SEO Value Section */}
      <section className="py-24 bg-white border-y border-slate-100">
        <div className="container px-4 mx-auto">
          <div className="grid gap-16 lg:grid-cols-2">
            <div>
              <h2 className="mb-8 text-3xl font-bold tracking-tight text-slate-900">
                Why OCR Platform V2?
              </h2>
              <div className="space-y-6">
                <div>
                  <h3 className="mb-2 text-lg font-semibold text-slate-900">Global AI Infrastructure</h3>
                  <p className="text-slate-600">
                    Built on high-load, cybersecure architecture to handle enterprise-level document processing. No registration required, ensuring privacy and speed.
                  </p>
                </div>
                <div>
                  <h3 className="mb-2 text-lg font-semibold text-slate-900">100% Accuracy Guaranteed</h3>
                  <p className="text-slate-600">
                    Our proprietary AI models utilize next-generation LLMs to understand context and ensure data integrity beyond simple character recognition.
                  </p>
                </div>
              </div>
            </div>

            <div className="layered-card p-12 bg-slate-50 flex items-center justify-center">
              <div className="text-center">
                <blockquote className="italic text-2xl text-slate-900 mb-6">
                  &ldquo;The most reliable tool for our audit workflows.&rdquo;
                </blockquote>
                <cite className="font-semibold text-slate-600 not-italic">
                  &mdash; Lead Engineer, Top 1% AI Firm
                </cite>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Structured Content for SEO */}
      <section className="py-20 bg-slate-50/50">
        <div className="container px-4 mx-auto max-w-3xl">
          <h2 className="text-3xl font-bold mb-10 text-center">Technical Specifications</h2>
          <div className="prose prose-slate max-w-none">
            <p>
              OCR Extraction is a global AI platform specializing in AI workflow orchestration, AI-powered tools, and providing expertise through top-tier AI engineers. Our mission is to democratize access to advanced document processing.
            </p>
            <p>
              Leveraging Next.js 16 and FastAPI, we provide a seamless bridge between front-end aesthetics and back-end raw processing power. Our workers are optimized for MLOps, LLMs, and GenAI applications.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
