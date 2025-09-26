import axios from "axios";
import { useState } from "react";

function FileUpload() {
  const [file] = useState(null);
  const [message, setMessage] = useState(""); 
  const handleFileChange:React.InputHTMLAttributes<HTMLInputElement>["onChange"] = (e) => {
    if (e.target.files && e.target.files[0]) {
      // setFile(e.target.!files[0]);
      setMessage(""); 
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); 

    try {
      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Upload successful!");
      console.log("Upload Success:", response.data);
    } catch (error) {
      setMessage("Upload failed.");
      console.error("Upload Error:", error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} className="ml-2 px-4 py-2 bg-zinc-500 rounded-2xl text-white hover:bg-zinc-600 transition">
        Upload
      </button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default FileUpload;
