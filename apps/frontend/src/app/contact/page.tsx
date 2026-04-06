import { ContactForm } from "@/features/leads/components/ContactForm";

export const metadata = {
  title: "Contact Us | Custom OCR Solutions & Enterprise AI",
  description: "Get in touch for custom OCR integration, high-volume document processing, or enterprise AI consulting.",
};

export default function ContactPage() {
  return (
    <main className="flex-1 w-full bg-slate-50/30">
      <section className="relative pt-24 pb-32 overflow-hidden">
        <div className="container px-4 mx-auto">
          <div className="max-w-5xl mx-auto">
            <div className="flex flex-wrap -mx-4 items-center">
              <div className="w-full lg:w-1/2 px-4 mb-16 lg:mb-0">
                <span className="inline-block px-4 py-1.5 mb-6 text-sm font-semibold tracking-wide text-primary bg-primary/10 rounded-full">
                  Partner with experts
                </span>
                <h1 className="mb-6 text-5xl font-extrabold tracking-tight text-slate-900 leading-[1.1]">
                  Let&apos;s build the future of extraction.
                </h1>
                <p className="mb-10 text-xl leading-relaxed text-slate-600">
                  Whether you need a custom LLM pipeline, high-volume automated OCR, 
                  or an expert AI audit, our engineering team is here to help.
                </p>
                
                <div className="space-y-4">
                  <div className="flex items-center text-slate-700">
                    <span className="w-6 h-6 flex items-center justify-center bg-primary/10 rounded-full mr-3 text-primary">✓</span>
                    <span className="font-medium">99.9% Extraction Accuracy</span>
                  </div>
                  <div className="flex items-center text-slate-700">
                    <span className="w-6 h-6 flex items-center justify-center bg-primary/10 rounded-full mr-3 text-primary">✓</span>
                    <span className="font-medium">Enterprise-ready HIPAA Compliance</span>
                  </div>
                  <div className="flex items-center text-slate-700">
                    <span className="w-6 h-6 flex items-center justify-center bg-primary/10 rounded-full mr-3 text-primary">✓</span>
                    <span className="font-medium">Dedicated Support SLA</span>
                  </div>
                </div>
              </div>

              <div className="w-full lg:w-1/2 px-4 shadow-xl rounded-2xl bg-white border border-slate-100 p-8 sm:p-12">
                <h2 className="text-2xl font-bold mb-8 text-slate-900">Send an inquiry</h2>
                <ContactForm />
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
