"use client";

import { useEffect, useState } from "react";

type Status = "idle" | "loading" | "done" | "error";

// آدرس بک‌اند از .env.local
const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

export default function Home() {
  const [idea, setIdea] = useState<string>("");
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);

  const fetchIdea = async () => {
    setStatus("loading");
    setError(null);
    setIdea("");

    try {
      const res = await fetch(`${BACKEND_URL}/`, {
        method: "GET",
        headers: {
          Accept: "text/plain",
        },
      });

      const text = await res.text();

      if (!res.ok) {
        throw new Error(text || "Request failed");
      }

      setIdea(text.trim());
      setStatus("done");
    } catch (err: any) {
      setError("Error: " + (err?.message || "Something went wrong"));
      setStatus("error");
    }
  };

  useEffect(() => {
    fetchIdea();
  }, []);

  return (
    <main
      className="
        min-h-screen
        bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950
        text-slate-100
        flex items-center justify-center
        px-4
      "
    >
      <div className="w-full max-w-4xl">
        {/* Header */}
        <header className="text-center mb-10">
          <h1
            className="
              text-4xl md:text-5xl font-extrabold tracking-tight
              text-blue-400
              drop-shadow-[0_0_25px_rgba(37,99,235,0.45)]
            "
          >
            Business Idea Generator
          </h1>
          <p className="mt-4 text-slate-300">
            AI-powered innovation at your fingertips
          </p>
        </header>

        {/* Card */}
        <section
          className="
            bg-slate-900/80
            border border-slate-700
            rounded-3xl
            shadow-2xl
            px-6 sm:px-10 py-8 sm:py-10
            flex items-center justify-center
            min-h-[220px]
          "
        >
          {status === "loading" && (
            <p className="text-slate-400 animate-pulse">
              Generating your business idea...
            </p>
          )}

          {status === "done" && (
            <p className="text-slate-100 whitespace-pre-wrap leading-relaxed">
              {idea}
            </p>
          )}

          {status === "error" && (
            <p className="text-red-400 whitespace-pre-wrap">
              {error}
            </p>
          )}
        </section>

        {/* Actions */}
        <div className="mt-6 flex justify-center">
          <button
            onClick={fetchIdea}
            className="
              inline-flex items-center gap-2
              rounded-full
              bg-blue-500 hover:bg-blue-600 active:bg-blue-700
              px-5 py-2
              text-sm font-medium
              shadow-lg shadow-blue-500/30
              transition-colors
            "
          >
            Generate another idea
          </button>
        </div>
      </div>
    </main>
  );
}
