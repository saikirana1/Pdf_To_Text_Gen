import { Button } from "@mui/material";
import axios from "axios";
import AttachmentIcon from "@mui/icons-material/Attachment";
import { useEffect, useState } from "react";
import { useCounterStore } from "../../src/store";
interface Message{
  status: string;
  result: string;
}

function FileUpload() {
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState<Message| null>( null);
  let VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL
  
  const { setStatus,setFile } = useCounterStore();
  useEffect(() => {
    if (message?.status === "success") {
      setStatus("success")
    }
    if (message?.status === "error") {
        setStatus("error")
      }
    
  
  }, [message]);

  useEffect(() => {
    if (fileName) { 
      setFile?.(fileName);
  }
    
  
    }, [fileName]);
  
  
  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    setFileName(selectedFile.name);
    // console.log("Selected file:", fileName);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const token = localStorage.getItem("token");

    const response = await axios.post(
      `${VITE_BACKEND_URL}/upload`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`, // ✅ send token in header
        },
      }
    );
       setMessage({
      status: response.data.status,
      result: response.data.result 
});
  
       console.log(message);
      console.log(response.data)
    } catch (error) {
       setStatus("error")

      console.error("Upload Error:", error);
    }
    
  };

  return (
    <div>
      <Button
        component="label"
        variant="contained"
        sx={{
          backgroundColor: "#27272a",
          color: "#f4f4f5",
          "&:hover": { backgroundColor: "#52525b" }, // hover effect
          borderRadius: "4px",
        }}
        startIcon={<AttachmentIcon sx={{ color: "#f4f4f5", fontSize: 40 }} />}
      >
        <input type="file" hidden onChange={handleFileChange} />
      </Button>

      {/* {fileName && (
        <Typography variant="body1" sx={{ marginTop: 2 }}>
          Selected file: {fileName}
        </Typography>
      )}

      {message && (
        <Typography
          variant="body2"
          color={message.includes("successful") ? "green" : "red"}
          sx={{ marginTop: 1 }}
        >
          {message}
        </Typography>
      )} */}
    </div>
  );
}

export default FileUpload;
