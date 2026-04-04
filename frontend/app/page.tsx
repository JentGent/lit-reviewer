"use client";

import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  async function handleUpload() {
    if (!file) {
      setStatus("Pick a PDF first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");

    let data;

    try {
      const res = await fetch(`${API_BASE}/get-references`, {
        method: "POST",
        body: formData,
      });

      data = await res.json();

      if (!res.ok) {
        setStatus(data.error || "Upload failed.");
        return;
      }
    } catch (e) {
      setStatus("Upload failed.");
      return;
    }

    setStatus(`${data.message}`);
  }

  return (
    <main className="p-10 max-w-xl">
      <h1 className="text-2xl font-bold">PDF Citation Extractor</h1>
      <p className="mt-2 text-gray-600">
        Upload a PDF and save it to the backend.
      </p>

      <div className="mt-6 flex flex-col gap-3">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />

        <button
          className="rounded bg-black px-4 py-2 text-white"
          onClick={handleUpload}
        >
          Upload PDF
        </button>

        <p className="text-sm text-gray-700">{status}</p>
      </div>
    </main>
  );
}