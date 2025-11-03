import { useEffect, useState } from "react";
import { useCounterStore } from "../store";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/CustomHooks/axios";
import Loading from "@/CustomHooks/loading";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardTitle,
  CardHeader,
} from "@/components/ui/card";

import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";

interface File {
  id: string;
  file_name: string;
  file_url: string;
}

const FileSelector = () => {
  const [selectedFiles, setSelectedFiles] = useState<{ [key: string]: File }>(
    {}
  );
  const [items, setItems] = useState<File[]>([]);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const { status, setFileDetails } = useCounterStore();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, [navigate]);

  useEffect(() => {
    if (selectedFiles) {
      setFileDetails?.(Object.values(selectedFiles));
    }
  }, [selectedFiles]);

  const fetchFiles = async () => {
    try {
      const response = await api.get(`${VITE_BACKEND_URL}/files`, {});
      return response.data;
    } catch (err) {
      console.error("Error fetching files:", err);
    }
  };

  const { data, isLoading, error, isError } = useQuery<File[], Error>({
    queryKey: ["files", status],
    queryFn: fetchFiles,
  });

  useEffect(() => {
    if (data) {
      setItems(data);
    }
  }, [data]);

  const handleCheckboxChange = (file: File) => {
    const updated = { ...selectedFiles };
    if (updated[file.id]) {
      delete updated[file.id];
    } else {
      updated[file.id] = file;
    }
    setSelectedFiles(updated);
  };
  const deleteFileMutation = useMutation({
    mutationFn: async (fileId: string) => {
      setDeletingId(fileId);
      const res = await api.delete(`${VITE_BACKEND_URL}/files/${fileId}`);
      return res.data;
    },
    onSuccess: (data) => {
      console.log("File deleted successfully", data);
      queryClient.invalidateQueries({ queryKey: ["files"] });
    },
    onError: (error) => {
      console.error("Error deleting file:", error);
      return (
        <>
          <div>
            <h1 className="text-red-600">
              Error While Loading Data{error.message}
            </h1>
          </div>
        </>
      );
    },
  });
  const handleDeleteFile = (fileId: string) => {
    deleteFileMutation.mutate(fileId);
  };

  if (isLoading) {
    return <Loading />;
  }
  if (error || isError) {
    return (
      <>
        <div>
          <h1 className="text-red-600">
            Error While Loading Data{error.message}
          </h1>
        </div>
      </>
    );
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Uploaded Files</CardTitle>
        <CardDescription>Select the files you want to include</CardDescription>
      </CardHeader>
      <CardContent>
        {items && items.length > 0 ? (
          <ul>
            {items.map((file) => (
              <li
                key={file.id}
                className="flex items-center justify-between border p-2 rounded-lg transition-all "
              >
                <input
                  type="checkbox"
                  checked={!!selectedFiles[file.id]}
                  onChange={() => handleCheckboxChange(file)}
                  className="accent-gray-600 hover:accent-gray-600 cursor-pointer transition-all"
                  title="Add the file"
                />{" "}
                <div className="ml-6 flex-1">
                  <span
                    className="cursor-pointer hover:text-gray-500 transition-all"
                    title={file.file_name}
                  >
                    {file.file_name}
                  </span>
                </div>
                <Button
                  variant="default"
                  size="sm"
                  disabled={deletingId === file.id}
                  className={`transition-all duration-200 ${
                    deletingId === file.id
                      ? "bg-gray-400 cursor-not-allowed"
                      : "hover:bg-red-400 hover:text-white"
                  }`}
                  onClick={() => handleDeleteFile(file.id)}
                >
                  {deletingId === file.id ? (
                    <span className="animate-pulse">Deleting...</span>
                  ) : (
                    <Trash2 className="h-4 w-4 mr-1" />
                  )}
                </Button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No files uploaded yet.</p>
        )}
      </CardContent>
      <CardFooter className="flex-col gap-2"></CardFooter>
    </Card>
  );
};

export default FileSelector;
