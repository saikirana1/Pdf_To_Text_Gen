import { useEffect, useRef, useState } from "react";
import FileUpload from "./FileUpload";

interface Message {
  role: "user" | "assistant";
  text: string;
}

function Chat() {
  const [userQuestion, setUserQuestion] = useState("");
  const eventSourceRef = useRef<EventSource | null>(null); 
  const [chatData, setChatData] = useState<Message[]>([]);
  

  const handle_onclick = () => {
    if (!userQuestion.trim()) return;
    setChatData((prev) => [...prev, { role: "user", text: userQuestion }]);
    console.log(userQuestion);
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    const encodedQuestion = encodeURIComponent(userQuestion);
    const eventSource = new EventSource(
      `http://localhost:8000/get_response?user_question=${encodedQuestion}`
    );

    eventSource.onopen = () => {
      setChatData(prev => [...prev, {role: "assistant", text: ""}])
    }

    eventSource.onmessage = (event) => {
      setChatData((prev) => {
        const last = prev[prev.length - 1] || {};
        const head = prev.slice(0, prev.length - 1);
        return [
          ...head,
          {...last, text: last.text + event.data}
        ]
      });
      console.log("Received:", event.data);
    };

    eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      eventSource.close();
    };

    eventSourceRef.current = eventSource; 
    setUserQuestion(""); 
  };

useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        console.log("EventSource closed on unmount");
      }
    };
  }, []);

  return (
    <div className="grid grid-cols-12 h-screen bg-zinc-900">
      <div className="col-span-3 flex items-center justify-center text-white"></div>
      <div className="col-span-6 flex flex-col bg-zinc-800 p-4 rounded-lg overflow-y-auto">
        <ul className="flex flex-col space-y-2 flex-1 mb-20">
          {chatData.map((item, index) => (
            <li
              key={index}
              className={`p-3 rounded-lg max-w-[80%] break-words ${
                item.role === "user"
                  ? "text-white self-end text-right bg-gray-700"
                : "text-white self-start text-left bg-gray-600"
              }`}
            >
             
              <strong>{item.role === "user" ? "User" : "AI"}:</strong> {item.text}
            </li>
          ))}
        </ul>
        <div className="bg-zinc-800 p-1 mt-2 rounded-2xl border border-zinc-700 flex h-16 fixed bottom-1 w-1/3 left-1/2 -translate-x-1/2">
                <form
          onSubmit={(e) => {
            e.preventDefault(); 
            handle_onclick();
          }}
          className="flex w-full"
        >
              <input
                type="text"
                className="w-full h-full p-3 outline-none bg-transparent text-white"
                placeholder="Ask me anything..."
                onChange={(e) => setUserQuestion(e.target.value)}
                value={userQuestion}
              />
                {/* <input
    type="file"
    // onChange={(e) => setUserFile(e.target.files[0])} // handle file selection
  /> */}

            <button
              type="submit" 
              className="px-4 bg-zinc-500 rounded-2xl text-white hover:bg-zinc-600 transition"
            >
              Ask
            </button>
        </form>
        </div>
      </div>
      <div className="col-span-3 flex items-center justify-items-center pr-4 text-white" >
          <FileUpload/>
      </div>
    </div>
  );
}

export default Chat;
