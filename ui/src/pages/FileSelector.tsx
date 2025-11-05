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
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
  PaginationEllipsis,
} from "@/components/ui/pagination";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import OpenPdf from "./OpenPdf";

interface File {
  id: string;
  file_name: string;
  file_url: string;
}

interface PaginatedFilesResponse {
  files: File[];
  total_records: number;
  total_pages: number;
  current_page: number;
  offset: number;
  limit: number;
}

const FileSelector = () => {
  const [selectedFiles, setSelectedFiles] = useState<{ [key: string]: File }>(
    {}
  );
  const [fileUrl, setFileUrl] = useState<string>("");
  const [items, setItems] = useState<File[]>([]);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const { status, setFileDetails, page, setPage } = useCounterStore();
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
  }, [selectedFiles, setFileDetails]);

  const fetchFiles = async () => {
    const offset = (page - 1) * 5;
    const response = await api.get(
      `${VITE_BACKEND_URL}/files?offset=${offset}&limit=8`
    );
    return response.data;
  };

  const { data, isLoading, error, isError } = useQuery<
    PaginatedFilesResponse,
    Error
  >({
    queryKey: ["files", page, status],
    queryFn: fetchFiles,
  });

  useEffect(() => {
    if (data) {
      setItems(data.files);
    }
  }, [data]);

  const handleCheckboxChange = (file: File) => {
    setSelectedFiles((prev) => {
      const updated = { ...prev };
      if (updated[file.id]) {
        delete updated[file.id];
      } else {
        updated[file.id] = file;
      }
      return updated;
    });
  };

  const deleteFileMutation = useMutation({
    mutationFn: async (fileId: string) => {
      setDeletingId(fileId);
      const res = await api.delete(`${VITE_BACKEND_URL}/files/${fileId}`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["files", page] });
      setDeletingId(null);
    },
    onError: (error) => {
      console.error("Error deleting file:", error);
      setDeletingId(null);
    },
  });

  const handleDeleteFile = (fileId: string) => {
    deleteFileMutation.mutate(fileId);
  };

  if (isLoading) return <Loading />;

  if (isError || error)
    return (
      <div className="text-red-600 text-center">
        Error While Loading Data: {error?.message}
      </div>
    );

  const totalPages = data?.total_pages || 1;
  console.log("fileUrl:", fileUrl);

  return (
    <div className="flex flex-row  p-4">
      <div className="w-2/5">
        <Card className="w-full max-w-sm">
          <CardHeader>
            <CardTitle>Uploaded Files</CardTitle>
            <CardDescription>
              Select the files you want to include
            </CardDescription>
          </CardHeader>

          <CardContent>
            {items && items.length > 0 ? (
              <ul className="space-y-2">
                {items.map((file) => (
                  <li
                    key={file.id}
                    className="flex items-center justify-between border p-2 rounded-lg transition-all"
                  >
                    <input
                      type="checkbox"
                      checked={!!selectedFiles[file.id]}
                      onChange={() => handleCheckboxChange(file)}
                      className="accent-gray-600 cursor-pointer"
                      title="Add the file"
                    />
                    <div className="ml-6 flex-1">
                      <span
                        className="cursor-pointer  transition-all hover:text-gray-500 hover:underline hover:decoration-gray-500"
                        title={file.file_name}
                        onClick={() => {
                          setFileUrl(file.file_url);
                        }}
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

          <CardFooter className="flex-col gap-2">
            <Pagination>
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious
                    href="#"
                    onClick={() => setPage((p: number) => Math.max(p - 1, 1))}
                    className={`${
                      page === 1 ? "pointer-events-none opacity-50" : ""
                    }`}
                  />
                </PaginationItem>
                {totalPages <= 2 ? (
                  [...Array(totalPages)].map((_, i) => (
                    <PaginationItem key={i}>
                      <PaginationLink
                        href="#"
                        isActive={page === i + 1}
                        onClick={() => setPage(i + 1)}
                      >
                        {i + 1}
                      </PaginationLink>
                    </PaginationItem>
                  ))
                ) : (
                  <>
                    {/* Show first 2 pages */}
                    {[1, 2].map((num) => (
                      <PaginationItem key={num}>
                        <PaginationLink
                          href="#"
                          isActive={page === num}
                          onClick={() => setPage(num)}
                        >
                          {num}
                        </PaginationLink>
                      </PaginationItem>
                    ))}

                    {/* Ellipsis for skipped pages */}
                    <PaginationItem>
                      <PaginationEllipsis />
                    </PaginationItem>

                    {/* Always show last page */}
                    <PaginationItem>
                      <PaginationLink
                        href="#"
                        isActive={page === totalPages}
                        onClick={() => setPage(totalPages)}
                      >
                        {totalPages}
                      </PaginationLink>
                    </PaginationItem>
                  </>
                )}

                <PaginationItem>
                  <PaginationNext
                    href="#"
                    onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                    className={`${
                      page === totalPages
                        ? "pointer-events-none opacity-50"
                        : ""
                    }`}
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </CardFooter>
        </Card>
      </div>
      <div className="w-3/5">
        <Card>
          <CardHeader>
            <CardTitle>PDF Preview</CardTitle>
            <CardDescription>View the selected file here</CardDescription>
          </CardHeader>
          <CardContent>
            {fileUrl ? (
              <OpenPdf fileUrl={fileUrl} />
            ) : (
              <h1 className="font-bold">No file chosen for preview.</h1>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default FileSelector;
