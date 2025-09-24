import React, { useEffect, useState } from 'react'

function Chat() {
     const [messages, setMessages] = useState<string[]>([]);
     const [userQuestion, setUserQuestion] = useState("");

function get_evet_data(){

const handle_onclick=()=>{
  console.log(userQuestion)
  const eventSource = new EventSource("http://localhost:8000/get_response?user_question=${encodedQuestion}");
  eventSource.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
      console.log(event.data)
      console.log(messages)
    };
     eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      eventSource.close();
    };
  setUserQuestion("")
    
}

   return (
     <>
       <div className="grid grid-cols-5 h-screen text-center">
         {/* <div className="col-span-1 bg-zinc-800">
         </div> */}
 
         <div className="col-span-full">
           <div className="container h-120">
            {messages}

           </div>
 
           <div className="bg-zinc-800 w-1/2 p-1 pr-5 text-white m-auto rounded-2xl border border-zinc-700 flex h-16">
             <input
               type="text"
               className="w-full h-full p-3 outline-none bg-transparent"
               placeholder="Ask me anything..."
               onChange={(e)=>setUserQuestion(e.target.value)}
               value={userQuestion}
             />
             <button className="px-4" onClick={handle_onclick}>Ask</button>
           </div>
         </div>
       </div>
     </>
   )
}

export default Chat