import { useCounterStore } from "@/store";
import { Trash2 } from "lucide-react"; // Lucide React icon
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function SelectedFiles() {
  const { files_urls, removeFileDetails } = useCounterStore();
  const navigate = useNavigate();

  const handleRemove = (fileName: string) => {
    removeFileDetails(fileName);
  };
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, [navigate]);

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-semibold mb-4 text-center">
        Selected Files
      </h1>

      {files_urls && files_urls.length > 0 ? (
        <ul className="space-y-3">
          {files_urls.map((f, index) => (
            <li
              key={index}
              className="flex items-center justify-between bg-gray-100 p-3 rounded-lg shadow-sm hover:bg-gray-200 transition"
            >
              <span className="truncate text-gray-800">{f.file_name}</span>
              <button
                onClick={() => handleRemove(f.file_name)}
                className="text-red-500 hover:text-red-700 transition"
                title="Remove file"
              >
                <Trash2 size={20} />
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 text-center">No files selected yet.</p>
      )}
    </div>
  );
}

export default SelectedFiles;
