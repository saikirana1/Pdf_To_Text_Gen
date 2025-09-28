import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { Button, Typography } from "@mui/material";
import axios from "axios";
import AttachmentIcon from "@mui/icons-material/Attachment";
import { useState } from "react";

function FileUpload() {
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState("");

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    setFileName(selectedFile.name);
    console.log("Selected file:", selectedFile.name);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        },
      );
      setMessage("Upload successful!");
      console.log("Upload Success:", response.data);
    } catch (error) {
      setMessage("Upload failed.");
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
