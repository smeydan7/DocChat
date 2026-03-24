import { FormEvent, useState } from "react";
import { askQuestion, uploadDocument } from "./api";
import type { AskResponse } from "./types";

export default function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<AskResponse | null>(null);
  const [status, setStatus] = useState<string>("Ready");

  async function handleUpload(e: FormEvent) {
    e.preventDefault();

    if (!selectedFile) {
      setStatus("Please choose a PDF before uploading.");
      return;
    }

    setStatus("Uploading document...");
    try {
      const result = await uploadDocument(selectedFile);
      setStatus(`Upload scaffold reached: ${result.file_name}`);
    } catch {
      setStatus("Upload failed. Check backend logs.");
    }
  }

  async function handleAsk(e: FormEvent) {
    e.preventDefault();
    if (!question.trim()) {
      setStatus("Please enter a question.");
      return;
    }

    setStatus("Asking question...");
    try {
      const result = await askQuestion(question.trim());
      setAnswer(result);
      setStatus("Response received.");
    } catch {
      setStatus("Question request failed. Check backend logs.");
    }
  }

  return (
    <main className="container">
      <h1>Chat with Your Docs</h1>
      <p className="subtitle">
        First commit groundwork: upload and ask flows are scaffolded.
      </p>

      <section className="card">
        <h2>1) Upload PDF</h2>
        <form onSubmit={handleUpload}>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
          />
          <button type="submit">Upload</button>
        </form>
      </section>

      <section className="card">
        <h2>2) Ask Question</h2>
        <form onSubmit={handleAsk}>
          <textarea
            placeholder="Ask something about your uploaded docs..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button type="submit">Ask</button>
        </form>
      </section>

      <section className="card">
        <h2>Answer</h2>
        {answer ? (
          <>
            <p>{answer.answer}</p>
            <h3>Sources</h3>
            {answer.sources.length === 0 ? (
              <p>No sources yet in scaffold response.</p>
            ) : (
              <ul>
                {answer.sources.map((source) => (
                  <li key={`${source.document_id}-${source.chunk_index}`}>
                    {source.text}
                  </li>
                ))}
              </ul>
            )}
          </>
        ) : (
          <p>No answer yet.</p>
        )}
      </section>

      <p className="status">Status: {status}</p>
    </main>
  );
}
