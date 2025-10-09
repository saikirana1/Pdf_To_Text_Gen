import  { useEffect, useState } from "react";
import axios from "axios";

const FileSelector = ({ onSelectionChange }) => {
  const [files, setFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState({});
  let VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL; // {id: file}

  // Fetch all files from backend
  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(`${VITE_BACKEND_URL}/files`, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });
      setFiles(res.data);
    } catch (err) {
      console.error("Error fetching files:", err);
    }
  };

  const handleCheckboxChange = (file: any) => {
    const updated = { ...selectedFiles };
    if (updated[file.id]) {
      delete updated[file.id];
    } else {
      updated[file.id] = file;
    }
    setSelectedFiles(updated);

    // Send selected URLs to parent component or anywhere
    if (onSelectionChange) {
      const urls = Object.values(updated).map((f) => f.file_url);
      onSelectionChange(urls);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h2>Select Files</h2>
      <ul>
        {files.map((file) => (
          <li key={file.id}>
            <input
              type="checkbox"
              checked={!!selectedFiles[file.id]}
              onChange={() => handleCheckboxChange(file)}
            />{" "}
            {file.file_name}
          </li>
        ))}
      </ul>

      <h3>Selected URLs:</h3>
      {/* <ul>
        {Object.values(selectedFiles).map((f) => (
          <li key={f.id}>{f.file_url}</li>
        ))}
      </ul> */}
    </div>
  );
};

export default FileSelector;
