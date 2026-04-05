"use client";

import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function Home() {
  const [researchProblem, setResearchProblem] = useState("What are the effects of sleep deprivation on memory consolidation?");
  const [error, setError] = useState("");
  const [thinking, setThinking] = useState("");

  async function handleStart() {
    setThinking("");
    setError("");

    try {
      const rsp = await fetch(API_BASE + "/api/rewrite-query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: researchProblem }),
      });
      if (!rsp.ok || !rsp.body) {
        throw new Error("Failed to rewrite query");
      }

      const reader = rsp.body.getReader();
      const decoder = new TextDecoder();
      let data = "";

      streamLoop: while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        data += decoder.decode(value, { stream: true });
        const parts = data.split("\n\n");
        data = parts.pop() || "";
        const prefix = "data: ";
        for (const part of parts) {
          const line = part.split("\n").find(l => l.startsWith(prefix));
          if (!line) continue;
          const payload = JSON.parse(line.slice(prefix.length));
          switch (payload.type) {
            case "chunk":
              setThinking(prev => prev + payload.text);
              break;
            case "error":
              throw new Error(payload.message);
              break;
            case "end":
              break streamLoop;
          }
        }
      }
    } catch (err) {
      setThinking(err instanceof Error ? err.message : "Something went wrong");
    } finally {

    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-xl space-y-6 text-center">
        <h1 className="text-3xl font-semibold text-black">
          Literature Reviewer
        </h1>

        <p className="text-gray-600">
          Enter your research problem and watch the AI think step-by-step
        </p>

        <textarea
          value={researchProblem}
          onChange={(e) => setResearchProblem(e.target.value)}
          placeholder="What are the effects of sleep deprivation on memory consolidation?"
          className="w-full text-black resize-none rounded-2xl border border-gray-300 p-4 shadow-sm text-left"
        />

        <button
          onClick={handleStart}
          className="w-full rounded-2xl bg-black text-white py-3 font-medium hover:opacity-80 active:opacity-90 transition"
        >
          Start
        </button>

        <div
          className="text-gray-500"
        >
          {thinking}
        </div>
      </div>
    </main>
  );
}