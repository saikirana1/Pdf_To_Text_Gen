import { Button } from "@mui/material";
import axios from "axios";
import AttachmentIcon from "@mui/icons-material/Attachment";
import { useEffect, useState } from "react";
import { useCounterStore } from "../../src/store";

interface Message {
  status: string;
  result: string;
}

function FileUpload() {
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState<Message | null>(null);
  const VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const { setStatus, setFile } = useCounterStore();

  // Update global status whenever message changes
  useEffect(() => {
    if (message?.status) {
      setStatus?.(message.status);
    }
  }, [message, setStatus]);

  // Update global file name whenever it changes
  useEffect(() => {
    if (fileName) {
      setFile?.(fileName);
    }
  }, [fileName, setFile]);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    setFileName(selectedFile.name);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const token = localStorage.getItem("token");

      const response = await axios.post(`${VITE_BACKEND_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });

      setMessage({
        status: response.data.status,
        result: response.data.result,
      });

      console.log("Upload response:", response.data);
    } catch (error: any) {
      console.error("An error occurred:", error?.message || error);
      setStatus?.("error");
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
          "&:hover": { backgroundColor: "#52525b" },
          borderRadius: "4px",
        }}
        startIcon={<AttachmentIcon sx={{ color: "#f4f4f5", fontSize: 40 }} />}
      >
        <input type="file" hidden onChange={handleFileChange} />
      </Button>
    </div>
  );
}

export default FileUpload;
