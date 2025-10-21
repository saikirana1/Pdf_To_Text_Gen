import { useEffect, useState } from "react";
import axios from "axios";
import { useCounterStore } from "../store";
import { useNavigate } from "react-router-dom";

interface File {
  id: string;
  file_name: string;
  file_url: string;
}

const FileSelector = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<{ [key: string]: File }>({});
  const VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const { status, setFileDetails } = useCounterStore();
  const navigate = useNavigate();
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, [navigate]);
  useEffect(() => {
    const fetchData = async () => {
      await fetchFiles();
    };
    fetchData();
  }, [status]);

  useEffect(() => {
    if (selectedFiles) {
          setFileDetails?.(Object.values(selectedFiles));
      }
  
  }, [selectedFiles]);
  

  const fetchFiles = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No auth token found");
        return;
      }
      const res = await axios.get(`${VITE_BACKEND_URL}/get_files`, {
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

  const handleCheckboxChange = (file: File) => {
    const updated = { ...selectedFiles };
    if (updated[file.id]) {
      delete updated[file.id];
    } else {
      updated[file.id] = file;
    }
    setSelectedFiles(updated);

    
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h2>Uploaded Files</h2>
      <ul>
        {files.map(file => (
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

      {/* <h3>Selected URLs:</h3>
      <ul>
        {Object.values(selectedFiles).map(f => (
          <li key={f.id}>{f.file_url}</li>
        ))}
      </ul> */}
    </div>
  );
};

export default FileSelector;
