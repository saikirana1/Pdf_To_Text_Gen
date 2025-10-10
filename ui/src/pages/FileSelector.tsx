import { useEffect, useState } from "react";
import axios from "axios";

interface File {
  id: string;
  file_name: string;
  file_url: string;
}

interface FileButtonProps {
  onSelectionChange?: (urls: string[]) => void;
}

const FileSelector = ({ onSelectionChange }: FileButtonProps) => {
  const [files, setFiles] = useState<File[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<{ [key: string]: File }>({});
  const VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL ;

  useEffect(() => {
    const fetchData = async () => {
      await fetchFiles();
    };
    fetchData();
  }, []);

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

    if (onSelectionChange) {
      const urls = Object.values(updated).map(f => f.file_url);
      onSelectionChange(urls);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h2>Select Files</h2>
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

      <h3>Selected URLs:</h3>
      <ul>
        {Object.values(selectedFiles).map(f => (
          <li key={f.id}>{f.file_url}</li>
        ))}
      </ul>
    </div>
  );
};

export default FileSelector;
