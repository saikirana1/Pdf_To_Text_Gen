import { useEffect, useRef, useState } from "react";
import FileUpload from "./FileUpload";
import { useCounterStore } from "../../src/store";
import { motion, AnimatePresence } from "framer-motion"; 
import toast from 'react-hot-toast';
import { useNavigate } from "react-router-dom";
import VoiceButton from "./VoiceButton";
import FileSelector from "./FileSelector";


interface Message {
  role: "user" | "assistant";
  text: string;
}
function Chat() {
  const navigate = useNavigate();
  const [userQuestion, setUserQuestion] = useState("");
  const eventSourceRef = useRef<EventSource | null>(null);
  const [chatData, setChatData] = useState<Message[]>([]);
  const [isMobile, setIsMobile] = useState(false);
  const [enurls, setEnurls] = useState("")
  const [endpoint,setEndpoint]=useState("")
  
  const { status, file, setFile ,setStatus} = useCounterStore();
  const [time, setTime] = useState(15);
  
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, [navigate]);
  
  useEffect(() => {
    if (!file) return; 
    
    let interval: ReturnType<typeof setInterval>;
    console.log("Status:", status);
    
    if (status !== "success") {
      interval = setInterval(() => {
        setTime((prev) => {
          if (prev <= 0) {
            return 15; 
          }
          return prev - 1;
        });
      }, 1000);
    }
    if (status === "success") {
      setFile?.("");
      setStatus("none");
      setTime(15);
      toast.success("✅ File uploaded successfully!", {
        style: {
          background: "#22c55e", 
          color: "white",
        },
        icon: '🚀'
      });
    }
    
    if (status === "error") {
      setFile?.("");
      setStatus("none");
      setTime(15);
      toast.error("❌ Error in file upload. Please try again.", {
        style: {
          background: "#dc2626", 
          color: "white",
        },
        icon: '⚠️'
      });
    }
    
    return () => {
      clearInterval(interval);
    };
  }, [file, status]); 
  
  
  
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    handleResize();
    window.addEventListener("resize", handleResize);
    
    return () => window.removeEventListener("resize", handleResize);
  }, []);

useEffect(() => {
  try {
    const decodedUrls = decodeURIComponent(enurls || "%5B%5D"); // safely decode
    const parsedUrls = JSON.parse(decodedUrls); // parse the JSON string

    if (Array.isArray(parsedUrls) && parsedUrls.length > 0) {
      setEndpoint("get_file_data");
    } else {
      setEndpoint("get_response");
    }
  } catch (error) {
    console.warn("Error decoding URLs:", error);
    setEndpoint("get_response");
  }
}, [enurls]);
console.log(time)

useEffect(() => {
  console.log(endpoint, "✅ current endpoint");
  console.log(typeof enurls, "🔍 type of enurls");
  console.log(enurls, "📁 encoded file URLs");
}, [endpoint, enurls]);


  
  let VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL
  const handleMicClick = (isRecording:any) => {
    if (isRecording) {
      console.log("🎤 Stopping recording...");
      
    }if(isRecording && userQuestion){
      console.log("🎙️ call api");
      if (!userQuestion.trim()) return;
      setChatData((prev) => [...prev, { role: "user", text: userQuestion }]);
      console.log(userQuestion);
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      
      const encodedQuestion = encodeURIComponent(userQuestion);
      const eventSource = new EventSource(
        `${VITE_BACKEND_URL}/get_response?user_question=${encodedQuestion}`
      );
      
      eventSource.onopen = () => {
        setChatData(prev => [...prev, { role: "assistant", text: "" }])
      }
      
      eventSource.onmessage = (event) => {
        setChatData((prev) => {
          const last = prev[prev.length - 1] || {};
          const head = prev.slice(0, prev.length - 1);
          return [
            ...head,
            { ...last, text: last.text + event.data }
          ]
        });
        console.log("Received:", event.data);
      };
      setUserQuestion("")
      
      eventSource.onerror = (err) => {
        console.error("SSE error:", err);
        eventSource.close();
      };
     
      
      eventSourceRef.current = eventSource;
      setUserQuestion("");
    }
  };
  const handleSelectedUrls = (urls:any) => {
    // console.log("Selected file URLs for OpenAI:", urls);
    const encodedUrls = encodeURIComponent(JSON.stringify(urls));
    setEnurls(encodedUrls)
    
  };

  console.log(enurls)
  const handle_onclick = () => {

    if (!userQuestion.trim()) return;
    setChatData((prev) => [...prev, { role: "user", text: userQuestion }]);
    console.log(userQuestion);
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    
    const encodedQuestion = encodeURIComponent(userQuestion);
    const eventSource = new EventSource(
      `${VITE_BACKEND_URL}/${endpoint}?user_question=${encodedQuestion}&urls=${enurls}`, {
        
      }
    );

    eventSource.onopen = () => {
      setChatData(prev => [...prev, { role: "assistant", text: "" }])
    }

    eventSource.onmessage = (event) => {
      setChatData((prev) => {
        const last = prev[prev.length - 1] || {};
        const head = prev.slice(0, prev.length - 1);
        return [
          ...head,
          { ...last, text: last.text + event.data }
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
   const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
   };
  return (

   <div className = "grid md:grid-cols-12 h-screen md:bg-zinc-900 bg-zinc-800" >
    {!isMobile && (
        <div className="col-span-3 flex items-center justify-center text-white">
          <FileSelector onSelectionChange={handleSelectedUrls} />
      </div>
          )
       }

      <div className="col-span-6 flex flex-col bg-zinc-800 p-4 rounded-lg overflow-y-auto">
       <AnimatePresence>
          {file && (<motion.div
      key="file-upload-status"
      initial={{ opacity: 0, y: -30, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -30, scale: 0.9 }}
      transition={{ duration: 0.4, type: "spring" }}
      className="bg-zinc-400 flex items-center justify-center rounded-lg mb-4 shadow-lg shadow-zinc-700"
    >
      <h1 className="inline-block text-zinc-900 font-semibold text-center text-lg animate-pulse">
       Preparing data... 
      </h1>
    </motion.div>
  )}
        </AnimatePresence>
        <div className="flex flex-col h-15">
         <button
        onClick={handleLogout}
        className="absolute top-4 right-4 px-2 py-2 bg-zinc-400 text-white rounded-lg hover:bg-gray-600 transition"
          >LogOut</button>
          </div>
       
          <ul className="flex flex-col space-y-2 flex-1 mb-20">
            {chatData.map((item, index) => (
              <li
                key={index}
                className={`p-3 rounded-lg max-w-[80%] break-words ${item.role === "user"
                    ? "text-white self-end text-right bg-zinc-900"
                    : "text-white self-start text-left bg-zinc-900"
                  }`}
              >
             
                <strong>{item.role === "user" ? "User" : "AI"}:</strong> {item.text}
              </li>
            ))}
          </ul>
          <div className="bg-zinc-800 p-1 mt-2 rounded-2xl border border-zinc-600 flex h-10 fixed bottom-3 w-full md:w-1/2 left-1/2 -translate-x-1/2">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handle_onclick();
              }}
              className="flex w-full"
            >
          
              <input
                type="text"
                className="w-full h-full p-3 outline-none bg-transparent text-white overflow-auto"
                placeholder="Ask me anything..."
                onChange={(e) => setUserQuestion(e.target.value)}
                value={userQuestion}
              />

              <button
              type="submit" 
              className="px-4 bg-zinc-500 rounded-2xl text-white hover:bg-zinc-400 transition"
            >
              Ask
          </button>
          {!userQuestion &&
            (
              <FileUpload />
            )
              
            }
              
            <VoiceButton onMicClick={handleMicClick} onTranscribe={(text: any) => setUserQuestion(text)} />
            
             
            </form>
          </div>
        </div>
       {!isMobile && <div className="col-span-3 pr-4 text-white"></div>}
        </div>
   
  );
}

export default Chat;
