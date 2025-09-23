import { createFileRoute } from '@tanstack/react-router';
import React, { useState, useEffect } from "react";

export const Route = createFileRoute('/about')({
  component: RouteComponent,
});

function RouteComponent() {
  const [userQuestion, setUserQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [eventSource, setEventSource] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    setMessages([]); // Clear previous messages

    // Close previous SSE connection if it exists
    if (eventSource) {
      eventSource.close();
    }

    // Create new SSE connection
    const encodedQuestion = encodeURIComponent(userQuestion);
    const source = new EventSource(`http://localhost:8000/get_response?user_question=${encodedQuestion}`);

    source.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    source.onerror = (err) => {
      console.error("SSE error:", err);
      source.close();
    };

    setEventSource(source);
    setUserQuestion(""); // Clear input after sending
  };

  // Cleanup SSE when component unmounts
  useEffect(() => {
    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [eventSource]);

  return (
    <div style={{ padding: "20px" }}>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={userQuestion}
          onChange={(e) => setUserQuestion(e.target.value)}
          placeholder="Type your question..."
          required
          style={{ padding: "8px", width: "300px" }}
        />
        <button type="submit" style={{ padding: "8px 12px", marginLeft: "8px" }}>Send</button>
      </form>

      <div>
  {messages.length > 0 && (
    <p style={{ backgroundColor: "#f1f1f1", padding: "8px", borderRadius: "4px", whiteSpace: "pre-wrap" }}>
      {messages.join("")}
    </p>
  )}
</div>
    </div>
  );
}
