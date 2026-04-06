"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useState } from "react";
import { Turnstile } from "@marsidev/react-turnstile";

const TURNSTILE_SITE_KEY = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY || "1x00000000000000000000AA";

const leadSchema = z.object({
  full_name: z.string().min(2, "Full name must be at least 2 characters."),
  email: z.string().email("Please enter a valid email address."),
  company: z.string().optional(),
  message: z.string().min(10, "Message must be at least 10 characters.").max(2000),
  turnstile_token: z.string().min(1, "Cloudflare Turnstile token required."),
});

type LeadFormValues = z.infer<typeof leadSchema>;

export function ContactForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<"idle" | "success" | "error">("idle");

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
  } = useForm<LeadFormValues>({
    resolver: zodResolver(leadSchema),
  });

  const onSubmit = async (data: LeadFormValues) => {
    setIsSubmitting(true);
    setSubmitStatus("idle");

    try {
      const payload = {
        ...data,
        source_env: process.env.NEXT_PUBLIC_BASE_PATH === "/v2" ? "staging" : "production"
      };

      const response = await fetch("/api/v1/leads/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Submission failed.");

      setSubmitStatus("success");
      reset();

      // Trigger GTM/GA4 Event
      interface Window { gtag?: (event: string, action: string, params: object) => void; }
      const win = window as unknown as Window;
      if (win.gtag) {
        win.gtag("event", "lead_conversion", {
          event_category: "leads",
          event_label: "contact_form",
        });
      }
    } catch (err) {
      console.error("Lead submission error:", err);
      setSubmitStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label htmlFor="full_name" className="block text-sm font-semibold text-slate-900">
          Full Name
        </label>
        <input
          {...register("full_name")}
          id="full_name"
          className="mt-2 block w-full rounded-lg border border-slate-200 px-4 py-2 text-slate-900 focus:border-primary focus:ring-1 focus:ring-primary h-12"
          placeholder="Jane Doe"
        />
        {errors.full_name && <p className="mt-1 text-sm text-red-500">{errors.full_name.message}</p>}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-semibold text-slate-900">
          Email Address
        </label>
        <input
          {...register("email")}
          id="email"
          type="email"
          className="mt-2 block w-full rounded-lg border border-slate-200 px-4 py-2 text-slate-900 focus:border-primary focus:ring-1 focus:ring-primary h-12"
          placeholder="jane@example.com"
        />
        {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="company" className="block text-sm font-semibold text-slate-900">
          Company (Optional)
        </label>
        <input
          {...register("company")}
          id="company"
          className="mt-2 block w-full rounded-lg border border-slate-200 px-4 py-2 text-slate-900 focus:border-primary focus:ring-1 focus:ring-primary h-12"
        />
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-semibold text-slate-900">
          How can we help?
        </label>
        <textarea
          {...register("message")}
          id="message"
          rows={4}
          className="mt-2 block w-full rounded-lg border border-slate-200 px-4 py-2 text-slate-900 focus:border-primary focus:ring-1 focus:ring-primary"
          placeholder="Tell us about your project..."
        />
        {errors.message && <p className="mt-1 text-sm text-red-500">{errors.message.message}</p>}
      </div>

      <div className="flex justify-center py-2">
        <Turnstile
          siteKey={TURNSTILE_SITE_KEY}
          onSuccess={(token) => setValue("turnstile_token", token)}
        />
        {errors.turnstile_token && (
          <p className="mt-1 text-sm text-red-500">{errors.turnstile_token.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-lg bg-primary px-4 py-3 font-semibold text-white transition-all hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? "Sending..." : "Submit Inquiry"}
      </button>

      {submitStatus === "success" && (
        <div className="rounded-lg bg-green-50 p-4 text-sm font-medium text-green-800">
          Thank you! We have received your inquiry and will reach out shortly.
        </div>
      )}

      {submitStatus === "error" && (
        <div className="rounded-lg bg-red-50 p-4 text-sm font-medium text-red-800">
          Something went wrong. Please try again later.
        </div>
      )}
    </form>
  );
}
