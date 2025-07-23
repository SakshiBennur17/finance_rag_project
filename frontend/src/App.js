import React, { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askBackend = async () => {
    if (!question.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setAnswer(data.answer || "No answer received.");
    } catch (error) {
      console.error("Error:", error);
      setAnswer("Error connecting to backend.");
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Finance Chatbot</h1>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something..."
        style={{ padding: "10px", width: "300px" }}
      />
      <button
        onClick={askBackend}
        style={{
          padding: "10px 20px",
          marginLeft: "10px",
          backgroundColor: "blue",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Ask
      </button>
      <div style={{ marginTop: "20px", fontSize: "18px" }}>
        <b>Answer:</b> {answer}
      </div>
    </div>
  );
}

export default App;

